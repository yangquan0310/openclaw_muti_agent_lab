/**
 * 工作记忆模块
 * 
 * 官方 Hook 映射:
 *   before_tool_call → 子代理启动追踪（OpenClaw 中子代理通过 agent/subagent 工具创建）
 *   after_tool_call  → 记录工具执行结果
 *   agent_end        → 归档本次运行的工具调用历史
 * 
 * Handler 签名: async (event, ctx) => { ... }
 */

const { getToday, getNow } = require('./utils');

function createWorkingMemoryModule({ api, config, state, logger }) {
  const enabled = config?.enabled !== false;
  const trackSubagents = enabled && config?.trackSubagents !== false;
  const autoArchive = enabled && config?.autoArchive !== false;

  function register() {
    if (!enabled) {
      logger.info('[WM] 工作记忆模块已禁用');
      return;
    }

    logger.info('[WM] 注册工作记忆 Hooks');

    // ── 子代理追踪: before_tool_call ──
    if (trackSubagents) {
      api.on('before_tool_call', async (event, ctx) => {
        const toolName = event.toolName;
        if (toolName !== 'agent' && toolName !== 'subagent') return;

        const runId = ctx.runId;
        const subagentId = event.params?.id || event.params?.name || `sub-${Date.now()}`;

        const entry = {
          type: 'subagent_spawn',
          subagentId,
          parentRunId: runId,
          purpose: event.params?.purpose || event.params?.instruction || '',
          model: event.params?.model || 'default',
          toolName,
          timestamp: getNow()
        };

        await state.append(`wm:${runId}:tools`, entry);
        logger.debug(`[WM] 追踪子代理: ${subagentId} (parent=${runId})`);
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

      if (toolName === 'agent' || toolName === 'subagent') {
        await state.append(`wm:${runId}:tools`, {
          type: 'subagent_complete',
          subagentId: event.params?.id || event.params?.name,
          resultSummary: summarizeResult(result),
          timestamp: getNow()
        });
      }
    });

    // ── 归档: agent_end ──
    if (autoArchive) {
      api.on('agent_end', async (event, ctx) => {
        const runId = ctx.runId;
        if (!runId) return;

        const toolHistory = await state.get(`wm:${runId}:tools`, []);
        if (toolHistory.length === 0) {
          await state.set(`wm:${runId}:tools`, null);
          return;
        }

        const archive = {
          runId,
          archivedAt: getNow(),
          toolCount: toolHistory.length,
          tools: toolHistory
        };

        await state.append(`memory_table:${getToday()}`, archive);
        await state.set(`wm:${runId}:tools`, null);

        logger.info(`[WM] 归档: runId=${runId}, tools=${toolHistory.length}`);
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

module.exports = { createWorkingMemoryModule };
