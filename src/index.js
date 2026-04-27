/**
 * OpenClaw Agent Self-Development Plugin
 *
 * 遵循 OpenClaw 官方 SDK 规范：
 * - 使用 definePluginEntry 定义插件入口
 * - 使用 api.pluginConfig 读取配置
 * - 使用 api.logger 输出日志
 * - 使用 api.on(name, (event, ctx) => {}, opts) 注册钩子
 *
 * 参考: https://docs.openclaw.ac.cn/plugins/sdk-overview
 */

import { definePluginEntry } from 'openclaw/plugin-sdk/plugin-entry';
import { PluginState } from './state.js';
import { createMetacognitionModule } from './metacognition.js';
import { createWorkingMemoryModule } from './working-memory.js';
import { createAssimilationModule } from './assimilation.js';
import { readIdentityFile, readSoulFile, readMemoryFile, readSkillsIndex } from './files.js';

export default definePluginEntry({
  id: 'agent-self-development',
  name: 'Agent Self-Development',
  version: '1.2.0',

  register(api) {
    // 非运行时加载（discovery/setup-only/cli-metadata）跳过副作用
    if (api.registrationMode && api.registrationMode !== 'full') {
      return;
    }

    const pluginId = 'agent-self-development';
    const config = api.pluginConfig || {};
    const state = new PluginState(pluginId);
    const logger = api.logger || console;

    logger.info(`[${pluginId}] Agent Self-Development Plugin v1.2.0 activated`);

    // 检查 conversation hooks 权限
    const entries = api.config?.plugins?.entries?.[pluginId];
    if (entries?.hooks?.allowConversationAccess !== true) {
      logger.warn(`[${pluginId}] ⚠️ plugins.entries.${pluginId}.hooks.allowConversationAccess 未启用，元认知监控可能无法工作`);
    }

    // 阶段0：会话初始化 — 载入核心自我文件到状态（异步，不阻塞注册）
    initializeCoreSelf(state, logger).catch(err => logger.warn(`[Init] 初始化失败: ${err.message}`));

    // 初始化三大模块
    const metacognition = createMetacognitionModule({ api, config: config.metacognition, state, logger });
    const workingMemory = createWorkingMemoryModule({ api, config: config.workingMemory, state, logger });
    const llmConfig = {
      ...config.llm,
      apiKey: config.llm?.apiKey
    };
    const assimilation = createAssimilationModule({ api, config: config.assimilation, state, logger, llmConfig });

    // 注册所有 Hooks 和服务
    metacognition.register();
    workingMemory.register();
    assimilation.register();

    logger.info(`[${pluginId}] 全部模块已注册`);
  }
});

// 阶段0：会话初始化 — 从 Markdown 文件载入核心自我到插件状态
async function initializeCoreSelf(state, logger) {
  try {
    const [identity, soul, memory, skills] = await Promise.all([
      readIdentityFile(),
      readSoulFile(),
      readMemoryFile(),
      readSkillsIndex()
    ]);
    await state.set('core:identity', identity);
    await state.set('core:soul', soul);
    await state.set('core:memory', memory);
    await state.set('core:skills', skills);
    logger.info('[Init] 核心自我文件已载入');
  } catch (err) {
    logger.warn(`[Init] 核心自我文件载入失败: ${err.message}`);
  }
}
