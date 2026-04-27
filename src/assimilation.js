/**
 * 同化顺应模块
 *
 * OpenClaw 没有 cron:* hook，使用 api.registerService() 启动后台定时器，
 * 每日 00:00 执行自我更新。
 *
 * 技能文档要求:
 *   - 每日 00:00 (Asia/Shanghai) 执行
 *   - 读取前一日事件记忆
 *   - 撰写发展日记
 *   - 阅读核心自我与配置文件
 *   - 同化与顺应分析
 *   - 检测更新信号并执行更新
 *   - 记录更新日志
 *
 * 官方 registerService 签名:
 *   api.registerService({
 *     id: "my-service",
 *     start: (ctx) => { ... },
 *     stop: (ctx) => { ... }
 *   });
 *
 * Handler 签名: async (event, ctx) => { ... }
 */

import cron from 'node-cron';
import { getToday, getYesterday, getNow, callLLM } from './utils.js';

export function createAssimilationModule({ api, config, state, logger, llmConfig }) {
  const enabled = config?.enabled !== false;
  const autoUpdate = config?.autoUpdate === true;
  const updateThreshold = config?.updateThreshold || 0.8;

  let cronJob = null;
  let fallbackTimer = null;
  let fallbackInterval = null;

  function register() {
    if (!enabled) {
      logger.info('[Assim] 同化顺应模块已禁用');
      return;
    }

    logger.info('[Assim] 注册同化顺应服务');

    const serviceRegistered = registerDailyService();
    if (!serviceRegistered) {
      logger.info('[Assim] 使用 gateway_start fallback 启动定时器');
      api.on('gateway_start', () => startDailyTimer());
      api.on('gateway_stop', () => stopDailyTimer());
    }
  }

  function registerDailyService() {
    if (typeof api.registerService !== 'function') return false;

    try {
      api.registerService({
        id: 'asd-daily-updater',
        start: (ctx) => {
          logger.info('[Assim][Service] 每日更新服务已启动');
          startDailyTimer();
        },
        stop: (ctx) => {
          logger.info('[Assim][Service] 每日更新服务已停止');
          stopDailyTimer();
        }
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
    logger.info(`[Assim] 启动每日更新定时器: ${cronExpr} (Asia/Shanghai)`);

    try {
      cronJob = cron.schedule(cronExpr, () => {
        runDailyUpdate().catch(err => logger.error(`[Assim] 定时更新失败: ${err.message}`));
      }, {
        scheduled: true,
        timezone: 'Asia/Shanghai'
      });
    } catch (err) {
      logger.warn(`[Assim] node-cron 启动失败: ${err.message}，回退到原生定时器`);
      startFallbackTimer();
    }
  }

  function startFallbackTimer() {
    const now = new Date();
    const tomorrow = new Date(now);
    tomorrow.setDate(tomorrow.getDate() + 1);
    tomorrow.setHours(0, 0, 0, 0);
    const msUntilMidnight = tomorrow - now;

    logger.info(`[Assim] 下次更新: ${tomorrow.toISOString()} (还有 ${Math.round(msUntilMidnight / 1000)} 秒)`);

    fallbackTimer = setTimeout(() => {
      runDailyUpdate();
      fallbackInterval = setInterval(runDailyUpdate, 24 * 60 * 60 * 1000);
    }, msUntilMidnight);
  }

  function stopDailyTimer() {
    if (cronJob) {
      cronJob.stop();
      cronJob = null;
    }
    if (fallbackTimer) {
      clearTimeout(fallbackTimer);
      fallbackTimer = null;
    }
    if (fallbackInterval) {
      clearInterval(fallbackInterval);
      fallbackInterval = null;
    }
  }

  async function runDailyUpdate() {
    // 每日更新应处理昨日事件（因为 00:00 执行时，今日刚开始，事件为空）
    const targetDate = getYesterday();
    logger.info(`[Assim] 开始每日自我更新: 处理日期 ${targetDate}`);

    try {
      const events = (await state.get(`events:${targetDate}`)) || [];
      logger.info(`[Assim] 事件数: ${events.length} (日期: ${targetDate})`);

      const diary = await generateDiary(targetDate, events);
      await state.set(`diary:${targetDate}`, diary);
      logger.info(`[Assim] 日记已生成`);

      const coreSelf = await loadCoreSelf();
      const analysis = analyzeAssimilation(diary, coreSelf);
      await state.set(`analysis:${targetDate}`, analysis);
      logger.info(`[Assim] 分析完成: ${analysis.summary}`);

      for (const signal of analysis.signals) {
        if (signal.confidence >= updateThreshold) {
          if (autoUpdate) {
            await applyUpdate(signal, coreSelf);
            logger.info(`[Assim] 自动更新: ${signal.type}`);
          } else {
            await state.append(`pending_updates:${targetDate}`, signal);
            logger.info(`[Assim] 待确认更新信号: ${signal.type}`);
          }
        }
      }
    } catch (err) {
      logger.error(`[Assim] 每日更新失败: ${err.message}`);
    }
  }

  // ─────────── 核心逻辑 ───────────

  async function generateDiary(date, events) {
    if (events.length === 0) {
      return { date, events: [], reflection: '今日无重大事件。', raw: '' };
    }

    const eventTexts = events.map(e => `[${e.time || ''}] ${e.summary || e.description || JSON.stringify(e)}`).join('\n');

    try {
      const prompt = [
        `请基于以下 Agent 今日事件，撰写一段简短的发展日记反思（200字以内，第一人称"我"）。`,
        `日期: ${date}`,
        '事件:',
        eventTexts,
        '要求: 总结核心认知变化，识别是否有新技能、角色或价值观的调整信号。只输出反思段落。'
      ].join('\n');

      const safeLLMConfig = llmConfig || { provider: 'kimicode', model: 'kimi-for-coding' };
      const reflection = await callLLM(prompt, safeLLMConfig);
      return { date, events, reflection, raw: reflection };
    } catch (err) {
      logger.warn(`[Assim] LLM 日记生成失败: ${err.message}`);
      return { date, events, reflection: '今日执行了常规任务。', raw: '' };
    }
  }

  async function loadCoreSelf() {
    return {
      identity: (await state.get('core:identity')) || {},
      soul: (await state.get('core:soul')) || {},
      skills: (await state.get('core:skills')) || []
    };
  }

  function analyzeAssimilation(diary, coreSelf) {
    const text = (diary.raw || diary.reflection || '').toLowerCase();
    const signals = [];

    const checks = [
      { keywords: ['学会', '掌握', '新技能'], type: 'skills', desc: '检测到新技能习得' },
      { keywords: ['角色', '身份', '负责'], type: 'identity', desc: '检测到角色变化' },
      { keywords: ['应该', '更重要', '改变方式', '风格'], type: 'style_beliefs', desc: '检测到价值观/风格调整' },
      { keywords: ['无法', '超出', '边界', '极限'], type: 'core_self', desc: '检测到能力边界变化' }
    ];

    for (const check of checks) {
      if (check.keywords.some(k => text.includes(k))) {
        signals.push({
          type: check.type,
          description: check.desc,
          confidence: 0.75,
          recommendedAction: `${check.type}_update`
        });
      }
    }

    return {
      date: getToday(),
      assimilation: signals.filter(s => s.confidence < 0.8).length,
      accommodation: signals.filter(s => s.confidence >= 0.8).length,
      signals,
      summary: `同化=${signals.filter(s => s.confidence < 0.8).length}, 顺应=${signals.filter(s => s.confidence >= 0.8).length}, 信号=${signals.length}`
    };
  }

  async function applyUpdate(signal, coreSelf) {
    const now = getNow();

    switch (signal.type) {
      case 'skills': {
        const skills = coreSelf.skills;
        skills.push({ name: '新习得技能', learnedAt: now, source: 'assimilation' });
        await state.set('core:skills', skills);
        break;
      }
      case 'identity': {
        const identity = coreSelf.identity;
        identity.lastUpdated = now;
        identity.notes = (identity.notes || '') + `\n[${now}] ${signal.description}`;
        await state.set('core:identity', identity);
        break;
      }
      case 'style_beliefs': {
        const soul = coreSelf.soul;
        soul.lastUpdated = now;
        soul.beliefs = (soul.beliefs || []);
        soul.beliefs.push(signal.description);
        await state.set('core:soul', soul);
        break;
      }
      case 'core_self': {
        const identity = coreSelf.identity;
        identity.boundaries = identity.boundaries || {};
        identity.boundaries.lastUpdated = now;
        await state.set('core:identity', identity);
        break;
      }
    }

    await state.append(`updates:${getToday()}`, { time: now, type: signal.type, description: signal.description });
  }

  return { register };
}
