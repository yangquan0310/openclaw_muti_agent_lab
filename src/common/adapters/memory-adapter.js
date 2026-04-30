/**
 * MemoryAdapter — 记忆存储适配器（聚合 JSON 文件版）
 * 使用 ~/.openclaw/memory/agent-self-development/{type}.json
 */

import { writeFileSync, readFileSync, existsSync, mkdirSync } from 'fs';
import { dirname } from 'path';

const DEFAULT_DIR = '/root/.openclaw/memory/agent-self-development';

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

export class MemoryAdapter {
  constructor(api, options = {}) {
    this.api = api;
    this.dir = options.dir || DEFAULT_DIR;
    ensureDir(this.dir);
  }

  _file(type) {
    return `${this.dir}/${type}.json`;
  }

  async archiveSession(session) {
    const id = session.sessionId || `session-${Date.now()}`;
    const record = {
      type: 'session',
      data: session,
      tags: [session.status, session.taskFamily],
      archivedAt: new Date().toISOString()
    };
    if (this.api?.archive) await this.api.archive(record);
    const path = this._file('archives');
    const data = loadJson(path);
    data[id] = record;
    saveJson(path, data);
  }

  async logEvent(event) {
    const id = event.eventId || `event-${Date.now()}`;
    const record = {
      type: 'event',
      data: event,
      tags: [event.type, event.severity || 'info'],
      loggedAt: new Date().toISOString()
    };
    if (this.api?.archive) await this.api.archive(record);
    const path = this._file('events');
    const data = loadJson(path);
    data[id] = record;
    saveJson(path, data);
  }

  async appendEventLog(date, event) {
    const path = this._file('eventlogs');
    const data = loadJson(path);
    if (!data[date]) data[date] = [];
    data[date].push(event);
    if (this.api?.set) await this.api.set(`event:${date}`, data[date]);
    saveJson(path, data);
  }

  async getEventLog(date) {
    if (this.api?.get) {
      const mem = await this.api.get(`event:${date}`);
      if (mem && Array.isArray(mem)) return mem;
    }
    return loadJson(this._file('eventlogs'))[date] || [];
  }

  async saveDiary(date, diary) {
    if (this.api?.set) await this.api.set(`diary:${date}`, diary);
    const path = this._file('diaries');
    const data = loadJson(path);
    data[date] = diary;
    saveJson(path, data);
  }

  async getDiary(date) {
    if (this.api?.get) {
      const mem = await this.api.get(`diary:${date}`);
      if (mem) return mem;
    }
    return loadJson(this._file('diaries'))[date] || null;
  }

  async queryHistory(options) {
    const results = [];
    const types = options.type ? [options.type] : ['archives', 'events', 'eventlogs', 'diaries'];
    for (const type of types) {
      const data = loadJson(this._file(type));
      for (const record of Object.values(data)) {
        if (options.tags && !options.tags.some(t => (record.tags || []).includes(t))) continue;
        if (options.dateRange) {
          const date = new Date(record.archivedAt || record.loggedAt || record.updatedAt || 0);
          const start = new Date(options.dateRange.start);
          const end = new Date(options.dateRange.end);
          if (date < start || date > end) continue;
        }
        results.push(record.data || record);
      }
    }
    return results;
  }
}
