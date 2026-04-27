/**
 * 元认知模块 —— 纯提醒框架
 *
 * 插件职责：为 Agent 提供计划建议和进度追踪基础设施
 * Agent 职责：自行判断偏差、决定是否 revise、管理执行节奏
 *
 * 不涉及：偏差判断、强制 revise、置信度评估
 */

import { generatePlanItems, assignSessions } from './utils.js';

export function createMetacognitionModule({ api, config, state, logger }) {
  const enabled = config?.enabled !== false;
  const planningEnabled = enabled && config?.planning !== false;
  const monitoringEnabled = enabled && config?.monitoring !== false;

  function register() {
    if (!enabled) {
      logger.info('[Meta] 元认知模块已禁用');
      return;
    }

    logger.info('[Meta] 注册元认知 Hooks');

    // ── Planning: before_prompt_build ──
    if (planningEnabled) {
      api.on('before_prompt_build', async (event, ctx) => {
        const runId = ctx.runId;
        if (!runId) return;

        const prompt = event.prompt || '';
        if (!shouldUseMetacognition(prompt)) {
          logger.debug(`[Meta] 简单任务，跳过计划: ${prompt.slice(0, 50)}`);
          return;
        }

        let plan = await state.get(`plan:${runId}`);
        if (!plan) {
          const items = generatePlanItems(prompt);
          const sessionAssignments = assignSessions(items, prompt);
          plan = {
            runId,
            prompt: prompt.slice(0, 500),
            items,
            sessionAssignments,
            createdAt: Date.now()
          };
          await state.set(`plan:${runId}`, plan);
          logger.debug(`[Meta] 计划生成: ${plan.items.length} 步`);
        }

        const planLines = plan.items.map((s, i) => {
          const assign = plan.sessionAssignments?.find(a => a.step === i + 1);
          const sessionHint = assign ? ` [建议会话: ${assign.sessionId}]` : '';
          return `${i + 1}. ${s}${sessionHint}`;
        }).join('\n');

        let sessionGuide = '';
        if (plan.sessionAssignments?.length > 0) {
          sessionGuide = `
【会话管理指引】
- 以下步骤建议创建独立会话执行
- 复用规则：执行前检查工作记忆中的「活跃会话清单」，若已存在相同标识则复用
- 向会话发送消息时，直接使用其会话ID调用 session_send
${plan.sessionAssignments.map(a => `  步骤${a.step}: ${a.sessionId} — ${a.purpose}`).join('\n')}
`;
        }

        return {
          prependSystemContext: `【执行计划建议】请根据以下步骤执行，完成一步后主动报告进度。\n${planLines}\n${sessionGuide}\n【Agent 职责】请自行判断是否需要偏离计划，如需变更请先说明理由。\n`
        };
      }, { priority: 50 });
    }

    // ── Monitoring: llm_output ──
    // 插件仅记录输出供 Agent 参考，不自行判断偏差
    if (monitoringEnabled) {
      api.on('llm_output', async (event, ctx) => {
        const runId = ctx.runId;
        if (!runId) return;
        const output = event.output || event.text || '';
        await state.set(`output:${runId}`, output);
        logger.debug(`[Meta] 输出已记录，runId=${runId}`);
      });
    }

    // ── Cleanup: agent_end ──
    api.on('agent_end', async (event, ctx) => {
      const runId = ctx.runId;
      if (!runId) return;
      await state.set(`plan:${runId}`, null);
      await state.set(`output:${runId}`, null);
      logger.debug(`[Meta] 清理状态: runId=${runId}`);
    });
  }

  function shouldUseMetacognition(prompt) {
    const simplePatterns = [
      /^(查询|搜索|查找|什么是|怎么|如何)/i,
      /^(现在几点|今天日期|天气)/i
    ];
    return !simplePatterns.some(p => p.test(prompt.trim()));
  }

  return { register };
}
