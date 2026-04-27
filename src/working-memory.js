/**
 * 工作记忆模块
 *
 * 官方 Hook 映射:
 *   before_tool_call → 会话启动追踪（OpenClaw 中通过 agent/subagent 工具创建会话）
 *   after_tool_call  → 记录工具执行结果，更新会话状态
 *   agent_end        → 归档本次运行的会话历史（completed 归档，killed 删除）
 *
 * 技能文档要求:
 *   - 维护「当前活跃任务看板」和「活跃会话清单」
 *   - 会话状态: active / paused / completed / killed
 *   - completed → 归档到事件记忆后删除
 *   - killed → 直接删除，不归档
 *
 * Handler 签名: async (event, ctx) => { ... }
 */

import { getToday, getNow } from './utils.js';

export function createWorkingMemoryModule({ api, config, state, logger }) {
  const enabled = config?.enabled !== false;
  const trackSubagents = enabled && config?.trackSubagents !== false;
  const autoArchive = enabled && config?.autoArchive !== false;

  function register() {
    if (!enabled) {
      logger.info('[WM] 工作记忆模块已禁用');
      return;
    }

    logger.info('[WM] 注册工作记忆 Hooks');

    // ── 会话追踪: before_tool_call ──
    if (trackSubagents) {
      api.on('before_tool_call', async (event, ctx) => {
        const toolName = event.toolName;
        const isSpawnTool = toolName === 'sessions_spawn' || toolName === 'agent' || toolName === 'subagent';
        if (!isSpawnTool) return;

        const runId = ctx.runId;
        // OpenClaw 中通过 agent/subagent 工具创建会话，直接使用工具参数中的 id/name 作为会话标识
        const sessionId = event.params?.id || event.params?.name || `sub-${Date.now()}`;

        const entry = {
          type: 'subagent_spawn',
          sessionId,
          parentRunId: runId,
          purpose: event.params?.purpose || event.params?.instruction || '',
          model: event.params?.model || 'default',
          toolName,
          status: 'active',
          timestamp: getNow()
        };

        await state.append(`wm:${runId}:tools`, entry);

        // 同时维护活跃会话清单（技能文档要求的表格结构）
        await state.append(`session_list:${runId}`, {
          sessionId,
          role: event.params?.role || '助手',
          task: entry.purpose,
          status: 'active',
          createdAt: getNow(),
          lastActive: getNow(),
          parentRunId: runId
        });

        logger.debug(`[WM] 追踪会话: ${sessionId} (parent=${runId})`);
      });
    }

    // ── 工具结果记录: after_tool_call ──
    api.on('after_tool_call', async (event, ctx) => {
      const runId = ctx.runId;
      const result = event.result;
      const toolName = event.toolName;

      const isError = result && (result.error || result.status === 'error');
      if (isError) {
        await state.append(`events:${getToday()}`, {
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

        await state.append(`wm:${runId}:tools`, {
          type: 'subagent_complete',
          sessionId,
          resultSummary: summarizeResult(result),
          status,
          timestamp: getNow()
        });

        // 更新会话清单中的状态
        const sessions = await state.get(`session_list:${runId}`, []);
        const updated = sessions.map(s =>
          s.sessionId === sessionId ? { ...s, status, lastActive: getNow() } : s
        );
        await state.set(`session_list:${runId}`, updated);
      }
    });

    // ── 归档: agent_end ──
    // 技能文档要求: completed → 归档到事件记忆后删除; killed → 直接删除，不归档
    if (autoArchive) {
      api.on('agent_end', async (event, ctx) => {
        const runId = ctx.runId;
        if (!runId) return;

        const sessions = await state.get(`session_list:${runId}`, []);
        const completedSessions = sessions.filter(s => s.status === 'completed');
        const killedSessions = sessions.filter(s => s.status === 'killed');
        const pausedSessions = sessions.filter(s => s.status === 'paused');

        // killed 直接删除，不归档
        if (killedSessions.length > 0) {
          logger.debug(`[WM] 删除 killed 会话: ${killedSessions.length}`);
        }

        // paused 保留到下次运行，不删除不归档
        if (pausedSessions.length > 0) {
          logger.debug(`[WM] 保留 paused 会话: ${pausedSessions.length}`);
        }

        if (completedSessions.length === 0 && killedSessions.length === 0 && pausedSessions.length === 0) {
          await state.set(`wm:${runId}:tools`, null);
          await state.set(`session_list:${runId}`, null);
          return;
        }

        // 只归档 completed 任务到事件记忆表
        for (const session of completedSessions) {
          const archive = {
            runId,
            sessionId: session.sessionId,
            archivedAt: getNow(),
            task: session.task,
            role: session.role,
            status: 'completed',
            toolCount: (await state.get(`wm:${runId}:tools`, [])).filter(t => t.sessionId === session.sessionId).length
          };
          await state.append(`memory_table:${getToday()}`, archive);
        }

        await state.set(`wm:${runId}:tools`, null);
        await state.set(`session_list:${runId}`, null);

        logger.debug(`[WM] 归档: runId=${runId}, completed=${completedSessions.length}, killed=${killedSessions.length}`);
      });
    }
  }

  function summarizeResult(result) {
    if (!result) return '无结果';
    if (typeof result === 'string') return result.slice(0, 200);
    if (result.summary) return result.summary;
    if (result.status) return `status=${result.status}`;
    return JSON.stringify(result).slice(0, 200);
  }

  return { register };
}
