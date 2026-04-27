/**
 * 插件状态管理
 *
 * OpenClaw 插件没有暴露内存/存储 API，因此插件自行在文件系统中
 * 维护状态。状态目录: ~/.openclaw/plugin-state/
 */

import fs from 'fs/promises';
import path from 'path';
import os from 'os';

export class PluginState {
  constructor(pluginId) {
    this.pluginId = pluginId;
    this.baseDir = path.join(os.homedir(), '.openclaw', 'plugin-state');
    this.stateFile = path.join(this.baseDir, `${pluginId}.json`);
    this.cache = null;
    this.initialized = false;
  }

  async init() {
    if (this.initialized) return;
    await fs.mkdir(this.baseDir, { recursive: true });
    try {
      const data = await fs.readFile(this.stateFile, 'utf-8');
      this.cache = JSON.parse(data);
    } catch {
      this.cache = {};
    }
    this.initialized = true;
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
    await this._persist();
  }

  async append(key, value) {
    const arr = (await this.get(key)) || [];
    arr.push(value);
    await this.set(key, arr);
  }

  async _persist() {
    const lockFile = this.stateFile + '.lock';
    const maxRetries = 5;
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
          await new Promise(r => setTimeout(r, 50 * (i + 1)));
          continue;
        }
        throw err;
      }
    }
    throw new Error('State file persist failed: unable to acquire lock');
  }
}
