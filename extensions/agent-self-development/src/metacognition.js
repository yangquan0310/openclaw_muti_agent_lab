/**
 * 元认知模块 —— 面向对象封装
 *
 * 插件职责：在合适的时机将对应的 skill 文档注入 Agent 的 system context
 * Agent 职责：自行阅读 skill、判断偏差、决定是否 revise
 *
 * Plan 状态机：
 *   draft → pending_approval → active → completed → destroyed
 *   ├─ draft: 生成 Plan，Agent 制定并汇报
 *   ├─ pending_approval: 等待用户确认（Agent 处理反馈）
 *   ├─ active: 用户确认后按 phases 执行
 *   └─ completed: 所有 phases 完成
 */

import { generatePlan, assignSessionsToPhases } from './utils.js';

export class MetacognitionModule {
  constructor({ api, config, state, skillLoader, logger }) {
    this.api = api;
    this.config = config || {};
    this.state = state;
    this.skillLoader = skillLoader;
    this.logger = logger;
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

    let plan = await this.state.get(`plan:${runId}`);

    // ── 阶段一：Plan 不存在，生成新 Plan ──
    if (!plan) {
      const planTemplate = generatePlan(prompt);
      const phases = assignSessionsToPhases(planTemplate.execution.phases, prompt);
      plan = {
        runId,
        prompt: prompt.slice(0, 500),
        createdAt: Date.now(),
        status: 'draft',
        context: planTemplate.context,
        workspace: planTemplate.workspace,
        execution: {
          phases,
          currentPhase: 0
        }
      };
      await this.state.set(`plan:${runId}`, plan);
      this.logger.debug(`[Meta] Plan 生成[${plan.status}]: ${phases.length} 阶段`);
    }

    // ── 阶段二：根据 Plan.status 注入不同的 skill ──
    const planningSkill = await this.skillLoader.load('planning');

    if (plan.status === 'draft') {
      // Agent 需要制定完整 Plan 并向用户汇报
      return this._buildDraftContext(planningSkill, plan);
    }

    if (plan.status === 'pending_approval') {
      // Agent 需要处理用户的确认/修改反馈
      return this._buildPendingApprovalContext(planningSkill, plan);
    }

    if (plan.status === 'active') {
      // 计划已确认，注入执行上下文帮助 Agent 继续执行
      return this._buildExecutionContext(plan);
    }

    // completed 或其他状态，不注入
    return null;
  }

  /**
   * draft 状态：要求 Agent 制定 Plan 并向用户汇报
   */
  _buildDraftContext(planningSkill, plan) {
    const { context, execution } = plan;
    const phaseLines = execution.phases.map((ph, i) => {
      const sessionHint = ph.sessionId ? ` [任务空间: ${ph.sessionId}]` : '';
      return `  ${i + 1}. ${ph.name} — ${ph.goal}${sessionHint}`;
    }).join('\n');

    const draftContext = `
【Plan 草稿 - 请制定并汇报】

▸ 用户任务：${plan.prompt.slice(0, 200)}

▸ 建议上下文（可参考，也可根据实际调整）：
  目标：${context.goal}
  约束：${context.constraints.join(' / ')}
  验收：${context.successCriteria.join(' / ')}

▸ 个人记忆配置：
  制定 Plan 前，请加载 ${'`'}memory.md${'`'} 中的条件-行动规则。
  若用户任务满足某条规则的条件，请在 Plan 中执行对应的行动（添加约束、阶段、验收标准等）。

▸ 建议阶段（可参考，可增删改）：
${phaseLines}

【Agent 职责 - 必做】
1. 根据上方 planning skill、用户任务和个人记忆配置（memory.md 条件-行动规则），制定完整 Plan
2. 向用户汇报 Plan 内容（目标、阶段、任务空间分配、验收标准）
3. 明确告知用户"计划已制定，请确认或提出修改意见"
4. 汇报完成后，将 Plan.status 更新为 "pending_approval"
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
   - 将 Plan.status 更新为 "active"
   - 开始按 phases 执行
3. 如果用户要求修改：
   - 修改 Plan.context / Plan.execution.phases
   - 重新向用户汇报修改后的 Plan
   - 保持 Plan.status 为 "pending_approval"
4. 如果用户取消任务：
   - 将 Plan.status 更新为 "completed"
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
    const { context, execution, workspace } = plan;
    const currentPhase = execution.phases[execution.currentPhase];

    let phaseInfo = '';
    if (currentPhase) {
      const sessionHint = currentPhase.sessionId
        ? `（任务空间: ${currentPhase.sessionId}）`
        : '';
      phaseInfo = `
▸ 当前阶段 (${execution.currentPhase + 1}/${execution.phases.length})：
  名称：${currentPhase.name}
  目标：${currentPhase.goal}
  状态：${currentPhase.status}
  ${sessionHint}
  预期产出：${currentPhase.outputs.join(' / ') || '无'}
`;
    } else {
      phaseInfo = '\n▸ 所有阶段已完成\n';
    }

    const execContext = `
【执行上下文 - 继续推进】

▸ 任务目标：${context.goal}
▸ 验收标准：${context.successCriteria.join(' / ')}
${phaseInfo}
▸ 已产出：${workspace.artifacts.join(' / ') || '无'}

【Agent 职责】
1. 按当前阶段目标推进任务
2. 阶段完成后更新 phase.status = "completed"，currentPhase++
3. 产出物记录到 workspace.artifacts
4. 如需调节 Plan（跳过阶段、新增阶段等），先说明理由并更新 Plan
`;

    return {
      prependSystemContext: execContext
    };
  }

  /**
   * llm_output：仅在 Plan active 时注入 monitoring skill
   */
  async onLlmOutput(event, ctx) {
    const runId = ctx.runId;
    if (!runId) return;

    const output = event.output || event.text || '';
    await this.state.set(`output:${runId}`, output);

    const plan = await this.state.get(`plan:${runId}`);
    if (!plan || plan.status !== 'active') return;

    const monitoringSkill = await this.skillLoader.load('monitoring');
    if (!monitoringSkill) return;

    const currentPhase = plan.execution.phases[plan.execution.currentPhase];
    const phaseHint = currentPhase
      ? `当前阶段：${currentPhase.name}（${currentPhase.goal}）`
      : '所有阶段已完成';

    return {
      prependSystemContext: `${monitoringSkill}\n\n【监控上下文】${phaseHint}\n\n【Agent 职责】请根据上方 monitoring skill 检查当前输出是否与 Plan 一致。关注：阶段目标是否达成、产出物是否完整、任务空间是否正常推进。\n`
    };
  }

  async onAgentEnd(event, ctx) {
    const runId = ctx.runId;
    if (!runId) return;
    await this.state.set(`plan:${runId}`, null);
    await this.state.set(`output:${runId}`, null);
    this.logger.debug(`[Meta] 清理状态: runId=${runId}`);
  }

  _shouldUseMetacognition(prompt) {
    const simplePatterns = [
      /^(查询|搜索|查找|什么是|怎么|如何)/i,
      /^(现在几点|今天日期|天气)/i
    ];
    return !simplePatterns.some(p => p.test(prompt.trim()));
  }
}
