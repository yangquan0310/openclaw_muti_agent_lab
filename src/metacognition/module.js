/**
 * 元认知模块 —— 面向对象封装
 *
 * 插件职责：在合适的时机将对应的 skill 文档注入 Agent 的 system context
 * Agent 职责：自行阅读 skill、判断偏差、决定是否 revise
 *
 * v3.4.0 变更：
 * - 移除插件自动创建 task JSON，改为 Agent 评估 + 用户确认后延迟创建
 * - 新增 assessment 阶段：before_prompt_build（无 task）→ 注入 assessment skill
 * - llm_output 检测 [NEED_PLAN] 标记后创建 task，再注入 planning skill
 *
 * Plan 状态机：
 *   draft → pending_approval → active → completed
 *   ├─ draft: Agent 制定并汇报 Plan
 *   ├─ pending_approval: 等待用户确认
 *   └─ active: 用户确认后按 phases 执行
 */

import { generatePlan, assignSessionsToPhases, getNow } from '../common/utils.js';

export class MetacognitionModule {
  constructor({ api, config, stateAdapter, skillLoader, logger, planManager, deviationManager, attributionManager }) {
    this.api = api;
    this.config = config || {};
    this.stateAdapter = stateAdapter;
    this.skillLoader = skillLoader;
    this.logger = logger;
    this.planManager = planManager;
    this.deviationManager = deviationManager;
    this.attributionManager = attributionManager;
    this.enabled = this.config.enabled !== false;
    this.assessmentEnabled = this.enabled && this.config.assessment !== false;
    this.planningEnabled = this.enabled && this.config.planning !== false;
    this.monitoringEnabled = this.enabled && this.config.monitoring !== false;
  }

  register() {
    if (!this.enabled) {
      this.logger.info('[Meta] 元认知模块已禁用');
      return;
    }

    this.logger.info('[Meta] 注册元认知 Hooks');
    this._registerAssessment();
    this._registerPlanning();
    this._registerMonitoring();
    this._registerCleanup();
  }

  // ── 任务评估: before_prompt_build（无 task 时）──
  _registerAssessment() {
    if (!this.assessmentEnabled) return;
    this.api.on('before_prompt_build', this.onBeforePromptBuild.bind(this), { priority: 55 });
  }

  // ── Plan 制定与确认: before_prompt_build（有 task 时）──
  _registerPlanning() {
    if (!this.planningEnabled) return;
    // planning 逻辑已合并到 onBeforePromptBuild，priority 55 统一处理
  }

  // ── 监控: llm_output ──
  _registerMonitoring() {
    if (!this.monitoringEnabled) return;
    this.api.on('llm_output', this.onLlmOutput.bind(this));
  }

  // ── 清理: agent_end ──
  _registerCleanup() {
    this.api.on('agent_end', this.onAgentEnd.bind(this));
  }

  async _getTask(runId) {
    return this.stateAdapter.getTask(runId);
  }

  async _saveTask(task) {
    task.updatedAt = getNow();
    await this.stateAdapter.saveTask(task.runId, task);
  }

  async _createTask(runId, prompt) {
    const planTemplate = generatePlan(prompt);
    const phases = assignSessionsToPhases(planTemplate.execution.phases, prompt);
    const task = {
      runId,
      status: 'draft',
      createdAt: getNow(),
      updatedAt: getNow(),
      plan: {
        prompt: prompt.slice(0, 500),
        createdAt: Date.now(),
        context: planTemplate.context,
        workspace: planTemplate.workspace,
        execution: {
          phases,
          currentPhase: 0
        }
      },
      event: { status: 'draft', deviations: [], attributions: [], planRevisions: [], outcome: {} },
      sessionIds: [],
      tools: []
    };
    await this._saveTask(task);
    this.logger.debug(`[Meta] Task 创建[draft]: ${phases.length} 阶段`);
    return task;
  }

  /**
   * before_prompt_build 逻辑：
   * 1. 无 task → 注入 assessment skill（Agent 评估 + 询问用户）
   * 2. task=draft → 注入 planning skill（制定 Plan）
   * 3. task=pending_approval → 注入 planning skill（处理用户反馈）
   * 4. task=active → 注入执行上下文 + monitoring
   */
  async onBeforePromptBuild(event, ctx) {
    const runId = ctx.runId;
    if (!runId) return;

    const task = await this._getTask(runId);

    // ── 阶段一：无 task → 注入 assessment skill ──
    if (!task) {
      const assessmentSkill = await this.skillLoader.load('assessment');
      if (!assessmentSkill) return;
      this.logger.debug(`[Meta] 注入 assessment skill: runId=${runId}`);
      return {
        prependSystemContext: `${assessmentSkill}\n\n【当前状态】本次会话尚无 task。请根据上方 assessment skill 评估用户任务复杂度，决定是否需要制定 Plan。\n`
      };
    }

    // ── 阶段二：根据 task.status 注入不同的 skill ──
    const planningSkill = await this.skillLoader.load('planning');

    if (task.status === 'draft') {
      return this._buildDraftContext(planningSkill, task.plan);
    }

    if (task.status === 'pending_approval') {
      return this._buildPendingApprovalContext(planningSkill, task.plan);
    }

    if (task.status === 'active') {
      return this._buildExecutionContext(task.plan);
    }

    return null;
  }

