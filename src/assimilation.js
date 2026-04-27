/**
 * 同化顺应模块 —— 纯提醒框架
 *
 * 插件职责：每日定时提醒 Agent 进行自我更新
 * Agent 职责：自行回顾事件、生成日记、分析同化/顺应、更新核心自我文件
 *
 * 不涉及：文件读写、LLM 调用、偏差判断、置信度评估
 */

import cron from 'node-cron';
import { getToday, getYesterday } from './utils.js';

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
    // 如果今日有待处理的自我更新提醒，注入 system context
    api.on('before_prompt_build', async (event, ctx) => {
      const runId = ctx.runId;
      if (!runId) return;

      const reminderDate = await state.get('assim:reminderDate');
      const today = getToday();
      if (reminderDate !== today) return;

      const yesterday = getYesterday();
      const events = (await state.get(`events:${yesterday}`)) || [];
      const eventCount = events.length;

      return {
        prependSystemContext: `【自我发展提醒】\n昨日（${yesterday}）共有 ${eventCount} 条事件记录。\n如尚未进行，请在合适时机回顾昨日事件、撰写发展日记，并决定是否需要更新核心自我文件（IDENTITY.md / SOUL.md / MEMORY.md / skills）。\n`
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
