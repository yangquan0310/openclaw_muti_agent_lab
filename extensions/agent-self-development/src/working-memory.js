/**
 * 工作记忆模块 —— 面向对象封装
 *
 * 核心概念：
 * - 会话（Session）= 任务空间：执行特定任务的内存空间
 * - 同一任务族的 Agent 在同一会话中处理任务
 * - Agent 是软件，在任务空间中执行任务
 * - 支持并行：一个 Agent 可同时持有多个任务空间
 * - Memory Table 是任务空间的集中管理中心
 *
 * 插件职责：追踪任务空间生命周期，记录事件，在 agent_end 时更新任务空间状态
 * Agent 职责：自行阅读 skill、管理任务空间看板、决定复用/创建/销毁策略
 */

import { getToday, getNow, inferTaskFamily } from './utils.js';

export class WorkingMemoryModule {
  constructor({ api, config, state, skillLoader, logger }) {
    this.api = api;
    this.config = config || {};
    this.state = state;
    this.skillLoader = skillLoader;
    this.logger = logger;
    this.enabled = this.config.enabled !== false;
    this.trackSubagents = this.enabled && this.config.trackSubagents !== false;
    this.autoArchive = this.enabled && this.config.autoArchive !== false;
  }

  /**
   * 注册所有工作记忆相关的 hooks
   */
  register() {
    if (!this.enabled) {
      this.logger.info('[WM] 工作记忆模块已禁用');
      return;
    }

    this.logger.info('[WM] 注册工作记忆 Hooks');
    this._registerSessionTracking();
    this._registerToolResult();
    this._registerArchive();
  }

  // ── 任务空间追踪: before_tool_call ──
  _registerSessionTracking() {
    if (!this.trackSubagents) return;
    this.api.on('before_tool_call', this.onBeforeToolCall.bind(this));
  }

  // ── 工具结果记录: after_tool_call ──
  _registerToolResult() {
    this.api.on('after_tool_call', this.onAfterToolCall.bind(this));
  }

  // ── 归档与状态更新: agent_end ──
  _registerArchive() {
    if (!this.autoArchive) return;
    this.api.on('agent_end', this.onAgentEnd.bind(this));
  }

  /**
   * 追踪任务空间创建
   * 当 Agent 调用 agent/subagent/sessions_spawn 时，注册一个新的任务空间
   */
  async onBeforeToolCall(event, ctx) {
    const toolName = event.toolName;
    const isSpawnTool = toolName === 'sessions_spawn' || toolName === 'agent' || toolName === 'subagent';
    if (!isSpawnTool) return;

    const runId = ctx.runId;
    const sessionId = event.params?.id || event.params?.name || `sub-${Date.now()}`;
    const purpose = event.params?.purpose || event.params?.instruction || '';
    const taskFamily = inferTaskFamily(purpose);

    const entry = {
      type: 'subagent_spawn',
      sessionId,
      taskFamily,
      parentRunId: runId,
      purpose,
      model: event.params?.model || 'default',
      toolName,
      status: 'active',
      timestamp: getNow()
    };

    await this.state.append(`wm:${runId}:tools`, entry);
    await this.state.append(`session_list:${runId}`, {
      sessionId,
      taskFamily,
      role: event.params?.role || '助手',
      task: purpose,
      status: 'active',
      createdAt: getNow(),
      lastActive: getNow(),
      parentRunId: runId
    });

    // 更新全局活跃任务空间索引（Memory Table 管理中心）
    await this._updateActiveSession(sessionId, taskFamily, 'active');

    this.logger.debug(`[WM] 创建任务空间: ${sessionId} (taskFamily=${taskFamily}, parent=${runId})`);
  }

  /**
   * 记录工具错误和任务空间完成状态
   */
  async onAfterToolCall(event, ctx) {
    const runId = ctx.runId;
    const result = event.result;
    const toolName = event.toolName;

    const isError = result && (result.error || result.status === 'error');
    if (isError) {
      await this.state.append(`events:${getToday()}`, {
        time: getNow(),
        type: 'tool_error',
        runId,
        toolName,
        summary: String(result.error || 'unknown error').slice(0, 200)
      });
    }

    const isSpawnTool = toolName === 'sessions_spawn' || toolName === 'agent' || toolName === 'subagent';
    if (isSpawnTool) {
      const sessionId = event.params?.id || event.params?.name;
      const status = isError ? 'killed' : 'completed';

      await this.state.append(`wm:${runId}:tools`, {
        type: 'subagent_complete',
        sessionId,
        resultSummary: this.summarizeResult(result),
        status,
        timestamp: getNow()
      });

      // 更新本次运行中的任务空间状态
      const sessions = await this.state.get(`session_list:${runId}`, []);
      const updated = sessions.map(s =>
        s.sessionId === sessionId ? { ...s, status, lastActive: getNow() } : s
      );
      await this.state.set(`session_list:${runId}`, updated);

      // 同步更新全局活跃任务空间索引
      const taskFamily = sessions.find(s => s.sessionId === sessionId)?.taskFamily;
      if (taskFamily) {
        await this._updateActiveSession(sessionId, taskFamily, status);
      }
    }
  }

