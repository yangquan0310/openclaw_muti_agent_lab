/**
 * OpenClaw Agent Self-Development Plugin
 *
 * 纯钩子框架——只注入提醒，不涉及操作
 * Agent 自行决策：偏差判断、文件读写、同化顺应分析、置信度评估
 */

import { PluginState } from './common/state.js';
import { MetacognitionModule } from './metacognition/module.js';
import { WorkingMemoryModule } from './working-memory/module.js';
import { PersonalityModule } from './personality/module.js';
import { SkillLoader } from './common/skills-loader.js';

// v3 adapters
import { StateAdapter } from './common/adapters/state-adapter.js';
import { TaskFlowAdapter } from './common/adapters/taskflow-adapter.js';
import { MemoryAdapter } from './common/adapters/memory-adapter.js';
import { LogAdapter } from './common/adapters/log-adapter.js';

// v3 managers
import { PlanManager } from './metacognition/plan-manager.js';
import { SessionManager } from './working-memory/session-manager.js';
import { ArchiveManager } from './personality/archive-manager.js';

const pluginId = 'openclaw-agent-self-development';

export default {
  id: pluginId,
  name: 'Agent Self-Development',
  version: '3.0.0',
  description: 'OpenClaw plugin for agent self-development based on Piaget\'s cognitive development theory',

  register(api) {
    if (api.registrationMode && api.registrationMode !== 'full') {
      return;
    }

    const config = api.pluginConfig || {};
    const state = new PluginState(pluginId);
    const skillLoader = new SkillLoader();
    const logger = api.logger || console;

    logger.info(`[${pluginId}] Agent Self-Development Plugin v3.0.0 activated`);

    // 检查 conversation hooks 权限
    const entries = api.config?.plugins?.entries?.[pluginId];
    if (entries?.hooks?.allowConversationAccess !== true) {
      logger.warn(`[${pluginId}] ⚠️ allowConversationAccess 未启用，元认知功能可能无法工作`);
    }

    // v3: 初始化核心系统适配器
    const runtime = api.runtime || {};
    const stateAdapter = new StateAdapter(runtime.state);
    const taskFlowAdapter = new TaskFlowAdapter(runtime.tasks?.flow);
    const memoryAdapter = new MemoryAdapter(runtime.memory);
    const logAdapter = new LogAdapter(runtime.log);

    // v3: 初始化业务管理器
    const planManager = new PlanManager(stateAdapter, taskFlowAdapter);
    const sessionManager = new SessionManager(stateAdapter, taskFlowAdapter, runtime.sessions);
    const archiveManager = new ArchiveManager(memoryAdapter, logAdapter);

    const metacognition = new MetacognitionModule({
      api, config: config.metacognition, state, skillLoader, logger,
      planManager
    });
    const workingMemory = new WorkingMemoryModule({
      api, config: config.workingMemory, state, skillLoader, logger,
      sessionManager
    });
    const personality = new PersonalityModule({
      api, config: config.personality || config.assimilation, state, skillLoader, logger,
      archiveManager
    });

    metacognition.register();
    workingMemory.register();
    personality.register();

    logger.info(`[${pluginId}] 全部模块已注册（元认知 / 工作记忆 / 人格）`);
  }
};
