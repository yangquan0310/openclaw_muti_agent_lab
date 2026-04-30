/**
 * FlowAdapter — 任务流适配器（聚合 JSON 文件版）
 * 使用 ~/.openclaw/flows/agent-self-development/flows.json
 */

import { writeFileSync, readFileSync, existsSync, mkdirSync } from 'fs';
import { dirname } from 'path';

const DEFAULT_DIR = '/root/.openclaw/flows/agent-self-development';

function ensureDir(dir) {
  try { mkdirSync(dir, { recursive: true }); } catch {}
}

function loadJson(path) {
  if (!existsSync(path)) return {};
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return {};
  }
}

function saveJson(path, data) {
  ensureDir(dirname(path));
  writeFileSync(path, JSON.stringify(data, null, 2), 'utf8');
}

export class FlowAdapter {
  constructor(api, options = {}) {
    this.api = api;
    this.dir = options.dir || DEFAULT_DIR;
    this.file = `${this.dir}/flows.json`;
    ensureDir(this.dir);
  }

  async createPlanFlow(plan) {
    const flowId = `plan-${plan.runId}`;
    const flow = {
      flowId,
      controllerId: 'agent-self-development/planning',
      goal: plan.context?.goal || '',
      currentStep: 'draft',
      createdAt: Date.now(),
      updatedAt: Date.now(),
      revision: 1,
      stateJson: {
        plan,
        phases: plan.execution?.phases || [],
        currentPhase: 0,
        status: 'draft'
      }
    };
    if (this.api?.create) await this.api.create(flow);
    const data = loadJson(this.file);
    data[flowId] = flow;
    saveJson(this.file, data);
    return flow;
  }

  async get(flowId) {
    if (this.api?.get) {
      const apiResult = await this.api.get(flowId);
      if (apiResult) return apiResult;
    }
    return loadJson(this.file)[flowId] || null;
  }

  async advancePhase(flowId, phase) {
    const data = loadJson(this.file);
    const flow = data[flowId];
    if (!flow) return null;
    flow.currentStep = phase.id || flow.currentStep;
    flow.updatedAt = Date.now();
    flow.revision = (flow.revision || 1) + 1;
    flow.stateJson.currentPhase = (flow.stateJson.currentPhase || 0) + 1;
    if (this.api?.update) {
      await this.api.update({ flowId, expectedRevision: flow.revision - 1, currentStep: flow.currentStep, stateJson: flow.stateJson });
    }
    data[flowId] = flow;
    saveJson(this.file, data);
    return flow;
  }

  async waitForApproval(flowId) {
    const data = loadJson(this.file);
    const flow = data[flowId];
    if (!flow) return null;
    flow.currentStep = 'pending_approval';
    flow.updatedAt = Date.now();
    flow.revision = (flow.revision || 1) + 1;
    flow.stateJson.status = 'pending_approval';
    if (this.api?.setWaiting) {
      await this.api.setWaiting({ flowId, expectedRevision: flow.revision - 1, currentStep: 'pending_approval', waitJson: { kind: 'user_confirm', reason: 'Plan pending approval' } });
    }
    data[flowId] = flow;
    saveJson(this.file, data);
    return flow;
  }

  async getByRunId(runId) {
    const data = loadJson(this.file);
    for (const flow of Object.values(data)) {
      if (flow.stateJson?.plan?.runId === runId) return flow;
    }
    return null;
  }

  async getByPhase(phaseId) {
    const data = loadJson(this.file);
    for (const flow of Object.values(data)) {
      const phases = flow.stateJson?.phases || [];
      if (phases.some(p => p.id === phaseId)) return flow;
    }
    return null;
  }

  async runSubtask(flowId, phase) {
    console.log(`[FlowAdapter] runSubtask: ${flowId} phase=${phase?.id}`);
    return null;
  }
}
