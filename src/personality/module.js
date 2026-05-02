/**
 * 人格模块 —— 面向对象封装
 *
 * 插件职责：在 agent_end 时读取 task JSON，注入 development skill 指导人格更新
 * Agent 职责：自行阅读 skill、判断同化/顺应、决定是否更新人格文件
 *
 * 核心原则：Plugin asks, Agent decides, Plugin records
 */

export class PersonalityModule {
  constructor({ api, config, stateAdapter, skillLoader, logger }) {
    this.api = api;
    this.config = config || {};
    this.stateAdapter = stateAdapter;
    this.skillLoader = skillLoader;
    this.logger = logger;
    this.enabled = this.config.enabled !== false;
  }

  /**
   * 注册人格模块相关的 hooks
   */
  register() {
    if (!this.enabled) {
      this.logger.info('[Personality] 人格模块已禁用');
      return;
    }

    this.logger.info('[Personality] 注册人格模块 Hook');
    this.api.on('agent_end', this.onAgentEnd.bind(this), { priority: 30 });
  }

  /**
   * agent_end 时：读取 task JSON 的 event，注入 development skill 指导人格更新
   */
  async onAgentEnd(event, ctx) {
    const runId = ctx.runId;
    if (!runId) return;

    const task = await this.stateAdapter.getTask(runId);
    if (!task || !task.event || task.event.status !== 'completed') {
      this.logger.debug(`[Personality] runId=${runId} 无 completed event，跳过人格更新`);
      return;
    }

    const developmentSkill = await this.skillLoader.load('development');
    if (!developmentSkill) {
      this.logger.warn('[Personality] development skill 未找到');
      return;
    }

    const eventSummary = {
      deviations: task.event.deviations || [],
      attributions: task.event.attributions || [],
      planRevisions: task.event.planRevisions || [],
      outcome: task.event.outcome || {}
    };

    return {
      prependSystemContext: `${developmentSkill}\n\n【任务回顾】本次运行（${runId}）已完成。\n【Event 摘要】\n- 偏差记录：${eventSummary.deviations.length} 条\n- 归因记录：${eventSummary.attributions.length} 条\n- 计划修订：${eventSummary.planRevisions.length} 次\n【Agent 职责】请根据上方 development skill，分析本次任务经验对 6 个维度的影响（自我、风格、信念、身份、技能、程序性记忆），自行决定是否需要更新人格文件。\n`
    };
  }
}
