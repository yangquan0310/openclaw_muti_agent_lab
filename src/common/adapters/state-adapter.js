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

  // Plan
  async savePlan(runId, plan) {
    await this.state.set(`plan:${runId}`, plan);
  }

  async getPlan(runId) {
    return this.state.get(`plan:${runId}`);
  }

  // Session
  async saveSession(sessionId, session) {
    await this.state.set(`session:${sessionId}`, session);
  }

  async getSession(sessionId) {
    return this.state.get(`session:${sessionId}`);
  }

  async deleteSession(sessionId) {
    await this.state.set(`session:${sessionId}`, null);
  }

  // Deviation
  async saveDeviation(runId, phaseId, deviation) {
    await this.state.set(`deviation:${runId}:${phaseId}`, deviation);
  }

  async getDeviation(runId, phaseId) {
    return this.state.get(`deviation:${runId}:${phaseId}`);
  }

  async listDeviationsByRunId(runId) {
    const keys = await this.state.keys?.() || [];
    const prefix = `deviation:${runId}:`;
    const deviationKeys = keys.filter(k => k.startsWith(prefix));
    const deviations = await Promise.all(
      deviationKeys.map(k => this.state.get(k))
    );
    return deviations.filter(Boolean);
  }

  // Attribution
  async saveAttribution(runId, deviationId, attribution) {
    await this.state.set(`attribution:${runId}:${deviationId}`, attribution);
  }

  async getAttribution(runId, deviationId) {
    return this.state.get(`attribution:${runId}:${deviationId}`);
  }

  // Event（临时存储，agent_end 时转移到 Memory）
  async saveEvent(eventId, event) {
    await this.state.set(`event:${eventId}`, event);
  }

  async getEvent(eventId) {
    return this.state.get(`event:${eventId}`);
  }

  async deleteEvent(eventId) {
    await this.state.set(`event:${eventId}`, null);
  }

  async listEvents() {
    const keys = await this.state.keys?.() || [];
    const eventKeys = keys.filter(k => k.startsWith('event:'));
    const events = await Promise.all(
      eventKeys.map(k => this.state.get(k))
    );
    return events.filter(Boolean);
  }
}
