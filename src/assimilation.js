/**
 * 同化顺应模块 —— 纯钩子框架
 *
 * 插件职责：每日定时触发，将 assimilation skill 注入 Agent 的 system context
 * Agent 职责：自行阅读 skill、回顾事件、撰写日记、分析同化/顺应、更新文件
 */

import cron from 'node-cron';
import { getToday, getYesterday } from './utils.js';
import { loadSkill } from './skills-loader.js';

export function createAssimilationModule({ api, config, state, logger }) {
  const enabled = config?.enabled !== false;
  let cronJob = null;
  let fallbackInterval = null;

  function register() {
    if (!enabled) {
      logger.info('[Assim] 同化顺应模块已禁用');
      return;
    }

    logger.info('[Assim] 注册同化顺应提醒服务');

    const serviceRegistered = registerDailyService();
    if (!serviceRegistered) {
      api.on('gateway_start', () => startDailyTimer());
      api.on('gateway_stop', () => stopDailyTimer());
    }

    // ── 提醒注入: before_prompt_build ──
    // 如果今日有待处理的自我更新提醒，注入 assimilation skill
    api.on('before_prompt_build', async (event, ctx) => {
      const runId = ctx.runId;
      if (!runId) return;

      const reminderDate = await state.get('assim:reminderDate');
      const today = getToday();
      if (reminderDate !== today) return;

      const assimilationSkill = await loadSkill('assimilation');
      if (!assimilationSkill) return;

      const yesterday = getYesterday();
      const events = (await state.get(`events:${yesterday}`)) || [];

      return {
        prependSystemContext: `${assimilationSkill}\n\n【昨日事件摘要】昨日（${yesterday}）共有 ${events.length} 条事件记录。\n【Agent 职责】请根据上方 assimilation skill 自行回顾事件、撰写日记、分析同化/顺应，并决定是否需要更新核心自我文件。\n`
      };
    }, { priority: 40 });
  }

  function registerDailyService() {
    if (typeof api.registerService !== 'function') return false;
    try {
      api.registerService({
        id: 'asd-daily-reminder',
        start: () => startDailyTimer(),
        stop: () => stopDailyTimer()
      });
      return true;
    } catch (err) {
      logger.warn(`[Assim] registerService 失败: ${err.message}`);
      return false;
    }
  }

  function startDailyTimer() {
    stopDailyTimer();
    const cronExpr = config?.dailyCron || '0 0 * * *';
    logger.info(`[Assim] 启动每日提醒定时器: ${cronExpr} (Asia/Shanghai)`);

    try {
      cronJob = cron.schedule(cronExpr, () => {
        setDailyReminder().catch(err => logger.error(`[Assim] 设置提醒失败: ${err.message}`));
      }, { scheduled: true, timezone: 'Asia/Shanghai' });
    } catch (err) {
      logger.warn(`[Assim] node-cron 启动失败: ${err.message}，回退到原生定时器`);
      startFallbackTimer();
    }
  }

  function startFallbackTimer() {
    const CHECK_INTERVAL = 5 * 60 * 1000;
    let lastCheckedDate = null;
    logger.info(`[Assim] 启动回退定时器 (每 ${CHECK_INTERVAL / 60000} 分钟检查)`);

    fallbackInterval = setInterval(() => {
      const now = new Date();
      const shNow = new Date(now.toLocaleString('en-US', { timeZone: 'Asia/Shanghai' }));
      const currentDateStr = shNow.toISOString().split('T')[0];
      if (currentDateStr !== lastCheckedDate && shNow.getHours() === 0 && shNow.getMinutes() < 5) {
        lastCheckedDate = currentDateStr;
        setDailyReminder().catch(err => logger.error(`[Assim] 设置提醒失败: ${err.message}`));
      }
    }, CHECK_INTERVAL);
  }

  function stopDailyTimer() {
    if (cronJob) { cronJob.stop(); cronJob = null; }
    if (fallbackInterval) { clearInterval(fallbackInterval); fallbackInterval = null; }
  }

  async function setDailyReminder() {
    const today = getToday();
    await state.set('assim:reminderDate', today);
    logger.info(`[Assim] 已设置今日自我更新提醒: ${today}`);
  }

  return { register };
}
