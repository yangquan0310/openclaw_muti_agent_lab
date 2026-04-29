/**
 * EventManager — 事件业务逻辑
 * 管理 Event 对象：记录各阶段执行事件，agent_end 时聚合到 EventLog
 */

export class EventManager {
  constructor(stateAdapter, memoryAdapter) {
    this.stateAdapter = stateAdapter;
    this.memoryAdapter = memoryAdapter;
  }

  /**
   * 记录单次事件（存 State，临时）
   */
  async recordEvent(eventData) {
    const eventId = `evt-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
    const event = {
      eventId,
      timestamp: Date.now(),
      ...eventData
    };
    await this.stateAdapter.saveEvent(eventId, event);
    return event;
  }

  /**
   * 获取单个事件
   */
  async getEvent(eventId) {
    return this.stateAdapter.getEvent(eventId);
  }

  /**
   * agent_end 时：把 State 中所有 Event 聚合到 Memory EventLog
   */
  async aggregateEvents(runId) {
    const events = await this.stateAdapter.listEvents();
    const date = new Date().toISOString().slice(0, 10);

    for (const event of events) {
      await this.memoryAdapter.appendEventLog(date, {
        ...event,
        runId,
        aggregatedAt: Date.now()
      });
      await this.stateAdapter.deleteEvent(event.eventId);
    }

    return { transferred: events.length, date };
  }

  /**
   * 查询某日的 EventLog
   */
  async queryEventLog(date) {
    return this.memoryAdapter.getEventLog(date);
  }
}
