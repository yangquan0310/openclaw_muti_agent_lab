/**
 * 人格模块 —— 面向对象封装
 *
 * 插件职责：当 Agent 收到 cron 触发的每日自我更新消息时，注入 personality skill
 * Agent 职责：自行阅读 skill、回顾事件、撰写日记、分析同化/顺应、更新核心自我文件
 *
 * 注意：每日定时任务由用户在 ~/.openclaw/cron/jobs.json 中配置，插件不管理定时器。
 */

import { getYesterday } from '../common/utils.js';

export class PersonalityModule {
  constructor({ api, config, stateAdapter, skillLoader, logger, eventManager, diaryManager }) {
    this.api = api;
    this.config = config || {};
    this.stateAdapter = stateAdapter;
    this.skillLoader = skillLoader;
    this.logger = logger;
    this.eventManager = eventManager;
    this.diaryManager = diaryManager;
    this.enabled = this.config.enabled !== false;
  }

  /**
   * 注册人格模块相关的 hooks
   */
  register() {
    if (!this.enabled) {
      this.logger.info('[Personality] 人格模块已禁用');
      return;
    }

    this.logger.info('[Personality] 注册人格模块 Hook');
    this.api.on('before_prompt_build', this.onBeforePromptBuild.bind(this), { priority: 40 });
  }

  /**
   * 检测 cron 每日自我更新触发消息，注入 personality skill
   */
  async onBeforePromptBuild(event, ctx) {
    const prompt = event.prompt || '';
    const isDailyUpdate = prompt.includes('[cron:每日自我更新]') || prompt.includes('每日自我更新');
    if (!isDailyUpdate) return;

    const personalitySkill = await this.skillLoader.load('assimilation');
    if (!personalitySkill) {
      this.logger.warn('[Personality] personality skill 未找到');
      return;
    }

    const yesterday = getYesterday();
    const events = await this.eventManager.queryEventLog(yesterday);

    return {
      prependSystemContext: `${personalitySkill}\n\n【昨日事件摘要】昨日（${yesterday}）共有 ${events.length} 条事件记录。\n【Agent 职责】请根据上方 personality skill 自行回顾事件、撰写日记、分析同化/顺应，并决定是否需要更新核心自我文件。\n`
    };
  }
}
