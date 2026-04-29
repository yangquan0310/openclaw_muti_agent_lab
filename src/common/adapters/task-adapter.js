/**
 * TaskAdapter — 任务适配器
 * 封装核心 Task API
 */

export class TaskAdapter {
  constructor(taskAPI) {
    this.task = taskAPI;
  }

  async createTask(task) {
    return this.task.create(task);
  }

  async getTask(taskId) {
    return this.task.get(taskId);
  }

  async updateTask(taskId, updates) {
    return this.task.update(taskId, updates);
  }

  async deleteTask(taskId) {
    return this.task.delete(taskId);
  }
}
