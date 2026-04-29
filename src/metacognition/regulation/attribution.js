/**
 * Attribution — 归因对象
 * 记录代理对偏差根因的分析和调节方案
 */

export class Attribution {
  constructor({ runId, deviationId, rootCause, adjustmentPlan }) {
    this.runId = runId;
    this.deviationId = deviationId;
    this.rootCause = rootCause;           // 根因分析
    this.adjustmentPlan = adjustmentPlan; // 调节方案
    this.status = 'analyzing';            // analyzing | completed | executed
    this.createdAt = Date.now();
    this.completedAt = null;
    this.executedAt = null;
    this.executionResult = null;
  }

  complete(rootCause, adjustmentPlan) {
    this.status = 'completed';
    this.completedAt = Date.now();
    this.rootCause = rootCause;
    this.adjustmentPlan = adjustmentPlan;
  }

  execute(executionResult) {
    this.status = 'executed';
    this.executedAt = Date.now();
    this.executionResult = executionResult;
  }
}
