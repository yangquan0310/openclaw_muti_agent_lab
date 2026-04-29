/**
 * Monitor — 监控对象
 * 跟踪 Agent 输出与 Plan 的偏离程度，检测偏差并触发调节
 */

export class Monitor {
  constructor({ runId, targetPlan }) {
    this.runId = runId;
    this.targetPlan = targetPlan;
    this.lastOutput = '';
    this.deviationFlags = [];
    this.status = 'idle';
  }

  /**
   * 记录最新 LLM 输出，进入 tracking 状态
   */
  recordOutput(output) {
    this.lastOutput = output;
    this.status = 'tracking';
  }

  /**
   * 检查当前输出是否与 Plan 偏离
   * @returns {object|null} 偏差信息或 null
   */
  check(plan, currentPhase) {
    const deviations = [];

    // 检查1：是否偏离当前阶段目标
    if (currentPhase && !this._matchesPhaseGoal(this.lastOutput, currentPhase)) {
      deviations.push({
        type: 'goal_deviation',
        severity: 'medium',
        message: `输出偏离阶段目标: ${currentPhase.goal}`
      });
    }

    // 检查2：产出物是否完整
    if (currentPhase && !this._hasRequiredOutputs(this.lastOutput, currentPhase.outputs)) {
      deviations.push({
        type: 'incomplete_output',
        severity: 'low',
        message: `缺少预期产出: ${currentPhase.outputs.join(', ')}`
      });
    }

    // 检查3：进度偏差（由外部调用方传入进度信息）
    // 检查4：时间消耗

    if (deviations.length > 0) {
      this.deviationFlags = deviations;
      this.status = 'alert';
      return deviations;
    }

    return null;
  }

  /**
   * 偏差已处理，返回 tracking 状态
   */
  resolved() {
    this.deviationFlags = [];
    this.status = 'tracking';
  }

  /**
   * 销毁 Monitor
   */
  destroy() {
    this.status = 'destroyed';
    this.lastOutput = '';
    this.deviationFlags = [];
  }

  _matchesPhaseGoal(output, phase) {
    // TODO: 实现更精确的匹配逻辑
    return output.length > 0;
  }

  _hasRequiredOutputs(output, requiredOutputs) {
    // TODO: 检查输出中是否包含必需的产出物引用
    return true;
  }
}
