/**
 * Deviation — 偏差对象
 * 记录代理对任务执行与 Plan 之间偏差的认知
 */

export class Deviation {
  constructor({ runId, phaseId, expected, actual, gap }) {
    this.runId = runId;
    this.phaseId = phaseId;
    this.expected = expected;      // 预期结果
    this.actual = actual;          // 实际结果
    this.gap = gap;                // 差距描述
    this.status = 'detected';      // detected | acknowledged | resolved
    this.createdAt = Date.now();
    this.acknowledgedAt = null;
    this.resolvedAt = null;
    this.agentAcknowledgment = null;
    this.resolution = null;
  }

  acknowledge(agentAcknowledgment) {
    this.status = 'acknowledged';
    this.acknowledgedAt = Date.now();
    this.agentAcknowledgment = agentAcknowledgment;
  }

  resolve(resolution) {
    this.status = 'resolved';
    this.resolvedAt = Date.now();
    this.resolution = resolution;
  }
}
