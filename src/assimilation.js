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
import {
  readIdentityFile, readSoulFile, readMemoryFile, readSkillsIndex,
  appendIdentityNote, appendSoulBelief, appendSkillEntry, appendMemoryNote
} from './files.js';

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
    const CHECK_INTERVAL = 5 * 60 * 1000; // 每 5 分钟检查一次
    let lastCheckedDate = null;

    logger.info(`[Assim] 启动回退定时器 (每 ${CHECK_INTERVAL / 60000} 分钟检查)`);

    fallbackInterval = setInterval(() => {
      const now = new Date();
      const shNow = new Date(now.toLocaleString('en-US', { timeZone: 'Asia/Shanghai' }));
      const currentDateStr = shNow.toISOString().split('T')[0];

      // 只在日期切换后的第一次检查执行（00:00 ~ 00:05 之间）
      if (currentDateStr !== lastCheckedDate && shNow.getHours() === 0 && shNow.getMinutes() < 5) {
        lastCheckedDate = currentDateStr;
        runDailyUpdate().catch(err => logger.error(`[Assim] 定时更新失败: ${err.message}`));
      }
    }, CHECK_INTERVAL);
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
    const today = getToday();
    const yesterday = getYesterday();
    const lastProcessed = await state.get('assim:lastProcessedDate');

    let targetDate = yesterday;
    if (lastProcessed === targetDate) {
      logger.debug(`[Assim] 日期 ${targetDate} 已处理，跳过`);
      return;
    }

    logger.info(`[Assim] 开始每日自我更新: 处理日期 ${targetDate}`);

    try {
      const events = (await state.get(`events:${targetDate}`)) || [];
      logger.info(`[Assim] 事件数: ${events.length} (日期: ${targetDate})`);

      // 生成日记（插件负责基础设施）
      const diary = await generateDiary(targetDate, events);
      await state.set(`diary:${targetDate}`, diary);
      logger.info(`[Assim] 日记已生成`);

      // 读取核心自我文件（插件负责文件读写基础设施）
      const coreSelf = await loadCoreSelf();
      await state.set(`core_self:${targetDate}`, coreSelf);
      logger.info(`[Assim] 核心自我文件已载入`);

      // 插件提供日记和核心自我给 Agent，Agent 自行分析同化/顺应
      // 如 autoUpdate=true，插件执行简单的关键词信号自动更新
      if (autoUpdate) {
        const signals = detectSignals(diary);
        for (const signal of signals) {
          if (signal.confidence >= updateThreshold) {
            await applyUpdate(signal);
            logger.info(`[Assim] 自动更新: ${signal.type}`);
          }
        }
      } else {
        // 仅记录关键词提示，Agent 自行评估和决定
        const hints = extractHints(diary);
        if (hints.length > 0) {
          await state.set(`assim_hints:${targetDate}`, hints);
          logger.info(`[Assim] 已准备 ${hints.length} 条同化/顺应提示，等待 Agent 分析`);
        }
      }

      await state.set('assim:lastProcessedDate', targetDate);
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
    const [identity, soul, memory, skills] = await Promise.all([
      readIdentityFile(),
      readSoulFile(),
      readMemoryFile(),
      readSkillsIndex()
    ]);
    return { identity, soul, memory, skills };
  }

  // 简单的关键词信号检测（低置信度，仅用于 autoUpdate 模式）
  function detectSignals(diary) {
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
        signals.push({ type: check.type, description: check.desc, confidence: 0.75 });
      }
    }
    return signals;
  }

  // 提取提示给 Agent（autoUpdate=false 时使用）
  function extractHints(diary) {
    const text = (diary.raw || diary.reflection || '').toLowerCase();
    const hints = [];
    if (['学会', '掌握', '新技能'].some(k => text.includes(k))) hints.push({ type: 'skills', hint: '日记中提到新技能，请评估是否需要更新 skills/README.md' });
    if (['角色', '身份', '负责'].some(k => text.includes(k))) hints.push({ type: 'identity', hint: '日记中提到角色变化，请评估是否需要更新 IDENTITY.md' });
    if (['应该', '更重要', '改变方式', '风格'].some(k => text.includes(k))) hints.push({ type: 'style_beliefs', hint: '日记中提到风格/价值观调整，请评估是否需要更新 SOUL.md' });
    if (['无法', '超出', '边界', '极限'].some(k => text.includes(k))) hints.push({ type: 'core_self', hint: '日记中提到能力边界，请评估是否需要更新 MEMORY.md 或 IDENTITY.md' });
    return hints;
  }

  async function applyUpdate(signal) {
    const now = getNow();
    switch (signal.type) {
      case 'skills':
        await appendSkillEntry('新习得技能', now);
        break;
      case 'identity':
        await appendIdentityNote(signal.description, now);
        break;
      case 'style_beliefs':
        await appendSoulBelief(signal.description, now);
        break;
      case 'core_self':
        await appendMemoryNote(signal.description, now);
        break;
    }
    await state.append(`updates:${getToday()}`, { time: now, type: signal.type, description: signal.description });
  }

  return { register };
}
