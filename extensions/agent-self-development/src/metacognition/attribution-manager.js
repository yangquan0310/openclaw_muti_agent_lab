/**
 * AttributionManager — 归因调节业务逻辑
 * 在 regulation 阶段管理 Attribution 对象的生命周期
 */

export class AttributionManager {
  constructor(stateAdapter, flowAdapter) {
    this.stateAdapter = stateAdapter;
    this.flowAdapter = flowAdapter;
  }

  /**
   * 创建归因分析
   */
  async analyzeAttribution(runId, deviationId, attributionData) {
    const attribution = {
      runId,
      deviationId,
      status: 'analyzing',
      createdAt: Date.now(),
      ...attributionData
    };
    await this.stateAdapter.saveAttribution(runId, deviationId, attribution);
    return attribution;
  }

  /**
   * 完成归因分析
   */
  async completeAttribution(runId, deviationId, rootCause, adjustmentPlan) {
    const attribution = await this.stateAdapter.getAttribution(runId, deviationId);
    if (!attribution) return null;

    attribution.status = 'completed';
    attribution.completedAt = Date.now();
    attribution.rootCause = rootCause;
    attribution.adjustmentPlan = adjustmentPlan;

    await this.stateAdapter.saveAttribution(runId, deviationId, attribution);
    return attribution;
  }

  /**
   * 执行调节方案
   */
  async applyAdjustment(runId, deviationId, executionResult) {
    const attribution = await this.stateAdapter.getAttribution(runId, deviationId);
    if (!attribution) return null;

    attribution.status = 'executed';
    attribution.executedAt = Date.now();
    attribution.executionResult = executionResult;

    await this.stateAdapter.saveAttribution(runId, deviationId, attribution);
    return attribution;
  }
}
