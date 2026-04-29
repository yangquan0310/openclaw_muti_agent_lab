/**
 * Regulator — 调节对象
 * 接收 Monitor 对象的偏差报告，分析根因，生成并执行调节方案
 */

export class Regulator {
  constructor({ runId, monitor }) {
    this.runId = runId;
    this.monitor = monitor;
    this.deviationType = null;
    this.deviationDetails = null;
    this.adjustmentPlan = null;
    this.status = 'idle';
  }

  /**
   * 接收偏差报告，进入 analyzing 状态
   */
  receive(deviation) {
    this.deviationType = deviation.type;
    this.deviationDetails = deviation;
    this.status = 'analyzing';
  }

  /**
   * 分析根因并生成调节方案
   */
  analyze(plan, sessions) {
    const strategy = this._selectStrategy(this.deviationType);
    this.adjustmentPlan = {
      strategy,
      actions: this._generateActions(strategy, plan, sessions),
      reason: this.deviationDetails?.message || ''
    };
    this.status = 'executing';
    return this.adjustmentPlan;
  }

  /**
   * 执行调节方案：修改 Plan 和 Session
   */
  execute(plan, sessionManager) {
    const actions = this.adjustmentPlan?.actions || [];

    for (const action of actions) {
      switch (action.type) {
        case 'update_plan':
          // 修改 Plan 对象
          Object.assign(plan, action.changes);
          break;
        case 'pause_session':
          // 暂停指定 Session
          sessionManager?.releaseSession(action.sessionId);
          break;
        case 'resume_session':
          // 恢复指定 Session
          // sessionManager?.createSession(...);
          break;
        case 'skip_phase':
          // 跳过当前阶段
          plan.execution.currentPhase++;
          break;
        default:
          // unknown action
      }
    }

    this.status = 'completed';
    return { success: true, actionsTaken: actions.length };
  }

  /**
   * 返回 Monitor 继续追踪
   */
  complete() {
    this.status = 'completed';
    this.monitor?.resolved();
  }

  /**
   * 销毁 Regulator
   */
  destroy() {
    this.status = 'destroyed';
    this.adjustmentPlan = null;
    this.deviationDetails = null;
  }

  _selectStrategy(deviationType) {
    const strategies = {
      goal_deviation: 'realign',
      incomplete_output: 'extend',
      progress_delay: 'parallelize',
      resource_exhausted: 'substitute'
    };
    return strategies[deviationType] || 'realign';
  }

  _generateActions(strategy, plan, sessions) {
    // TODO: 根据策略生成具体的调节动作
    return [{ type: 'notify', message: `调节策略: ${strategy}` }];
  }
}
