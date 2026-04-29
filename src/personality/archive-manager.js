/**
 * ArchiveManager — 归档管理器
 * 组合 MemoryAdapter + LogAdapter，负责 daily summary 和归档
 */

export class ArchiveManager {
  constructor(memory, log) {
    this.memory = memory;
    this.log = log;
  }

  async archivePlan(plan) {
    await this.memory.archiveSession({
      type: 'plan',
      data: plan,
      tags: [plan.status, 'plan'],
      date: new Date()
    });
  }

  async dailySummary(date) {
    const startOfDay = new Date(date);
    startOfDay.setHours(0, 0, 0, 0);
    const endOfDay = new Date(date);
    endOfDay.setHours(23, 59, 59, 999);

    const archives = await this.memory.queryHistory({
      type: 'session',
      dateRange: [startOfDay, endOfDay]
    });

    return {
      date,
      totalSessions: archives.length,
      completedSessions: archives.filter(a => a.data.status === 'completed').length,
      failedSessions: archives.filter(a => a.data.status === 'killed').length,
      items: archives
    };
  }
}
