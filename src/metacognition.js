/**
 * 元认知模块 —— 纯钩子框架
 *
 * 插件职责：在合适的时机将对应的 skill 文档注入 Agent 的 system context
 * Agent 职责：自行阅读 skill、判断偏差、决定是否 revise
 */

import { generatePlanItems, assignSessions } from './utils.js';
import { loadSkill } from './skills-loader.js';

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
    // 复杂任务时注入 planning skill + 计划建议
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

        const planningSkill = await loadSkill('planning');

        return {
          prependSystemContext: `${planningSkill}\n\n【当前执行计划】\n${planLines}\n\n【Agent 职责】请根据上方 skill 指导自行制定和执行计划。如需偏离计划请先说明理由。\n`
        };
      }, { priority: 50 });
    }

    // ── Monitoring: llm_output ──
    // 注入 monitoring skill，Agent 自行阅读并判断偏差
    if (monitoringEnabled) {
      api.on('llm_output', async (event, ctx) => {
        const runId = ctx.runId;
        if (!runId) return;

        const output = event.output || event.text || '';
        await state.set(`output:${runId}`, output);

        const monitoringSkill = await loadSkill('monitoring');
        if (!monitoringSkill) return;

        // 仅在计划存在时注入监控 skill（避免简单任务也被注入）
        const plan = await state.get(`plan:${runId}`);
        if (!plan) return;

        return {
          prependSystemContext: `${monitoringSkill}\n\n【Agent 职责】请根据上方 monitoring skill 自行检查当前输出是否与计划一致，识别偏差或阻塞。\n`
        };
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
