/**
 * LogAdapter — 日志适配器（按代理分文件版）
 * 基于文本文件持久化，每个代理独立文件 ~/.openclaw/logs/{agentId}.log
 */

import { writeFileSync, readFileSync, existsSync, mkdirSync, appendFileSync } from 'fs';
import { join } from 'path';

const DEFAULT_LOGS_DIR = '/root/.openclaw/logs';

function ensureDir(dir) {
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
}

export class LogAdapter {
  constructor(api, options = {}) {
    this.api = api; // 可为 null
    this.dir = options.dir || DEFAULT_LOGS_DIR;
    this.agentId = options.agentId || 'agent-self-development';
    this.logFile = join(this.dir, `${this.agentId}.log`);
    this.jsonlFile = join(this.dir, `${this.agentId}.jsonl`);
    this._ensureFiles();
  }

  _ensureFiles() {
    ensureDir(this.dir);
    if (!existsSync(this.logFile)) writeFileSync(this.logFile, '', 'utf8');
    if (!existsSync(this.jsonlFile)) writeFileSync(this.jsonlFile, '', 'utf8');
  }

  _formatText(entry) {
    const ts = entry.timestamp || new Date().toISOString();
    const level = entry.level?.toUpperCase() || 'INFO';
    return `[${ts}] [${level}] ${entry.message || ''}`;
  }

  async write(entry) {
    if (this.api?.write) await this.api.write(entry);
    const line = this._formatText(entry) + '\n';
    appendFileSync(this.logFile, line, 'utf8');
  }

  async read(options = {}) {
    if (this.api?.read) {
      const apiResult = await this.api.read(options);
      if (apiResult) return apiResult;
    }
    try {
      const content = readFileSync(this.logFile, 'utf8');
      const lines = content.split('\n').filter(Boolean);
      if (options.limit) return lines.slice(-options.limit);
      return lines;
    } catch (error) {
      console.error('[LogAdapter] 读取失败', error.message);
      return [];
    }
  }

  async query(options = {}) {
    const lines = await this.read(options);
    return lines.filter(line => {
      if (options.level && !line.includes(`[${options.level.toUpperCase()}]`)) return false;
      if (options.search && !line.includes(options.search)) return false;
      if (options.since) {
        const tsMatch = line.match(/^\[(.*?)\]/);
        if (tsMatch && new Date(tsMatch[1]) < new Date(options.since)) return false;
      }
      return true;
    });
  }

  // JSONL 结构化日志
  async writeJsonl(record) {
    const line = JSON.stringify({ ...record, _ts: new Date().toISOString() }) + '\n';
    appendFileSync(this.jsonlFile, line, 'utf8');
  }

  async readJsonl(options = {}) {
    try {
      const content = readFileSync(this.jsonlFile, 'utf8');
      const lines = content.split('\n').filter(Boolean);
      const records = lines.map(l => JSON.parse(l));
      if (options.type) return records.filter(r => r.type === options.type);
      if (options.limit) return records.slice(-options.limit);
      return records;
    } catch {
      return [];
    }
  }
}
