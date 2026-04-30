/**
 * TaskAdapter — 任务适配器（聚合 JSON 文件版）
 * 使用 ~/.openclaw/tasks/agent-self-development/tasks.json
 */

import { writeFileSync, readFileSync, existsSync, mkdirSync } from 'fs';
import { dirname } from 'path';

const DEFAULT_DIR = '/root/.openclaw/tasks/agent-self-development';

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

export class TaskAdapter {
  constructor(api, options = {}) {
    this.api = api;
    this.dir = options.dir || DEFAULT_DIR;
    this.file = `${this.dir}/tasks.json`;
    ensureDir(this.dir);
  }

  async createTask(task) {
    const taskId = task.id || `task-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
    const record = { ...task, id: taskId, createdAt: task.createdAt || new Date().toISOString(), updatedAt: new Date().toISOString() };
    if (this.api?.create) await this.api.create(record);
    const data = loadJson(this.file);
    data[taskId] = record;
    saveJson(this.file, data);
    return record;
  }

  async getTask(taskId) {
    if (this.api?.get) {
      const apiResult = await this.api.get(taskId);
      if (apiResult) return apiResult;
    }
    return loadJson(this.file)[taskId] || null;
  }

  async updateTask(taskId, updates) {
    const existing = await this.getTask(taskId);
    if (!existing) return null;
    const updated = { ...existing, ...updates, updatedAt: new Date().toISOString() };
    if (this.api?.update) await this.api.update(taskId, updates);
    const data = loadJson(this.file);
    data[taskId] = updated;
    saveJson(this.file, data);
    return updated;
  }

  async deleteTask(taskId) {
    if (this.api?.delete) await this.api.delete(taskId);
    const data = loadJson(this.file);
    delete data[taskId];
    saveJson(this.file, data);
  }

  async listTasks() {
    return Object.values(loadJson(this.file));
  }
}
