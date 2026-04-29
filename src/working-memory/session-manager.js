/**
 * SessionManager — 会话管理器
 * 组合 StateAdapter + TaskFlowAdapter + Session API，管理任务空间复用
 */

export class SessionManager {
  constructor(state, taskFlow, sessionAPI) {
    this.state = state;
    this.taskFlow = taskFlow;
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

    const existing = await this.state.getSession(sessionId);
    if (existing && existing.status === 'idle') {
      existing.status = 'active';
      await this.state.saveSession(sessionId, existing);
      return existing;
    }

    const session = {
      id: sessionId,
      taskFamily,
      status: 'active',
      createdAt: Date.now()
    };

    await this.state.saveSession(sessionId, session);
    await this.sessionAPI.create(sessionId, session);

    const flow = await this.taskFlow.getByPhase(phase.id);
    if (flow) {
      await this.taskFlow.runSubtask(flow.flowId, phase);
    }

    return session;
  }

  async releaseSession(sessionId) {
    const session = await this.state.getSession(sessionId);
    if (session) {
      session.status = 'idle';
      await this.state.saveSession(sessionId, session);
      await this.sessionAPI.update(sessionId, { status: 'idle' });
    }
  }

  async destroySession(sessionId) {
    await this.state.deleteSession(sessionId);
    await this.sessionAPI.destroy(sessionId);
  }
}
