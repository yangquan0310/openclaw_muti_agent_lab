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

  async queryHistory(options) {
    return this.memory.query({
      type: options.type,
      tags: options.tags,
      dateRange: options.dateRange
    });
  }
}
