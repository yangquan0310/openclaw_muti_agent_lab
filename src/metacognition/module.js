/**
 * 元认知模块 —— 面向对象封装
 *
 * 插件职责：在合适的时机将对应的 skill 文档注入 Agent 的 system context
 * Agent 职责：自行阅读 skill、判断偏差、决定是否 revise
 *
 * Plan 状态机：
 *   draft → pending_approval → active → completed
 *   ├─ draft: 生成 Plan，Agent 制定并汇报
 *   ├─ pending_approval: 等待用户确认（Agent 处理反馈）
 *   └─ active: 用户确认后按 phases 执行
 *
 * 数据统一存储在 task:{runId} JSON 中，不再使用独立的 plan.json
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
    this.planningEnabled = this.enabled && this.config.planning !== false;
    this.monitoringEnabled = this.enabled && this.config.monitoring !== false;
  }

  register() {
    if (!this.enabled) {
      this.logger.info('[Meta] 元认知模块已禁用');
      return;
    }

    this.logger.info('[Meta] 注册元认知 Hooks');
    this._registerPlanning();
    this._registerMonitoring();
    this._registerCleanup();
  }

  _registerPlanning() {
    if (!this.planningEnabled) return;
    this.api.on('before_prompt_build', this.onBeforePromptBuild.bind(this), { priority: 50 });
  }

  _registerMonitoring() {
    if (!this.monitoringEnabled) return;
    this.api.on('llm_output', this.onLlmOutput.bind(this));
  }

  _registerCleanup() {
    this.api.on('agent_end', this.onAgentEnd.bind(this));
  }

  /**
   * 获取或创建 task JSON（统一存储）
   */
  async _getOrCreateTask(runId) {
    let task = await this.stateAdapter.getTask(runId);
    if (!task) {
      task = {
        runId,
        status: 'draft',
        createdAt: getNow(),
        updatedAt: getNow(),
        plan: {},
        event: { status: 'draft', deviations: [], attributions: [], planRevisions: [], outcome: {} },
        sessionIds: [],
        tools: []
      };
    }
    return task;
  }

  async _saveTask(task) {
    task.updatedAt = getNow();
    await this.stateAdapter.saveTask(task.runId, task);
  }

  /**
   * before_prompt_build 三阶段逻辑：
   * 1. draft / null → 注入 planning skill，要求制定 Plan 并汇报
   * 2. pending_approval → 注入 planning skill，处理用户确认/修改
   * 3. active → 注入执行上下文 + monitoring
   */
  async onBeforePromptBuild(event, ctx) {
    const runId = ctx.runId;
    if (!runId) return;

    const prompt = event.prompt || '';
    if (!this._shouldUseMetacognition(prompt)) {
      this.logger.debug(`[Meta] 简单任务，跳过计划: ${prompt.slice(0, 50)}`);
      return;
    }

    let task = await this._getOrCreateTask(runId);

    // ── 阶段一：Plan 不存在，生成新 Plan ──
    if (!task.plan || !task.plan.execution) {
      const planTemplate = generatePlan(prompt);
      const phases = assignSessionsToPhases(planTemplate.execution.phases, prompt);
      task.plan = {
        prompt: prompt.slice(0, 500),
        createdAt: Date.now(),
        context: planTemplate.context,
        workspace: planTemplate.workspace,
        execution: {
          phases,
          currentPhase: 0
        }
      };
      task.status = 'draft';
      await this._saveTask(task);
      this.logger.debug(`[Meta] Plan 生成[draft]: ${phases.length} 阶段`);
    }

    const plan = task.plan;

    // ── 阶段二：根据 task.status 注入不同的 skill ──
    const planningSkill = await this.skillLoader.load('planning');

    if (task.status === 'draft') {
      return this._buildDraftContext(planningSkill, plan);
    }

    if (task.status === 'pending_approval') {
      return this._buildPendingApprovalContext(planningSkill, plan);
    }

    if (task.status === 'active') {
      return this._buildExecutionContext(plan);
    }

    // completed 或其他状态，不注入
    return null;
  }

  /**
   * draft 状态：要求 Agent 制定 Plan 并向用户汇报
   */
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

  /**
   * pending_approval 状态：处理用户确认/修改
   */
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

  /**
   * active 状态：注入执行上下文
   */
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
   * llm_output：仅在 task.status === 'active' 时注入 monitoring skill
   */
  async onLlmOutput(event, ctx) {
    const runId = ctx.runId;
    if (!runId) return;

    const output = event.output || event.text || '';

    const task = await this._getOrCreateTask(runId);
    task.plan = task.plan || {};
    task.plan.output = output;
    await this._saveTask(task);

    if (task.status !== 'active') return;

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

  _shouldUseMetacognition(prompt) {
    const simplePatterns = [
      /^(查询|搜索|查找|什么是|怎么|如何)/i,
      /^(现在几点|今天日期|天气)/i
    ];
    return !simplePatterns.some(p => p.test(prompt.trim()));
  }
}
