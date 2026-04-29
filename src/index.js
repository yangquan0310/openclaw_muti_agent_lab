/**
 * OpenClaw Agent Self-Development Plugin
 *
 * 纯钩子框架——只注入提醒，不涉及操作
 * Agent 自行决策：偏差判断、文件读写、同化顺应分析、置信度评估
 */

import { MetacognitionModule } from './metacognition/module.js';
import { WorkingMemoryModule } from './working-memory/module.js';
import { PersonalityModule } from './personality/module.js';
import { SkillLoader } from './common/skills-loader.js';

// v3 adapters
import { StateAdapter } from './common/adapters/state-adapter.js';
import { TaskAdapter } from './common/adapters/task-adapter.js';
import { FlowAdapter } from './common/adapters/flow-adapter.js';
import { MemoryAdapter } from './common/adapters/memory-adapter.js';
import { LogAdapter } from './common/adapters/log-adapter.js';

// v3 managers
import { PlanManager } from './metacognition/plan-manager.js';
import { DeviationManager } from './metacognition/deviation-manager.js';
import { AttributionManager } from './metacognition/attribution-manager.js';
import { SessionManager } from './working-memory/session-manager.js';
import { EventManager } from './personality/event-manager.js';
import { DiaryManager } from './personality/diary-manager.js';

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
    const taskAdapter = new TaskAdapter(runtime.tasks);
    const flowAdapter = new FlowAdapter(runtime.flow);
    const memoryAdapter = new MemoryAdapter(runtime.memory);
    const logAdapter = new LogAdapter(runtime.log);

    // v3: 初始化业务管理器
    const planManager = new PlanManager(stateAdapter, flowAdapter);
    const deviationManager = new DeviationManager(stateAdapter);
    const attributionManager = new AttributionManager(stateAdapter, flowAdapter);
    const sessionManager = new SessionManager(stateAdapter, flowAdapter, runtime.sessions);
    const eventManager = new EventManager(stateAdapter, memoryAdapter);
    const diaryManager = new DiaryManager(memoryAdapter);

    const metacognition = new MetacognitionModule({
      api, config: config.metacognition, stateAdapter, skillLoader, logger,
      planManager, deviationManager, attributionManager
    });
    const workingMemory = new WorkingMemoryModule({
      api, config: config.workingMemory, stateAdapter, skillLoader, logger,
      sessionManager, eventManager
    });
    const personality = new PersonalityModule({
      api, config: config.personality || config.assimilation, stateAdapter, skillLoader, logger,
      eventManager, diaryManager
    });

    metacognition.register();
    workingMemory.register();
    personality.register();

    logger.info(`[${pluginId}] 全部模块已注册（元认知 / 工作记忆 / 人格）`);
  }
};
