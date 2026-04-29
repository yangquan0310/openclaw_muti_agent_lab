/**
 * StateAdapter — 状态存储适配器
 * 隔离核心 State API 变化，提供统一接口
 * 状态持久化到 /root/.openclaw/state/agent-self-development/
 */

import { writeFileSync, readFileSync, existsSync, mkdirSync, readdirSync, unlinkSync } from 'fs';
import { join } from 'path';

const STATE_DIR = '/root/.openclaw/state/agent-self-development';

function ensureDir() {
  if (!existsSync(STATE_DIR)) {
    mkdirSync(STATE_DIR, { recursive: true });
  }
}

function getPath(key) {
  ensureDir();
  // 将 key 中的特殊字符替换为安全文件名
  const safeKey = key.replace(/[^a-zA-Z0-9_-]/g, '_');
  return join(STATE_DIR, `${safeKey}.json`);
}

export class StateAdapter {
  constructor(stateAPI) {
    this.state = stateAPI;
  }

  async transaction(operations) {
    return this.state.transaction(operations);
  }

  // 持久化辅助方法
  _saveToFile(key, data) {
    const path = getPath(key);
    if (data === null || data === undefined) {
      if (existsSync(path)) {
        unlinkSync(path);
      }
      return;
    }
    writeFileSync(path, JSON.stringify(data, null, 2), 'utf8');
  }

  _loadFromFile(key) {
    const path = getPath(key);
    if (!existsSync(path)) return undefined;
    try {
      const content = readFileSync(path, 'utf8');
      return JSON.parse(content);
    } catch {
      return undefined;
    }
  }

  _deleteFile(key) {
    const path = getPath(key);
    if (existsSync(path)) {
      unlinkSync(path);
    }
  }

  _listFiles(prefix) {
    ensureDir();
    const files = readdirSync(STATE_DIR);
    const safePrefix = prefix.replace(/[^a-zA-Z0-9_-]/g, '_');
    return files
      .filter(f => f.startsWith(safePrefix) && f.endsWith('.json'))
      .map(f => join(STATE_DIR, f));
  }

  // Plan
  async savePlan(runId, plan) {
    const key = `plan:${runId}`;
    await this.state.set(key, plan);
    this._saveToFile(key, plan);
  }

  async getPlan(runId) {
    const key = `plan:${runId}`;
    const memory = await this.state.get(key);
    if (memory !== undefined) return memory;
    return this._loadFromFile(key);
  }

  // Session
  async saveSession(sessionId, session) {
    const key = `session:${sessionId}`;
    await this.state.set(key, session);
    this._saveToFile(key, session);
  }

  async getSession(sessionId) {
    const key = `session:${sessionId}`;
    const memory = await this.state.get(key);
    if (memory !== undefined) return memory;
    return this._loadFromFile(key);
  }

  async deleteSession(sessionId) {
    const key = `session:${sessionId}`;
    await this.state.set(key, null);
    this._deleteFile(key);
  }

  // Deviation
  async saveDeviation(runId, phaseId, deviation) {
    const key = `deviation:${runId}:${phaseId}`;
    await this.state.set(key, deviation);
    this._saveToFile(key, deviation);
  }

  async getDeviation(runId, phaseId) {
    const key = `deviation:${runId}:${phaseId}`;
    const memory = await this.state.get(key);
    if (memory !== undefined) return memory;
    return this._loadFromFile(key);
  }

  async listDeviationsByRunId(runId) {
    const keys = await this.state.keys?.() || [];
    const prefix = `deviation:${runId}:`;
    const deviationKeys = keys.filter(k => k.startsWith(prefix));
    
    // 同时从文件加载
    const filePaths = this._listFiles(prefix);
    const fileKeys = filePaths.map(p => {
      const basename = p.replace(STATE_DIR + '/', '').replace('.json', '');
      // 还原 key 格式
      return basename.replace(/_/g, ':');
    });
    
    const allKeys = [...new Set([...deviationKeys, ...fileKeys])];
    const deviations = await Promise.all(
      allKeys.map(k => this.getDeviation(
        k.split(':')[1], 
        k.split(':')[2]
      ))
    );
    return deviations.filter(Boolean);
  }

  // Attribution
  async saveAttribution(runId, deviationId, attribution) {
    const key = `attribution:${runId}:${deviationId}`;
    await this.state.set(key, attribution);
    this._saveToFile(key, attribution);
  }

  async getAttribution(runId, deviationId) {
    const key = `attribution:${runId}:${deviationId}`;
    const memory = await this.state.get(key);
    if (memory !== undefined) return memory;
    return this._loadFromFile(key);
  }

  // Event（临时存储，agent_end 时转移到 Memory）
  async saveEvent(eventId, event) {
    const key = `event:${eventId}`;
    await this.state.set(key, event);
    this._saveToFile(key, event);
  }

  async getEvent(eventId) {
    const key = `event:${eventId}`;
    const memory = await this.state.get(key);
    if (memory !== undefined) return memory;
    return this._loadFromFile(key);
  }

  async deleteEvent(eventId) {
    const key = `event:${eventId}`;
    await this.state.set(key, null);
    this._deleteFile(key);
  }

  async listEvents() {
    const keys = await this.state.keys?.() || [];
    const prefix = 'event:';
    const eventKeys = keys.filter(k => k.startsWith(prefix));
    
    // 同时从文件加载
    const filePaths = this._listFiles(prefix);
    const fileKeys = filePaths.map(p => {
      const basename = p.replace(STATE_DIR + '/', '').replace('.json', '');
      return basename.replace(/_/g, ':');
    });
    
    const allKeys = [...new Set([...eventKeys, ...fileKeys])];
    const events = await Promise.all(
      allKeys.map(k => this.getEvent(k.replace(/^event:/, '')))
    );
    return events.filter(Boolean);
  }
}
