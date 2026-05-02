/**
 * StateAdapter — 状态存储适配器（统一 task JSON 版）
 * 使用 ~/.openclaw/state/agent-self-development/{type}.json
 *
 * 统一设计：一个任务一个 JSON（task:{runId}），包含 Plan + Event + Sessions + Tools
 * Session 全局管理（sessions.json）
 *
 * v3.3.0 归档策略：completed 任务移至 archive/tasks_archive.json，保留最近 50 个
 */

import { writeFileSync, readFileSync, existsSync, mkdirSync } from 'fs';
import { dirname, join } from 'path';

const DEFAULT_DIR = '/root/.openclaw/state/agent-self-development';
const ARCHIVE_DIR = 'archive';
const MAX_ARCHIVED_TASKS = 50;

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

export class StateAdapter {
  constructor(api, options = {}) {
    this.api = api;
    this.dir = options.dir || DEFAULT_DIR;
    ensureDir(this.dir);
    ensureDir(join(this.dir, ARCHIVE_DIR));
  }

  _file(type) {
    return `${this.dir}/${type}.json`;
  }

  _archiveFile() {
    return join(this.dir, ARCHIVE_DIR, 'tasks_archive.json');
  }

  _get(type, key) {
    const data = loadJson(this._file(type));
    return data[key];
  }

  _set(type, key, value) {
    const path = this._file(type);
    const data = loadJson(path);
    if (value === null || value === undefined) {
      delete data[key];
    } else {
      data[key] = value;
    }
    saveJson(path, data);
  }

  _list(type, prefix) {
    const data = loadJson(this._file(type));
    return Object.entries(data)
      .filter(([k]) => !prefix || k.startsWith(prefix))
      .map(([, v]) => v);
  }

  // ── Task（统一聚合 JSON）──

  async saveTask(runId, task) {
    if (this.api?.set) await this.api.set(`task:${runId}`, task);
    this._set('tasks', runId, task);
  }

  async getTask(runId) {
    if (this.api?.get) {
      const mem = await this.api.get(`task:${runId}`);
      if (mem !== undefined && mem !== null) return mem;
    }
    return this._get('tasks', runId);
  }

  async deleteTask(runId) {
    if (this.api?.set) await this.api.set(`task:${runId}`, null);
    this._set('tasks', runId, null);
  }

  async listTasks() {
    return this._list('tasks');
  }

  /**
   * 归档已完成的任务：从 tasks.json 移至 archive/tasks_archive.json
   * 并清理超过 MAX_ARCHIVED_TASKS 的旧归档
   */
  async archiveTask(runId) {
    const task = await this.getTask(runId);
    if (!task) return false;

    // 只归档 completed 状态的任务
    if (task.status !== 'completed') {
      return false;
    }

    const archivePath = this._archiveFile();
    const archiveData = loadJson(archivePath);

    // 添加归档时间戳
    const archivedTask = {
      ...task,
      archivedAt: new Date().toISOString()
    };

    archiveData[runId] = archivedTask;
    saveJson(archivePath, archiveData);

    // 从活跃任务中删除
    await this.deleteTask(runId);

    // 清理旧归档，保留最近 50 个
    await this._cleanupOldArchives();

    return true;
  }

  /**
   * 获取已归档的任务
   */
  async getArchivedTask(runId) {
    const archiveData = loadJson(this._archiveFile());
    return archiveData[runId] || null;
  }

  /**
   * 列出所有已归档的任务
   */
  async listArchivedTasks() {
    const archiveData = loadJson(this._archiveFile());
    return Object.values(archiveData);
  }

  /**
   * 清理旧归档：按 archivedAt 排序，只保留最近 50 个
   */
  async _cleanupOldArchives() {
    const archivePath = this._archiveFile();
    const archiveData = loadJson(archivePath);
    const entries = Object.entries(archiveData);

    if (entries.length <= MAX_ARCHIVED_TASKS) return;

    // 按 archivedAt 升序排序，删除最旧的
    const sorted = entries.sort((a, b) => {
      const tA = new Date(a[1].archivedAt || 0).getTime();
      const tB = new Date(b[1].archivedAt || 0).getTime();
      return tA - tB;
    });

    const toDelete = sorted.slice(0, sorted.length - MAX_ARCHIVED_TASKS);
    for (const [key] of toDelete) {
      delete archiveData[key];
    }

    saveJson(archivePath, archiveData);
  }

  // ── Session（全局，跨任务复用）──

  async saveSession(sessionId, session) {
    if (this.api?.set) await this.api.set(`session:${sessionId}`, session);
    this._set('sessions', sessionId, session);
  }

  async getSession(sessionId) {
    if (this.api?.get) {
      const mem = await this.api.get(`session:${sessionId}`);
      if (mem !== undefined && mem !== null) return mem;
    }
    return this._get('sessions', sessionId);
  }

  async deleteSession(sessionId) {
    if (this.api?.set) await this.api.set(`session:${sessionId}`, null);
    this._set('sessions', sessionId, null);
  }

  async listSessions() {
    return this._list('sessions');
  }

  async listSessionsByStatus(status) {
    const all = await this.listSessions();
    return all.filter(s => s.status === status);
  }
}
