/**
 * MemoryAdapter — 记忆存储适配器（SQLite 版）
 * 使用 ~/.openclaw/memory/agent-self-development/memory.db
 */

import { join } from 'path';

const DEFAULT_DIR = '/root/.openclaw/memory';

// 动态导入 better-sqlite3（兼容 ESM）
let Database;
async function getDatabase() {
  if (!Database) {
    const module = await import('better-sqlite3');
    Database = module.default || module;
  }
  return Database;
}

export class MemoryAdapter {
  constructor(api, options = {}) {
    this.api = api;
    this.dir = options.dir || DEFAULT_DIR;
    this.dbPath = join(this.dir, 'agent-self-development', 'memory.db');
    this._db = null;
  }

  async _init() {
    const Database = await getDatabase();
    const db = new Database(this.dbPath);
    db.exec(`
      CREATE TABLE IF NOT EXISTS archives (
        id TEXT PRIMARY KEY,
        type TEXT NOT NULL,
        data TEXT NOT NULL,
        tags TEXT,
        archived_at TEXT
      );
      CREATE TABLE IF NOT EXISTS events (
        id TEXT PRIMARY KEY,
        type TEXT NOT NULL,
        data TEXT NOT NULL,
        tags TEXT,
        logged_at TEXT
      );
      CREATE TABLE IF NOT EXISTS eventlogs (
        date TEXT PRIMARY KEY,
        events TEXT NOT NULL
      );
      CREATE TABLE IF NOT EXISTS diaries (
        date TEXT PRIMARY KEY,
        content TEXT NOT NULL
      );
    `);
    db.close();
  }

  async _getDb() {
    if (!this._db) {
      const Database = await getDatabase();
      this._db = new Database(this.dbPath);
    }
    return this._db;
  }

  async archiveSession(session) {
    await this._init();
    const id = session.sessionId || `session-${Date.now()}`;
    const record = {
      type: 'session',
      data: JSON.stringify(session),
      tags: JSON.stringify([session.status, session.taskFamily]),
      archived_at: new Date().toISOString()
    };
    if (this.api?.archive) await this.api.archive({ type: 'session', data: session, tags: [session.status, session.taskFamily], date: new Date() });
    const db = await this._getDb();
    db.prepare('INSERT OR REPLACE INTO archives (id, type, data, tags, archived_at) VALUES (?, ?, ?, ?, ?)').run(id, record.type, record.data, record.tags, record.archived_at);
  }

  async logEvent(event) {
    await this._init();
    const id = event.eventId || `event-${Date.now()}`;
    const record = {
      type: event.type || 'event',
      data: JSON.stringify(event),
      tags: JSON.stringify([event.type, event.severity || 'info']),
      logged_at: new Date().toISOString()
    };
    if (this.api?.archive) await this.api.archive({ type: 'event', data: event, tags: [event.type, event.severity || 'info'], date: new Date() });
    const db = await this._getDb();
    db.prepare('INSERT OR REPLACE INTO events (id, type, data, tags, logged_at) VALUES (?, ?, ?, ?, ?)').run(id, record.type, record.data, record.tags, record.logged_at);
  }

  async appendEventLog(date, event) {
    await this._init();
    const db = await this._getDb();
    const existing = db.prepare('SELECT events FROM eventlogs WHERE date = ?').get(date);
    const events = existing ? JSON.parse(existing.events) : [];
    events.push(event);
    db.prepare('INSERT OR REPLACE INTO eventlogs (date, events) VALUES (?, ?)').run(date, JSON.stringify(events));
    if (this.api?.set) await this.api.set(`event:${date}`, events);
  }

  async getEventLog(date) {
    if (this.api?.get) {
      const mem = await this.api.get(`event:${date}`);
      if (mem && Array.isArray(mem)) return mem;
    }
    await this._init();
    const db = await this._getDb();
    const row = db.prepare('SELECT events FROM eventlogs WHERE date = ?').get(date);
    return row ? JSON.parse(row.events) : [];
  }

  async saveDiary(date, diary) {
    if (this.api?.set) await this.api.set(`diary:${date}`, diary);
    await this._init();
    const db = await this._getDb();
    db.prepare('INSERT OR REPLACE INTO diaries (date, content) VALUES (?, ?)').run(date, JSON.stringify(diary));
  }

  async getDiary(date) {
    if (this.api?.get) {
      const mem = await this.api.get(`diary:${date}`);
      if (mem) return mem;
    }
    await this._init();
    const db = await this._getDb();
    const row = db.prepare('SELECT content FROM diaries WHERE date = ?').get(date);
    return row ? JSON.parse(row.content) : null;
  }

  async queryHistory(options) {
    await this._init();
    const results = [];
    const db = await this._getDb();
    
    if (!options.type || options.type === 'archives') {
      const rows = db.prepare('SELECT data FROM archives').all();
      results.push(...rows.map(r => JSON.parse(r.data)));
    }
    if (!options.type || options.type === 'events') {
      const rows = db.prepare('SELECT data FROM events').all();
      results.push(...rows.map(r => JSON.parse(r.data)));
    }
    
    return results;
  }
}
