/**
 * StateAdapter — 状态存储适配器（聚合 JSON 文件版）
 * 使用 ~/.openclaw/state/agent-self-development/{type}.json
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

  // Plan
  async savePlan(runId, plan) {
    if (this.api?.set) await this.api.set(`plan:${runId}`, plan);
    this._set('plans', runId, plan);
  }

  async getPlan(runId) {
    if (this.api?.get) {
      const mem = await this.api.get(`plan:${runId}`);
      if (mem !== undefined && mem !== null) return mem;
    }
    return this._get('plans', runId);
  }

  // Session
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

  // Deviation
  async saveDeviation(runId, phaseId, deviation) {
    const key = `${runId}:${phaseId}`;
    if (this.api?.set) await this.api.set(`deviation:${key}`, deviation);
    this._set('deviations', key, deviation);
  }

  async getDeviation(runId, phaseId) {
    const key = `${runId}:${phaseId}`;
    if (this.api?.get) {
      const mem = await this.api.get(`deviation:${key}`);
      if (mem !== undefined && mem !== null) return mem;
    }
    return this._get('deviations', key);
  }

  async listDeviationsByRunId(runId) {
    return this._list('deviations', `${runId}:`);
  }

  // Attribution
  async saveAttribution(runId, deviationId, attribution) {
    const key = `${runId}:${deviationId}`;
    if (this.api?.set) await this.api.set(`attribution:${key}`, attribution);
    this._set('attributions', key, attribution);
  }

  async getAttribution(runId, deviationId) {
    const key = `${runId}:${deviationId}`;
    if (this.api?.get) {
      const mem = await this.api.get(`attribution:${key}`);
      if (mem !== undefined && mem !== null) return mem;
    }
    return this._get('attributions', key);
  }

  // Event
  async saveEvent(eventId, event) {
    if (this.api?.set) await this.api.set(`event:${eventId}`, event);
    this._set('events', eventId, event);
  }

  async getEvent(eventId) {
    if (this.api?.get) {
      const mem = await this.api.get(`event:${eventId}`);
      if (mem !== undefined && mem !== null) return mem;
    }
    return this._get('events', eventId);
  }

  async deleteEvent(eventId) {
    if (this.api?.set) await this.api.set(`event:${eventId}`, null);
    this._set('events', eventId, null);
  }

  async listEvents() {
    return this._list('events');
  }
}
