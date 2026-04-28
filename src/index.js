/**
 * OpenClaw Agent Self-Development Plugin
 *
 * 纯钩子框架 —— 只注入提醒，不涉及操作。
 * Agent 自行决策：偏差判断、文件读写、同化顺应分析、置信度评估。
 */

import { definePluginEntry } from 'openclaw/plugin-sdk/plugin-entry';
import { PluginState } from './state.js';
import { MetacognitionModule } from './metacognition.js';
import { WorkingMemoryModule } from './working-memory.js';
import { PersonalityModule } from './personality.js';
import { SkillLoader } from './skills-loader.js';

export default definePluginEntry({
  id: 'agent-self-development',
  name: 'Agent Self-Development',
  version: '2.0.1',

  register(api) {
    if (api.registrationMode && api.registrationMode !== 'full') {
      return;
    }

    const pluginId = 'agent-self-development';
    const config = api.pluginConfig || {};
    const state = new PluginState(pluginId);
    const skillLoader = new SkillLoader();
    const logger = api.logger || console;

    logger.info(`[${pluginId}] Agent Self-Development Plugin v2.0.1 activated`);

    // 检查 conversation hooks 权限
    const entries = api.config?.plugins?.entries?.[pluginId];
    if (entries?.hooks?.allowConversationAccess !== true) {
      logger.warn(`[${pluginId}] ⚠️ allowConversationAccess 未启用，元认知功能可能无法工作`);
    }

    const metacognition = new MetacognitionModule({
      api, config: config.metacognition, state, skillLoader, logger
    });
    const workingMemory = new WorkingMemoryModule({
      api, config: config.workingMemory, state, skillLoader, logger
    });
    const personality = new PersonalityModule({
      api, config: config.personality || config.assimilation, state, skillLoader, logger
    });

    metacognition.register();
    workingMemory.register();
    personality.register();

    logger.info(`[${pluginId}] 全部模块已注册（元认知 / 工作记忆 / 人格）`);
  }
});
