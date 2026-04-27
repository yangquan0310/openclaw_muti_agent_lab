/**
 * OpenClaw Agent Self-Development Plugin
 * 
 * 遵循 OpenClaw 官方 SDK 规范：
 * - 导出 { id, name, register(api) }
 * - 使用 api.pluginConfig 读取配置
 * - 使用 api.logger 输出日志
 * - 使用 api.on(name, (event, ctx) => {}, opts) 注册钩子
 * 
 * 参考: https://docs.openclaw.ac.cn/plugins/sdk-overview
 */

const { PluginState } = require('./state');
const { createMetacognitionModule } = require('./metacognition');
const { createWorkingMemoryModule } = require('./working-memory');
const { createAssimilationModule } = require('./assimilation');

module.exports = {
  id: 'agent-self-development',
  name: 'Agent Self-Development',
  version: '1.0.1',

  register(api) {
    // 非运行时加载（discovery/setup-only/cli-metadata）跳过副作用
    if (api.registrationMode && api.registrationMode !== 'full') {
      return;
    }

    const pluginId = 'agent-self-development';
    const config = api.pluginConfig || {};
    const state = new PluginState(pluginId);
    const logger = api.logger || console;

    logger.info(`[${pluginId}] ╔════════════════════════════════════════════════════════════╗`);
    logger.info(`[${pluginId}] ║  Agent Self-Development Plugin v1.0.0 已激活               ║`);
    logger.info(`[${pluginId}] ║  基于皮亚杰认知发展理论 · 钩子驱动                         ║`);
    logger.info(`[${pluginId}] ╚════════════════════════════════════════════════════════════╝`);

    // 初始化三大模块
    const metacognition = createMetacognitionModule({ api, config: config.metacognition, state, logger });
    const workingMemory = createWorkingMemoryModule({ api, config: config.workingMemory, state, logger });
    const assimilation = createAssimilationModule({ api, config: config.assimilation, state, logger, llmConfig: config.llm });

    // 注册所有 Hooks 和服务
    metacognition.register();
    workingMemory.register();
    assimilation.register();

    logger.info(`[${pluginId}] 全部模块已注册`);
  }
};
