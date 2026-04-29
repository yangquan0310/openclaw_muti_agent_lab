/**
 * PlanManager — 计划管理器
 * 组合 StateAdapter + TaskFlowAdapter，管理 Plan 全生命周期
 */

export class PlanManager {
  constructor(state, taskFlow) {
    this.state = state;
    this.taskFlow = taskFlow;
  }

  async createPlan(prompt) {
    const runId = crypto.randomUUID();
    const plan = {
      runId,
      prompt,
      status: 'draft',
      context: { goal: '', constraints: [], successCriteria: [] },
      workspace: { sessions: [], artifacts: [], tools: [], skills: [] },
      execution: { phases: [], currentPhase: 0 }
    };

    await this.state.savePlan(runId, plan);
    await this.taskFlow.createPlanFlow(plan);

    return plan;
  }

  async approvePlan(runId) {
    const plan = await this.state.getPlan(runId);
    if (!plan) throw new Error('Plan not found');

    plan.status = 'active';
    await this.state.savePlan(runId, plan);

    const flow = await this.taskFlow.getByRunId(runId);
    await this.taskFlow.advancePhase(flow.flowId, plan.execution.phases[0]);
  }

  async completePhase(runId, phaseIndex) {
    const plan = await this.state.getPlan(runId);
    if (!plan) throw new Error('Plan not found');

    plan.execution.phases[phaseIndex].status = 'completed';
    plan.execution.currentPhase = phaseIndex + 1;

    await this.state.savePlan(runId, plan);

    if (plan.execution.currentPhase >= plan.execution.phases.length) {
      plan.status = 'completed';
      await this.state.savePlan(runId, plan);
    } else {
      const nextPhase = plan.execution.phases[plan.execution.currentPhase];
      const flow = await this.taskFlow.getByRunId(runId);
      await this.taskFlow.advancePhase(flow.flowId, nextPhase);
    }
  }
}
