/**
 * MemoryAdapter — 记忆存储适配器
 * 封装核心 Memory API
 */

export class MemoryAdapter {
  constructor(memoryAPI) {
    this.memory = memoryAPI;
  }

  async archiveSession(session) {
    await this.memory.archive({
      type: 'session',
      data: session,
      tags: [session.status, session.taskFamily],
      date: new Date()
    });
  }

  async logEvent(event) {
    await this.memory.archive({
      type: 'event',
      data: event,
      tags: [event.type, event.severity],
      date: new Date()
    });
  }

  // EventLog — 按日聚合的事件列表
  async appendEventLog(date, event) {
    const key = `event:${date}`;
    const existing = (await this.memory.get?.(key)) || [];
    existing.push(event);
    await this.memory.set?.(key, existing);
  }

  async getEventLog(date) {
    return this.memory.get?.(`event:${date}`) || [];
  }

  // Diary
  async saveDiary(date, diary) {
    await this.memory.set?.(`diary:${date}`, diary);
  }

  async getDiary(date) {
    return this.memory.get?.(`diary:${date}`);
  }

  async queryHistory(options) {
    return this.memory.query({
      type: options.type,
      tags: options.tags,
      dateRange: options.dateRange
    });
  }
}
