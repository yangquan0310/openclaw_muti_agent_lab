/**
 * Skill 加载器
 *
 * 面向对象封装：SkillLoader 类负责管理 skill 文件的加载和缓存。
 */

import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_SKILLS_DIR = path.join(__dirname, '..');

export class SkillLoader {
  constructor(skillsDir) {
    this.skillsDir = skillsDir || DEFAULT_SKILLS_DIR;
    this.skillMap = {
      assessment: 'metacognition/assessment/SKILL.md',
      planning: 'metacognition/planning/SKILL.md',
      monitoring: 'metacognition/monitoring/SKILL.md',
      regulation: 'metacognition/regulation/SKILL.md',
      working_memory: 'working-memory/SKILL.md',
      development: 'personality/SKILL.md'
    };
    this._cache = new Map();
  }

  /**
   * 加载指定名称的 skill，返回 SKILL.md 的文本内容
   * @param {string} name - skill 名称
   * @returns {Promise<string>} skill 文本内容，失败返回空字符串
   */
  async load(name) {
    if (this._cache.has(name)) {
      return this._cache.get(name);
    }
    const content = await this._readFile(name);
    this._cache.set(name, content);
    return content;
  }

  /**
   * 从磁盘读取 skill 文件
   */
  async _readFile(name) {
    const filename = this.skillMap[name];
    if (!filename) return '';
    try {
      return await fs.readFile(path.join(this.skillsDir, filename), 'utf-8');
    } catch {
      return '';
    }
  }

  /**
   * 清除内存缓存
   */
  clearCache() {
    this._cache.clear();
  }

  /**
   * 获取所有可用的 skill 名称列表
   */
  getAvailableSkills() {
    return Object.keys(this.skillMap);
  }
}

// 向后兼容：默认实例的便捷函数
const defaultLoader = new SkillLoader();

export async function loadSkill(name) {
  return defaultLoader.load(name);
}
