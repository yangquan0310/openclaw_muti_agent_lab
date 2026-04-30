/**
 * OpenClaw Agent Self-Development Plugin
 *
 * 纯钩子框架——只注入提醒，不涉及操作
 * Agent 自行决策：偏差判断、文件读写、同化顺应分析、置信度评估
 */

import { dirname } from 'path';

import { StateAdapter } from './common/adapters/state-adapter.js';
import { TaskAdapter } from './common/adapters/task-adapter.js';
import { FlowAdapter } from './common/adapters/flow-adapter.js';
import { MemoryAdapter } from './common/adapters/memory-adapter.js';
import { LogAdapter } from './common/adapters/log-adapter.js';
import { HookAdapter } from './common/adapters/hook-adapter.js';
import { CronAdapter } from './common/adapters/cron-adapter.js';

import { MetacognitionModule } from './metacognition/module.js';
import { WorkingMemoryModule } from './working-memory/module.js';
import { PersonalityModule } from './personality/module.js';
import { SkillLoader } from './common/skills-loader.js';

// v3 managers
import { PlanManager } from './metacognition/plan-manager.js';
import { DeviationManager } from './metacognition/deviation-manager.js';
import { AttributionManager } from './metacognition/attribution-manager.js';
import { SessionManager } from './working-memory/session-manager.js';
import { EventManager } from './common/event-manager.js';
import { DiaryManager } from './personality/diary-manager.js';

const pluginId = 'agent-self-development';

export default {
  id: pluginId,
  name: 'Agent Self-Development',
  version: '3.2.1',
  description: 'OpenClaw plugin for agent self-development based on Piaget\'s cognitive development theory',

  register(api) {
    if (api.registrationMode && api.registrationMode !== 'full') {
      return;
    }

    const config = api.pluginConfig || {};
    const skillLoader = new SkillLoader();
    const logger = api.logger || console;

    logger.info(`[${pluginId}] Agent Self-Development Plugin v3.2.1 activated`);

    // 检查 conversation hooks 权限
    // OpenClaw 2026.4.21 版本使用 allowPromptInjection 控制对话访问
    const entries = api.config?.plugins?.entries?.[pluginId];
    const hooks = entries?.hooks || {};
    if (hooks.allowConversationAccess !== true && hooks.allowPromptInjection !== true) {
      logger.warn(`[${pluginId}] ⚠️ allowConversationAccess / allowPromptInjection 未启用，元认知功能可能无法工作`);
    }

    // B方案：使用聚合 JSON 文件，参照 OpenClaw 核心文件格式
    const runtime = api.runtime || {};
    const baseDir = runtime.state?.resolveStateDir
      ? dirname(runtime.state.resolveStateDir())
      : '/root/.openclaw';

    // 获取当前代理ID
    const agentId = api.agentId || 'main';
    
    // 使用当前代理的数据库文件
    // 使用已有的系统数据库
    const stateAdapter = new StateAdapter(null, { dir: `${baseDir}/state/agent-self-development` });
    const taskAdapter = new TaskAdapter(null, { dbPath: `${baseDir}/tasks/runs.sqlite` });
    const flowAdapter = new FlowAdapter(null, { dbPath: `${baseDir}/flows/registry.sqlite` });
    const memoryAdapter = new MemoryAdapter(null, { dbPath: `${baseDir}/memory/${agentId}.sqlite` });
    const logAdapter = new LogAdapter(null, { 
      dir: `${baseDir}/logs`, 
      agentId: agentId 
    });
    const hookAdapter = new HookAdapter(null, { dir: `${baseDir}/hooks/agent-self-development` });
    const cronAdapter = new CronAdapter({ path: `${baseDir}/cron/jobs.json` });

    // 初始化 Hook 目录结构（HOOK.md + handler.ts）
    hookAdapter.init().catch(e => logger.warn(`[${pluginId}] Hook 初始化失败:`, e.message));

    // v3: 初始化业务管理器
    const planManager = new PlanManager(stateAdapter, flowAdapter);
    const deviationManager = new DeviationManager(stateAdapter);
    const attributionManager = new AttributionManager(stateAdapter, flowAdapter);
    const sessionManager = new SessionManager(stateAdapter, flowAdapter, null);
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