  /**
   * 归档 completed 任务空间，更新全局索引
   * - completed → 归档到 Memory Table + 标记为 idle（可复用）
   * - killed → 从全局索引移除
   * - paused → 保留在全局索引中
   */
  async onAgentEnd(event, ctx) {
    const runId = ctx.runId;
    if (!runId) return;

    const sessions = await this.state.get(`session_list:${runId}`, []);
    const completedSessions = sessions.filter(s => s.status === 'completed');
    const killedSessions = sessions.filter(s => s.status === 'killed');
    const pausedSessions = sessions.filter(s => s.status === 'paused');

    if (killedSessions.length > 0) {
      this.logger.debug(`[WM] 销毁 killed 任务空间: ${killedSessions.length}`);
    }
    if (pausedSessions.length > 0) {
      this.logger.debug(`[WM] 保留 paused 任务空间: ${pausedSessions.length}`);
    }

    // completed 任务空间：归档 + 标记为 idle（可复用）
    for (const session of completedSessions) {
      const archive = {
        runId,
        sessionId: session.sessionId,
        taskFamily: session.taskFamily,
        archivedAt: getNow(),
        task: session.task,
        role: session.role,
        status: 'completed',
        toolCount: (await this.state.get(`wm:${runId}:tools`, [])).filter(t => t.sessionId === session.sessionId).length
      };
      await this.state.append(`memory_table:${getToday()}`, archive);

      // 回到 idle 状态，供后续同任务族复用
      await this._updateActiveSession(session.sessionId, session.taskFamily, 'idle');
    }

    // killed 任务空间：从全局索引移除
    for (const session of killedSessions) {
      await this._removeActiveSession(session.sessionId);
    }

    // 清理本次运行的临时数据
    await this.state.set(`wm:${runId}:tools`, null);
    await this.state.set(`session_list:${runId}`, null);

    this.logger.debug(`[WM] 任务空间归档: runId=${runId}, completed=${completedSessions.length}, killed=${killedSessions.length}`);

    // 注入 working_memory skill，提醒 Agent 检查任务空间看板
    const workingMemorySkill = await this.skillLoader.load('working_memory');
    if (workingMemorySkill) {
      return {
        prependSystemContext: `${workingMemorySkill}\n\n【Agent 职责】本次运行已结束，请根据上方 working_memory skill 检查「当前活跃任务空间看板」和「任务空间复用策略」。completed 的任务空间已标记为 idle，可供同任务族后续复用。\n`
      };
    }
  }

  /**
   * 更新全局活跃任务空间索引
   * 键: working_memory:active_sessions
   * Memory Table 作为任务空间的集中管理中心
   */
  async _updateActiveSession(sessionId, taskFamily, status) {
    const activeSessions = await this.state.get('working_memory:active_sessions', []);
    const existingIndex = activeSessions.findIndex(s => s.sessionId === sessionId);

    if (existingIndex >= 0) {
      activeSessions[existingIndex] = {
        ...activeSessions[existingIndex],
        taskFamily,
        status,
        lastActive: getNow()
      };
    } else {
      activeSessions.push({
        sessionId,
        taskFamily,
        status,
        lastActive: getNow()
      });
    }

    await this.state.set('working_memory:active_sessions', activeSessions);
  }

  /**
   * 从全局活跃索引中移除任务空间
   */
  async _removeActiveSession(sessionId) {
    const activeSessions = await this.state.get('working_memory:active_sessions', []);
    const updated = activeSessions.filter(s => s.sessionId !== sessionId);
    await this.state.set('working_memory:active_sessions', updated);
  }

  /**
   * 将工具结果摘要化为短字符串
   */
  summarizeResult(result) {
    if (!result) return '无结果';
    if (typeof result === 'string') return result.slice(0, 200);
    if (result.summary) return result.summary;
    if (result.status) return `status=${result.status}`;
    return JSON.stringify(result).slice(0, 200);
  }
}
