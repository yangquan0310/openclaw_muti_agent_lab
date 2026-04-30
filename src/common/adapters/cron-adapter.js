/**
 * CronAdapter — 定时任务适配器
 * 读写 ~/.openclaw/cron/jobs.json
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';

const DEFAULT_JOBS_PATH = '/root/.openclaw/cron/jobs.json';

function ensureDir(path) {
  try { mkdirSync(dirname(path), { recursive: true }); } catch {}
}

function loadJobs(path) {
  if (!existsSync(path)) return { version: 1, jobs: [] };
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return { version: 1, jobs: [] };
  }
}

function saveJobs(path, data) {
  ensureDir(path);
  writeFileSync(path, JSON.stringify(data, null, 2), 'utf8');
}

export class CronAdapter {
  constructor(options = {}) {
    this.path = options.path || DEFAULT_JOBS_PATH;
  }

  /**
   * 注册定时任务
   * @param {Object} job - { name, schedule, payload, enabled }
   */
  async register(job) {
    const data = loadJobs(this.path);
    const existing = data.jobs.findIndex(j => j.name === job.name);
    if (existing >= 0) {
      data.jobs[existing] = { ...data.jobs[existing], ...job, updatedAt: new Date().toISOString() };
    } else {
      data.jobs.push({ ...job, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() });
    }
    saveJobs(this.path, data);
    return job;
  }

  /**
   * 注销定时任务
   */
  async unregister(name) {
    const data = loadJobs(this.path);
    data.jobs = data.jobs.filter(j => j.name !== name);
    saveJobs(this.path, data);
  }

  /**
   * 查询任务列表
   */
  async list() {
    return loadJobs(this.path).jobs;
  }

  /**
   * 获取单个任务
   */
  async get(name) {
    const data = loadJobs(this.path);
    return data.jobs.find(j => j.name === name);
  }
}
