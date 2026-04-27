/**
 * 元认知模块
 * 
 * 官方 Hook 映射:
 *   before_agent_start    → 计划 (Planning): 解析 prompt，生成执行计划存入 state
 *   before_prompt_build   → 注入计划: 将计划注入 system context
 *   llm_output            → 监控 (Monitoring): 分析输出与计划的偏差
 *   before_agent_finalize → 调节 (Regulation): 偏差大时请求 revise
 *   agent_end             → 清理状态
 * 
 * 依赖: plugins.entries.<id>.hooks.allowConversationAccess = true
 * 
 * Handler 签名: async (event, ctx) => { ... }
 *   ctx.runId / ctx.agentId / ctx.sessionKey / ctx.logger
 */

const { generatePlanItems } = require('./utils');

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

    // ── Planning: before_agent_start ──
    if (planningEnabled) {
      api.on('before_agent_start', async (event, ctx) => {
        const runId = ctx.runId;
        const prompt = event.prompt || '';

        const plan = {
          runId,
          prompt: prompt.slice(0, 500),
          items: generatePlanItems(prompt),
          createdAt: Date.now(),
          stage: 'monitoring'
        };

        await state.set(`plan:${runId}`, plan);
        logger.debug(`[Meta][Planning] runId=${runId}, steps=${plan.items.length}`);
      }, { priority: 50 });
    }

    // ── Prompt Injection: before_prompt_build ──
    if (planningEnabled) {
      api.on('before_prompt_build', async (event, ctx) => {
        const runId = ctx.runId;
        if (!runId) return;

        const plan = await state.get(`plan:${runId}`);
        if (!plan) return;

        const planText = plan.items.map((s, i) => `${i + 1}. ${s}`).join('\n');

        logger.debug(`[Meta][PromptBuild] 注入计划到 runId=${runId}`);

        return {
          prependSystemContext: `【执行计划】请严格按照以下步骤执行，完成一步后主动报告进度。若发现偏离计划，请立即说明。\n${planText}\n`
        };
      });
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

    for (let i = 0; i < plan.items.length; i++) {
      const keyword = plan.items[i].slice(0, 10).toLowerCase();
      if (outputLower.includes(keyword) || outputLower.includes(`步骤${i + 1}`)) {
        currentStep = i + 1;
      }
    }

    const errorSignals = ['错误', '失败', '无法', 'exception', 'error', 'failed', 'cannot'];
    const hasError = errorSignals.some(s => outputLower.includes(s));
    const blocked = outputLower.includes('阻塞') || outputLower.includes('等待');
    const significant = hasError || blocked;

    return {
      expected: `步骤 ${currentStep}/${plan.items.length}`,
      actual: '由单次 llm_output 推断',
      significant,
      reason: hasError ? '输出中包含错误信号' : blocked ? '任务可能阻塞' : '无明显偏差',
      adjustment: hasError
        ? '请检查错误原因，尝试修复或回退到上一个稳定状态。'
        : blocked
        ? '识别阻塞原因，尝试替代方案。'
        : '继续按原计划执行。'
    };
  }

  return { register };
}

module.exports = { createMetacognitionModule };
