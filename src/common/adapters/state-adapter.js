/**
 * StateAdapter — 状态存储适配器
 * 隔离核心 State API 变化，提供统一接口
 */

export class StateAdapter {
  constructor(stateAPI) {
    this.state = stateAPI;
  }

  async transaction(operations) {
    return this.state.transaction(operations);
  }

  async savePlan(runId, plan) {
    await this.state.set(`plan:${runId}`, plan);
  }

  async getPlan(runId) {
    return this.state.get(`plan:${runId}`);
  }

  async saveSession(sessionId, session) {
    await this.state.set(`session:${sessionId}`, session);
  }

  async getSession(sessionId) {
    return this.state.get(`session:${sessionId}`);
  }

  async deleteSession(sessionId) {
    await this.state.set(`session:${sessionId}`, null);
  }
}
