/**
 * OpenClaw Agent Self-Development Plugin
 *
 * 纯钩子框架 —— 只注入提醒，不涉及操作。
 * Agent 自行决策：偏差判断、文件读写、同化顺应分析、置信度评估。
 */

import { definePluginEntry } from 'openclaw/plugin-sdk/plugin-entry';
import { PluginState } from './state.js';
import { createMetacognitionModule } from './metacognition.js';
import { createWorkingMemoryModule } from './working-memory.js';
import { createAssimilationModule } from './assimilation.js';

export default definePluginEntry({
  id: 'agent-self-development',
  name: 'Agent Self-Development',
  version: '1.2.3',

  register(api) {
    if (api.registrationMode && api.registrationMode !== 'full') {
      return;
    }

    const pluginId = 'agent-self-development';
    const config = api.pluginConfig || {};
    const state = new PluginState(pluginId);
    const logger = api.logger || console;

    logger.info(`[${pluginId}] Agent Self-Development Plugin v1.2.3 activated`);

    // 检查 conversation hooks 权限
    const entries = api.config?.plugins?.entries?.[pluginId];
    if (entries?.hooks?.allowConversationAccess !== true) {
      logger.warn(`[${pluginId}] ⚠️ allowConversationAccess 未启用，元认知功能可能无法工作`);
    }

    const metacognition = createMetacognitionModule({ api, config: config.metacognition, state, logger });
    const workingMemory = createWorkingMemoryModule({ api, config: config.workingMemory, state, logger });
    const assimilation = createAssimilationModule({ api, config: config.assimilation, state, logger });

    metacognition.register();
    workingMemory.register();
    assimilation.register();

    logger.info(`[${pluginId}] 全部模块已注册`);
  }
});
