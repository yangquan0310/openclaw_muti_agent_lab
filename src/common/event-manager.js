/**
 * EventManager — 事件业务逻辑
 * 跨模块数据管道：agent_end 时将 task:{runId}.event 聚合到 Memory EventLog
 *
 * v3.3.0: 事件统一存储在 task:{runId}.event 中，不再使用独立的 event.json
 */

export class EventManager {
  constructor(stateAdapter, memoryAdapter) {
    this.stateAdapter = stateAdapter;
    this.memoryAdapter = memoryAdapter;
  }

  /**
   * agent_end 时：把 task:{runId}.event 聚合到 Memory EventLog
   */
  async aggregateEvents(runId) {
    const task = await this.stateAdapter.getTask(runId);
    if (!task || !task.event) {
      return { transferred: 0, date: null };
    }

    const date = new Date().toISOString().slice(0, 10);
    const eventLog = {
      runId,
      event: task.event,
      aggregatedAt: Date.now()
    };

    await this.memoryAdapter.appendEventLog(date, eventLog);

    return { transferred: 1, date, event: task.event };
  }

  /**
   * 查询某日的 EventLog
   */
  async queryEventLog(date) {
    return this.memoryAdapter.getEventLog(date);
  }
}
