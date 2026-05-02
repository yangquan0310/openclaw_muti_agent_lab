/**
 * StateAdapter — 状态存储适配器（统一 task JSON 版）
 * 使用 ~/.openclaw/state/agent-self-development/{type}.json
 *
 * 统一设计：一个任务一个 JSON（task:{runId}），包含 Plan + Event + Sessions + Tools
 * Session 全局管理（sessions.json）
 */

import { writeFileSync, readFileSync, existsSync, mkdirSync } from 'fs';
import { dirname } from 'path';

const DEFAULT_DIR = '/root/.openclaw/state/agent-self-development';

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
  }

  _file(type) {
    return `${this.dir}/${type}.json`;
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
