/**
 * 插件状态管理
 *
 * OpenClaw 插件没有暴露内存/存储 API，因此插件自行在文件系统中
 * 维护状态。状态目录: <plugin-root>/state/
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export class PluginState {
  constructor(pluginId) {
    this.pluginId = pluginId;
    this.baseDir = path.join(__dirname, '..', 'state');
    this.stateFile = path.join(this.baseDir, `${pluginId}.json`);
    this.cache = null;
    this.initialized = false;
    this._initPromise = null;
    this._writeQueue = Promise.resolve();
  }

  async init() {
    if (this.initialized) return;
    if (!this._initPromise) {
      this._initPromise = (async () => {
        await fs.mkdir(this.baseDir, { recursive: true });
        try {
          const data = await fs.readFile(this.stateFile, 'utf-8');
          this.cache = JSON.parse(data);
        } catch {
          this.cache = {};
        }
        this.initialized = true;
      })();
    }
    await this._initPromise;
  }

  async get(key, defaultValue = null) {
    await this.init();
    return this.cache[key] ?? defaultValue;
  }

  async set(key, value) {
    await this.init();
    if (value === undefined) {
      delete this.cache[key];
    } else {
      this.cache[key] = value;
    }
    this._writeQueue = this._writeQueue.then(() => this._persist());
    await this._writeQueue;
  }

  async append(key, value) {
    this._writeQueue = this._writeQueue.then(async () => {
      const arr = (await this.get(key)) || [];
      arr.push(value);
      if (value === undefined) {
        delete this.cache[key];
      } else {
        this.cache[key] = arr;
      }
      return this._persist();
    });
    await this._writeQueue;
  }

  async _persist() {
    const lockFile = this.stateFile + '.lock';
    const maxRetries = 20;
    for (let i = 0; i < maxRetries; i++) {
      try {
        await fs.writeFile(lockFile, Date.now().toString(), { flag: 'wx' });
        try {
          await fs.writeFile(this.stateFile, JSON.stringify(this.cache, null, 2), 'utf-8');
        } finally {
          await fs.unlink(lockFile).catch(() => {});
        }
        return;
      } catch (err) {
        if (err.code === 'EEXIST') {
          await new Promise(r => setTimeout(r, 30 * (i + 1)));
          continue;
        }
        throw err;
      }
    }
    throw new Error('State file persist failed: unable to acquire lock');
  }
}