  _buildDraftContext(planningSkill, plan) {
    const { execution, workspace } = plan;
    const assignedSessions = execution.phases.filter(ph => ph.sessionId).length;

    const draftContext = `
【Plan 状态】draft — 需制定并汇报

【可用上下文】
- 阶段总数：${execution.phases.length}，已分配任务空间：${assignedSessions}
- 当前状态：status = "draft"，currentPhase = 0
- 可用工具：${workspace.tools.join(' / ') || '无'}

【执行指导】
1. 载入 ~/.openclaw/workspace/{agent}/MEMORY.md 中的条件-行动规则
2. 检查「活跃会话清单」，判断是否需要复用现有会话
3. 制定完整 Plan 后向用户汇报，等待确认
4. 汇报完成后，通知插件将 status 更新为 "pending_approval"
`;

    return {
      prependSystemContext: `${planningSkill}\n${draftContext}`
    };
  }

  _buildPendingApprovalContext(planningSkill, plan) {
    const pendingContext = `
【Plan 待确认 - 处理用户反馈】

当前 Plan 状态：pending_approval（等待用户确认）

【Agent 职责 - 必做】
1. 读取用户反馈内容
2. 如果用户确认（"确认"、"可以"、"开始执行"等）：
   - 将 task.status 更新为 "active"
   - 开始按 phases 执行
3. 如果用户要求修改：
   - 修改 task.plan.context / task.plan.execution.phases
   - 重新向用户汇报修改后的 Plan
   - 保持 task.status 为 "pending_approval"
4. 如果用户取消任务：
   - 将 task.status 更新为 "completed"
   - 说明取消原因
`;

    return {
      prependSystemContext: `${planningSkill}\n${pendingContext}`
    };
  }

  _buildExecutionContext(plan) {
    const { execution, workspace } = plan;
    const currentPhase = execution.phases[execution.currentPhase];
    const completedCount = execution.phases.filter(ph => ph.status === 'completed').length;

    let phaseInfo = '';
    if (currentPhase) {
      const sessionHint = currentPhase.sessionId
        ? `，分配会话：${currentPhase.sessionId}`
        : '';
      phaseInfo = `当前阶段：${execution.currentPhase + 1}/${execution.phases.length}（ID: ${currentPhase.id}）${sessionHint}`;
    } else {
      phaseInfo = '所有阶段已完成';
    }

    const execContext = `
【Plan 状态】active — 按阶段推进

【当前上下文】
- ${phaseInfo}
- 已完成阶段：${completedCount} 个
- 已产出物数量：${workspace.artifacts.length}

【执行指导】
1. 当前阶段已确认，按目标推进
2. 阶段完成后通知插件：phase.status = "completed"，currentPhase++
3. 产出物追加到 task.plan.workspace.artifacts
4. 如需调节 Plan，先说明理由并通知插件更新
`;

    return {
      prependSystemContext: execContext
    };
  }

  /**
   * llm_output：
   * 1. 检测 [NEED_PLAN] 标记 → 创建 task → 注入 planning skill
   * 2. task=active → 注入 monitoring skill
   */
  async onLlmOutput(event, ctx) {
    const runId = ctx.runId;
    if (!runId) return;

    const output = event.output || event.text || '';

    // ── 检测 [NEED_PLAN] 标记 ──
    const needPlan = output.includes('[NEED_PLAN]');
    let task = await this._getTask(runId);

    if (needPlan && !task) {
      const prompt = event.prompt || '';
      task = await this._createTask(runId, prompt);

      // 注入 planning skill，让 Agent 在同一次回复中继续制定 Plan
      const planningSkill = await this.skillLoader.load('planning');
      if (planningSkill) {
        const draftContext = this._buildDraftContext(planningSkill, task.plan);
        this.logger.debug(`[Meta] 检测到 [NEED_PLAN]，创建 task 并注入 planning skill: runId=${runId}`);
        return draftContext;
      }
    }

    // ── 保存 output 到 task（如果 task 存在）──
    if (task) {
      task.plan = task.plan || {};
      task.plan.output = output;
      await this._saveTask(task);
    }

    // ── task=active → 注入 monitoring skill ──
    if (task && task.status === 'active') {
      const monitoringSkill = await this.skillLoader.load('monitoring');
      if (!monitoringSkill) return;

      const currentPhase = task.plan.execution?.phases?.[task.plan.execution?.currentPhase];
      const phaseHint = currentPhase
        ? `当前阶段：${currentPhase.id}，分配会话：${currentPhase.sessionId || '无'}`
        : '所有阶段已完成';

      return {
        prependSystemContext: `${monitoringSkill}\n\n【监控上下文】${phaseHint}\n\n【Agent 职责】请根据上方 monitoring skill 检查当前输出是否与 Plan 一致。关注：阶段目标是否达成、产出物是否完整、任务空间是否正常推进。\n`
      };
    }
  }

  async onAgentEnd(event, ctx) {
    const runId = ctx.runId;
    if (!runId) return;
    const task = await this.stateAdapter.getTask(runId);
    if (task) {
      task.status = 'completed';
      await this._saveTask(task);
    }
    this.logger.debug(`[Meta] 任务状态更新为 completed: runId=${runId}`);
  }
}
