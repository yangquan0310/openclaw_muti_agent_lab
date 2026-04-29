/**
 * FlowAdapter — 任务流适配器
 * 封装核心 Flow，实现计划工作流管理
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
    const flow = await this.taskFlow.get(flowId);
    await this.taskFlow.update({
      flowId,
      expectedRevision: flow.revision,
      currentStep: phase.id,
      stateJson: {
        ...flow.stateJson,
        currentPhase: flow.stateJson.currentPhase + 1
      }
    });
  }

  async waitForApproval(flowId) {
    const flow = await this.taskFlow.get(flowId);
    await this.taskFlow.setWaiting({
      flowId,
      expectedRevision: flow.revision,
      currentStep: 'pending_approval',
      waitJson: { kind: 'user_confirm', reason: 'Plan pending approval' }
    });
  }

  async runSubtask(flowId, phase) {
    // TODO: implement subtask execution via TaskFlow
  }

  async getByRunId(runId) {
    // TODO: lookup flow by runId
  }

  async getByPhase(phaseId) {
    // TODO: lookup flow by phaseId
  }
}
