/**
 * 同化顺应模块 —— 纯提醒框架
 *
 * 插件职责：当 Agent 收到 cron 触发的每日自我更新消息时，注入 assimilation skill
 * Agent 职责：自行阅读 skill、回顾事件、撰写日记、分析同化/顺应、更新文件
 *
 * 注意：每日定时任务由用户在 ~/.openclaw/cron/jobs.json 中配置，插件不管理定时器。
 */

import { getYesterday } from './utils.js';
import { loadSkill } from './skills-loader.js';

export function createAssimilationModule({ api, config, state, logger }) {
  const enabled = config?.enabled !== false;

  function register() {
    if (!enabled) {
      logger.info('[Assim] 同化顺应模块已禁用');
      return;
    }

    logger.info('[Assim] 注册同化顺应 Hook');

    // ── 提醒注入: before_prompt_build ──
    // 检测 cron 每日自我更新触发消息，注入 assimilation skill
    api.on('before_prompt_build', async (event, ctx) => {
      const prompt = event.prompt || '';
      const isDailyUpdate = prompt.includes('[cron:每日自我更新]') || prompt.includes('每日自我更新');
      if (!isDailyUpdate) return;

      const assimilationSkill = await loadSkill('assimilation');
      if (!assimilationSkill) {
        logger.warn('[Assim] assimilation skill 未找到');
        return;
      }

      const yesterday = getYesterday();
      const events = (await state.get(`events:${yesterday}`)) || [];

      return {
        prependSystemContext: `${assimilationSkill}\n\n【昨日事件摘要】昨日（${yesterday}）共有 ${events.length} 条事件记录。\n【Agent 职责】请根据上方 assimilation skill 自行回顾事件、撰写日记、分析同化/顺应，并决定是否需要更新核心自我文件。\n`
      };
    }, { priority: 40 });
  }

  return { register };
}
