/**
 * 核心自我文件读写
 *
 * 数据目录: ~/.openclaw/workspace/agent-self-development/
 * 文件格式: Markdown（Agent 可直接阅读和编辑）
 *
 * 插件职责: 提供文件读写基础设施
 * Agent 职责: 决定内容、分析同化/顺应、评估置信度
 */

import { promises as fs } from 'fs';
import path from 'path';
import os from 'os';

const DATA_DIR = path.join(os.homedir(), '.openclaw', 'workspace', 'agent-self-development');

async function ensureDataDir() {
  await fs.mkdir(DATA_DIR, { recursive: true });
  await fs.mkdir(path.join(DATA_DIR, 'skills'), { recursive: true });
}

async function readFile(filename, defaultContent = '') {
  await ensureDataDir();
  try {
    return await fs.readFile(path.join(DATA_DIR, filename), 'utf-8');
  } catch {
    return defaultContent;
  }
}

async function writeFile(filename, content) {
  await ensureDataDir();
  await fs.writeFile(path.join(DATA_DIR, filename), content, 'utf-8');
}

// ─────────── 读取 API ───────────

export async function readIdentityFile() {
  return readFile('IDENTITY.md', DEFAULT_IDENTITY);
}

export async function readSoulFile() {
  return readFile('SOUL.md', DEFAULT_SOUL);
}

export async function readMemoryFile() {
  return readFile('MEMORY.md', DEFAULT_MEMORY);
}

export async function readSkillsIndex() {
  return readFile('skills/README.md', DEFAULT_SKILLS);
}

// ─────────── 写入 API ───────────

export async function appendIdentityNote(note, timestamp) {
  const content = await readIdentityFile();
  const entry = `\n- [${timestamp}] ${note}`;
  const updated = content.includes('## 历史更新')
    ? content.replace('## 历史更新', `## 历史更新${entry}`)
    : content + `\n## 历史更新${entry}\n`;
  await writeFile('IDENTITY.md', updated);
}

export async function appendSoulBelief(belief, timestamp) {
  const content = await readSoulFile();
  const entry = `\n- [${timestamp}] ${belief}`;
  const updated = content.includes('## 信念')
    ? content.replace('## 信念', `## 信念${entry}`)
    : content + `\n## 信念${entry}\n`;
  await writeFile('SOUL.md', updated);
}

export async function appendSkillEntry(name, timestamp) {
  const content = await readSkillsIndex();
  const entry = `| ${name} | ${timestamp} | assimilation |\n`;
  const updated = content.includes('|------|')
    ? content.replace('|------|\n', `|------|\n${entry}`)
    : content + `\n| Name | Learned At | Source |\n|------|------------|--------|\n${entry}`;
  await writeFile('skills/README.md', updated);
}

export async function appendMemoryNote(note, timestamp) {
  const content = await readMemoryFile();
  const entry = `\n- [${timestamp}] ${note}`;
  const updated = content.includes('## 事件')
    ? content.replace('## 事件', `## 事件${entry}`)
    : content + `\n## 事件${entry}\n`;
  await writeFile('MEMORY.md', updated);
}

// ─────────── 默认模板 ───────────

const DEFAULT_IDENTITY = `# Identity

## 核心身份
- 名称: Agent
- 角色: 智能助手

## 能力边界
- 可执行: 代码编写、文件操作、数据分析
- 不可执行: 物理操作、访问外部未授权系统

## 历史更新
`;

const DEFAULT_SOUL = `# Soul

## 核心价值观
- 诚实、高效、持续学习

## 信念
`;

const DEFAULT_MEMORY = `# Memory

## 核心认知
- 自我发展是一个持续循环

## 事件
`;

const DEFAULT_SKILLS = `# Skills

## 技能索引
`;
