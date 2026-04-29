/**
 * DeviationManager — 偏差认知业务逻辑
 * 在 monitoring 阶段管理 Deviation 对象的生命周期
 */

export class DeviationManager {
  constructor(stateAdapter) {
    this.stateAdapter = stateAdapter;
  }

  /**
   * 创建新的偏差记录
   */
  async createDeviation(runId, phaseId, deviationData) {
    const deviation = {
      runId,
      phaseId,
      status: 'detected',
      createdAt: Date.now(),
      ...deviationData
    };
    await this.stateAdapter.saveDeviation(runId, phaseId, deviation);
    return deviation;
  }

  /**
   * 代理确认偏差后更新状态
   */
  async acknowledgeDeviation(runId, phaseId, agentAcknowledgment) {
    const deviation = await this.stateAdapter.getDeviation(runId, phaseId);
    if (!deviation) return null;

    deviation.status = 'acknowledged';
    deviation.acknowledgedAt = Date.now();
    deviation.agentAcknowledgment = agentAcknowledgment;

    await this.stateAdapter.saveDeviation(runId, phaseId, deviation);
    return deviation;
  }

  /**
   * 偏差已解决
   */
  async resolveDeviation(runId, phaseId, resolution) {
    const deviation = await this.stateAdapter.getDeviation(runId, phaseId);
    if (!deviation) return null;

    deviation.status = 'resolved';
    deviation.resolvedAt = Date.now();
    deviation.resolution = resolution;

    await this.stateAdapter.saveDeviation(runId, phaseId, deviation);
    return deviation;
  }

  /**
   * 获取当前 run 的所有偏差
   */
  async listDeviations(runId) {
    return this.stateAdapter.listDeviationsByRunId(runId);
  }
}
