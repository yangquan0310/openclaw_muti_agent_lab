/**
 * FlowAdapter — 任务流适配器
 * 封装核心 Flow API，实现计划工作流管理
 */

export class FlowAdapter {
  constructor(flowAPI) {
    this.flow = flowAPI;
  }

  async createPlanFlow(plan) {
    return this.flow.createManaged({
      controllerId: 'agent-self-development/planning',
      goal: plan.context.goal,
      currentStep: 'draft',
      stateJson: {
        plan,
        phases: plan.execution.phases,
        currentPhase: 0,
        status: 'draft'
      }
    });
  }

  async advancePhase(flowId, phase) {
    const f = await this.flow.get(flowId);
    await this.flow.update({
      flowId,
      expectedRevision: f.revision,
      currentStep: phase.id,
      stateJson: {
        ...f.stateJson,
        currentPhase: f.stateJson.currentPhase + 1
      }
    });
  }

  async waitForApproval(flowId) {
    const f = await this.flow.get(flowId);
    await this.flow.setWaiting({
      flowId,
      expectedRevision: f.revision,
      currentStep: 'pending_approval',
      waitJson: { kind: 'user_confirm', reason: 'Plan pending approval' }
    });
  }

  async getByRunId(runId) {
    // TODO: lookup flow by runId
  }

  async getByPhase(phaseId) {
    // TODO: lookup flow by phaseId
  }
}
