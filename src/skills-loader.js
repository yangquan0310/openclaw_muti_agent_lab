/**
 * Skill 加载器
 *
 * 根据 skill 名称读取 skills/ 目录下对应的 SKILL.md
 * 插件在合适的 hook 时机将 skill 内容注入 Agent 的 system context
 */

import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SKILLS_DIR = path.join(__dirname, '../skills');

const SKILL_MAP = {
  planning: 'metacognition/planning/SKILL.md',
  monitoring: 'metacognition/monitoring/SKILL.md',
  regulation: 'metacognition/regulation/SKILL.md',
  working_memory: 'working_memory/SKILL.md',
  assimilation: 'assimilation_accommodation/SKILL.md'
};

export async function loadSkill(name) {
  const filename = SKILL_MAP[name];
  if (!filename) return '';
  try {
    return await fs.readFile(path.join(SKILLS_DIR, filename), 'utf-8');
  } catch {
    return '';
  }
}
