/**
 * SessionManager — 会话管理器
 * 组合 StateAdapter + FlowAdapter + Session API，管理任务空间复用
 */

export class SessionManager {
  constructor(stateAdapter, flowAdapter, sessionAPI) {
    this.stateAdapter = stateAdapter;
    this.flowAdapter = flowAdapter;
    this.sessionAPI = sessionAPI;
  }

  async createSession(phase, taskFamily) {
    const sessionId = `session:${taskFamily}:${taskFamily}`;

    const existingSession = await this.sessionAPI.get(sessionId);
    if (existingSession && existingSession.status === 'idle') {
      existingSession.status = 'active';
      await this.sessionAPI.update(sessionId, existingSession);
      return existingSession;
    }

    const existing = await this.stateAdapter.getSession(sessionId);
    if (existing && existing.status === 'idle') {
      existing.status = 'active';
      await this.stateAdapter.saveSession(sessionId, existing);
      return existing;
    }

    const session = {
      id: sessionId,
      taskFamily,
      status: 'active',
      createdAt: Date.now()
    };

    await this.stateAdapter.saveSession(sessionId, session);
    await this.sessionAPI.create(sessionId, session);

    const flow = await this.flowAdapter.getByPhase(phase.id);
    if (flow) {
      await this.flowAdapter.runSubtask(flow.flowId, phase);
    }

    return session;
  }

  async releaseSession(sessionId) {
    const session = await this.stateAdapter.getSession(sessionId);
    if (session) {
      session.status = 'idle';
      await this.stateAdapter.saveSession(sessionId, session);
      await this.sessionAPI.update(sessionId, { status: 'idle' });
    }
  }

  async destroySession(sessionId) {
    await this.stateAdapter.deleteSession(sessionId);
    await this.sessionAPI.destroy(sessionId);
  }
}
