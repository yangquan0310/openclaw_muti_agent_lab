/**
 * 元认知模块
 *
 * 官方 Hook 映射:
 *   before_prompt_build   → 计划 + 注入: 生成执行计划并注入 system context
 *                         （新插件推荐用 before_prompt_build 替代已废弃的 before_agent_start）
 *   llm_output            → 监控 (Monitoring): 分析输出与计划的偏差
 *   before_agent_finalize → 调节 (Regulation): 偏差大时请求 revise
 *   agent_end             → 清理状态
 *
 * 依赖: plugins.entries.<id>.hooks.allowConversationAccess = true
 *
 * Handler 签名: async (event, ctx) => { ... }
 *   ctx.runId / ctx.agentId / ctx.sessionKey / ctx.logger
 */

const { generatePlanItems, assignSessions } = require('./utils');

function createMetacognitionModule({ api, config, state, logger }) {
  const enabled = config?.enabled !== false;
  const planningEnabled = enabled && config?.planning !== false;
  const monitoringEnabled = enabled && config?.monitoring !== false;
  const regulationEnabled = enabled && config?.regulation !== false;

  function register() {
    if (!enabled) {
      logger.info('[Meta] 元认知模块已禁用');
      return;
    }

    logger.info('[Meta] 注册元认知 Hooks');

    // ── Planning + Prompt Injection: before_prompt_build ──
    // 官方推荐新插件使用 before_prompt_build 替代 before_agent_start
    if (planningEnabled) {
      api.on('before_prompt_build', async (event, ctx) => {
        const runId = ctx.runId;
        if (!runId) return;

        let plan = await state.get(`plan:${runId}`);
        if (!plan) {
          const prompt = event.prompt || '';
          const items = generatePlanItems(prompt);
          const sessionAssignments = assignSessions(items, prompt);
          plan = {
            runId,
            prompt: prompt.slice(0, 500),
            items,
            sessionAssignments,
            createdAt: Date.now(),
            stage: 'monitoring'
          };
          await state.set(`plan:${runId}`, plan);
          logger.debug(`[Meta][Planning] runId=${runId}, steps=${plan.items.length}, sessions=${sessionAssignments.length}`);
        }

        // 构建带会话分配提示的计划文本
        const planLines = plan.items.map((s, i) => {
          const assign = plan.sessionAssignments?.find(a => a.step === i + 1);
          const sessionHint = assign ? ` [建议会话: ${assign.sessionId}]` : '';
          return `${i + 1}. ${s}${sessionHint}`;
        }).join('\n');

        // 如果存在会话分配，追加会话管理指引
        let sessionGuide = '';
        if (plan.sessionAssignments?.length > 0) {
          sessionGuide = `
【会话管理指引】
- 以下步骤建议创建独立会话执行，创建后记录其会话ID到工作记忆
- 复用规则：执行前检查工作记忆中的「活跃会话清单」，若已存在相同标识的会话则复用，不再创建
- 会话标识格式: session:{TYPE}:{任务标识}
- 向会话发送消息时，直接使用其会话ID作为参数调用 session_send
${plan.sessionAssignments.map(a => `  步骤${a.step}: ${a.sessionId} — ${a.purpose}`).join('\n')}
`;
        }

        logger.debug(`[Meta][PromptBuild] 注入计划到 runId=${runId}`);

        return {
          prependSystemContext: `【执行计划】请严格按照以下步骤执行，完成一步后主动报告进度。若发现偏离计划，请立即说明。\n${planLines}\n${sessionGuide}\n`
        };
      }, { priority: 50 });
    }

    // ── Monitoring: llm_output ──
    if (monitoringEnabled) {
      api.on('llm_output', async (event, ctx) => {
        const runId = ctx.runId;
        if (!runId) return;

        const plan = await state.get(`plan:${runId}`);
        if (!plan) return;

        const output = event.output || event.text || '';
        const deviation = detectDeviation(plan, output);

        if (deviation.significant) {
          await state.set(`deviation:${runId}`, deviation);
          logger.warn(`[Meta][Monitoring] 偏差检测: ${deviation.reason}`);
        }
      });
    }

    // ── Regulation: before_agent_finalize ──
    if (regulationEnabled) {
      api.on('before_agent_finalize', async (event, ctx) => {
        const runId = ctx.runId;
        if (!runId) return;

        const deviation = await state.get(`deviation:${runId}`);
        if (!deviation?.significant) return;

        logger.info(`[Meta][Regulation] 请求 revise: ${deviation.reason}`);

        // 清除偏差标记，防止无限循环
        await state.set(`deviation:${runId}`, null);

        return {
          action: 'revise',
          reason: `元认知调节: ${deviation.reason}\n建议调整: ${deviation.adjustment}`
        };
      });
    }

    // ── Cleanup: agent_end ──
    api.on('agent_end', async (event, ctx) => {
      const runId = ctx.runId;
      if (!runId) return;

      await state.set(`plan:${runId}`, null);
      await state.set(`deviation:${runId}`, null);
      logger.debug(`[Meta] 清理状态: runId=${runId}`);
    });
  }

  // ─────────── 辅助函数 ───────────

  function detectDeviation(plan, output) {
    const outputLower = (output || '').toLowerCase();
    let currentStep = 0;
    let completedSteps = 0;

    for (let i = 0; i < plan.items.length; i++) {
      const keyword = plan.items[i].slice(0, 10).toLowerCase();
      if (outputLower.includes(keyword) || outputLower.includes(`步骤${i + 1}`) || outputLower.includes(`step ${i + 1}`)) {
        currentStep = i + 1;
      }
      // 检查是否报告完成了该步骤
      const completionSignals = ['完成', 'done', 'finished', '已执行', '已处理', 'ok'];
      if (completionSignals.some(s => outputLower.includes(`${s}步骤${i + 1}`) || outputLower.includes(`步骤${i + 1}${s}`))) {
        completedSteps++;
      }
    }

    const errorSignals = ['错误', '失败', '无法', 'exception', 'error', 'failed', 'cannot'];
    const hasError = errorSignals.some(s => outputLower.includes(s));
    const blocked = outputLower.includes('阻塞') || outputLower.includes('等待') || outputLower.includes('blocked') || outputLower.includes('waiting');
    const offTrack = outputLower.includes('偏离') || outputLower.includes('变更') || outputLower.includes('调整方案') || outputLower.includes('改用');

    const significant = hasError || blocked || offTrack;

    return {
      expected: `步骤 ${currentStep}/${plan.items.length}`,
      actual: `已完成 ${completedSteps}/${plan.items.length} 步`,
      significant,
      reason: hasError ? '输出中包含错误信号'
        : blocked ? '任务可能阻塞'
        : offTrack ? '检测到方案偏离或工具变更'
        : '无明显偏差',
      adjustment: hasError
        ? '请检查错误原因，尝试修复或回退到上一个稳定状态。'
        : blocked
        ? '识别阻塞原因，尝试替代方案。'
        : offTrack
        ? '请回归原计划，如需变更方案请先向用户说明。'
        : '继续按原计划执行。'
    };
  }

  return { register };
}

module.exports = { createMetacognitionModule };
