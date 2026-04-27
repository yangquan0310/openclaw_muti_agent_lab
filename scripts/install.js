#!/usr/bin/env node
/**
 * OpenClaw Agent Self-Development Plugin 安装脚本
 * 
 * 自动将插件注册到 openclaw.json，支持安装/卸载/预览。
 * 
 * 关键：本插件使用了 llm_output / before_agent_finalize / agent_end 等
 * Conversation Hook，必须在配置中设置 allowConversationAccess: true。
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const PLUGIN_NAME = 'agent-self-development';

const DEFAULT_PLUGIN_CONFIG = {
  enabled: true,
  hooks: {
    allowConversationAccess: true
  },
  config: {
    metacognition: {
      enabled: true,
      planning: true,
      monitoring: true,
      regulation: true
    },
    workingMemory: {
      enabled: true,
      trackSubagents: true,
      autoArchive: true
    },
    assimilation: {
      enabled: true,
      dailyCron: "0 0 * * *",
      autoUpdate: false,
      updateThreshold: 0.8
    },
    llm: {
      model: "kimi-for-coding",
      provider: "kimicode"
    }
  }
};

/* ─────────── 主流程 ─────────── */

function main() {
  const args = parseArgs();

  if (args.help) {
    showHelp();
    process.exit(0);
  }

  const configPath = resolveConfigPath(args.config);

  if (!fs.existsSync(configPath)) {
    console.error(`❌ 找不到 openclaw.json: ${configPath}`);
    console.error(`   请用 --config 指定路径，或设置 OPENCLAW_CONFIG 环境变量`);
    process.exit(1);
  }

  console.log(`📂 目标配置: ${configPath}`);

  const raw = fs.readFileSync(configPath, 'utf-8');
  let config;
  try {
    config = JSON.parse(raw);
  } catch (err) {
    console.error(`❌ JSON 解析失败: ${err.message}`);
    process.exit(1);
  }

  if (args.uninstall) {
    uninstall(config, args);
  } else {
    install(config, args);
  }

  const output = JSON.stringify(config, null, 2) + '\n';

  if (args.dryRun) {
    console.log('\n📋 [Dry Run] 变更预览（不会写入文件）：\n');
    console.log(output);
    return;
  }

  const backupPath = `${configPath}.bak.${Date.now()}`;
  fs.copyFileSync(configPath, backupPath);
  console.log(`💾 配置已备份: ${backupPath}`);

  fs.writeFileSync(configPath, output, 'utf-8');
  console.log(`✅ 配置已更新: ${configPath}`);

  if (!args.uninstall) {
    console.log(`\n⚠️  重要提醒`);
    console.log(`   本插件使用了 llm_output / before_agent_finalize / agent_end 等 Conversation Hook，`);
    console.log(`   已自动在配置中设置 hooks.allowConversationAccess = true。`);
    console.log(`\n🚀 下一步: 重启 OpenClaw Gateway`);
    console.log(`   openclaw gateway restart`);
    console.log(`   然后验证: openclaw hooks list`);
  }
}

/* ─────────── 安装逻辑 ─────────── */

function install(config, args) {
  config.plugins = config.plugins || {};
  config.plugins.entries = config.plugins.entries || {};
  config.plugins.load = config.plugins.load || {};
  config.plugins.load.paths = config.plugins.load.paths || [];
  config.plugins.allow = config.plugins.allow || [];

  // 1. 添加/更新 entries
  const existing = config.plugins.entries[PLUGIN_NAME];
  if (existing) {
    config.plugins.entries[PLUGIN_NAME] = deepMerge(DEFAULT_PLUGIN_CONFIG, existing);
    console.log(`🔄 更新 plugins.entries.${PLUGIN_NAME}（保留用户自定义）`);
  } else {
    config.plugins.entries[PLUGIN_NAME] = JSON.parse(JSON.stringify(DEFAULT_PLUGIN_CONFIG));
    console.log(`➕ 添加 plugins.entries.${PLUGIN_NAME}`);
  }

  // 2. 添加 load path
  const pluginPath = resolvePluginPath(args.path);
  const paths = config.plugins.load.paths;
  const normalizedPaths = paths.map(p => path.normalize(p));
  const normalizedNew = path.normalize(pluginPath);

  if (!normalizedPaths.includes(normalizedNew)) {
    paths.push(pluginPath);
    console.log(`➕ 添加 plugins.load.paths: ${pluginPath}`);
  } else {
    console.log(`ℹ️ 加载路径已存在: ${pluginPath}`);
  }

  // 3. 添加到 allow 白名单
  const allowList = config.plugins.allow;
  if (!allowList.includes(PLUGIN_NAME)) {
    allowList.push(PLUGIN_NAME);
    console.log(`➕ 添加 plugins.allow: ${PLUGIN_NAME}`);
  } else {
    console.log(`ℹ️ 白名单已存在: ${PLUGIN_NAME}`);
  }
}

/* ─────────── 卸载逻辑 ─────────── */

function uninstall(config, args) {
  if (config.plugins?.entries?.[PLUGIN_NAME]) {
    delete config.plugins.entries[PLUGIN_NAME];
    console.log(`🗑️ 移除 plugins.entries.${PLUGIN_NAME}`);
  } else {
    console.log(`ℹ️ plugins.entries.${PLUGIN_NAME} 不存在`);
  }

  const pluginPath = resolvePluginPath(args.path);
  if (config.plugins?.load?.paths) {
    const paths = config.plugins.load.paths;
    const normalizedPaths = paths.map(p => path.normalize(p));
    const normalizedTarget = path.normalize(pluginPath);
    const idx = normalizedPaths.indexOf(normalizedTarget);

    if (idx !== -1) {
      paths.splice(idx, 1);
      console.log(`🗑️ 移除 plugins.load.paths: ${pluginPath}`);
    } else {
      console.log(`ℹ️ 加载路径未找到: ${pluginPath}`);
    }
  }

  if (config.plugins?.allow) {
    const idx = config.plugins.allow.indexOf(PLUGIN_NAME);
    if (idx !== -1) {
      config.plugins.allow.splice(idx, 1);
      console.log(`🗑️ 移除 plugins.allow: ${PLUGIN_NAME}`);
    }
  }

  if (config.plugins?.load?.paths?.length === 0) {
    delete config.plugins.load.paths;
  }
  if (config.plugins?.load && Object.keys(config.plugins.load).length === 0) {
    delete config.plugins.load;
  }
  if (config.plugins?.entries && Object.keys(config.plugins.entries).length === 0) {
    delete config.plugins.entries;
  }
}

/* ─────────── 路径解析 ─────────── */

function resolvePluginPath(customPath) {
  if (customPath) return path.resolve(customPath);
  return path.resolve(__dirname, '..');
}

function resolveConfigPath(customPath) {
  if (customPath) return path.resolve(customPath);
  if (process.env.OPENCLAW_CONFIG) return path.resolve(process.env.OPENCLAW_CONFIG);

  const candidates = [
    path.join(os.homedir(), '.openclaw', 'openclaw.json'),
    path.resolve('openclaw.json'),
    path.resolve(__dirname, '..', '..', 'openclaw.json'),
    path.resolve(__dirname, '..', '..', '.openclaw', 'openclaw.json'),
  ];

  for (const p of candidates) {
    if (fs.existsSync(p)) return p;
  }
  return candidates[0];
}

/* ─────────── 工具函数 ─────────── */

function deepMerge(base, override) {
  const result = JSON.parse(JSON.stringify(base));
  for (const key of Object.keys(override)) {
    if (
      override[key] &&
      typeof override[key] === 'object' &&
      !Array.isArray(override[key])
    ) {
      result[key] = deepMerge(result[key] || {}, override[key]);
    } else {
      result[key] = override[key];
    }
  }
  return result;
}

function parseArgs() {
  const args = { dryRun: false, uninstall: false, help: false };
  const argv = process.argv.slice(2);

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    switch (arg) {
      case '--config':
      case '-c':
        args.config = argv[++i];
        break;
      case '--path':
      case '-p':
        args.path = argv[++i];
        break;
      case '--dry-run':
      case '-d':
        args.dryRun = true;
        break;
      case '--uninstall':
      case '-u':
        args.uninstall = true;
        break;
      case '--help':
      case '-h':
        args.help = true;
        break;
    }
  }
  return args;
}

function showHelp() {
  console.log(`
用法: node scripts/install.js [选项]

选项:
  -c, --config <路径>   指定 openclaw.json 路径
                        (默认自动搜索: ~/.openclaw/openclaw.json, ./openclaw.json)
  -p, --path <路径>     指定插件加载路径
                        (默认: 当前插件目录)
  -d, --dry-run         预览变更，不写入文件
  -u, --uninstall       从 openclaw.json 中移除插件配置
  -h, --help            显示此帮助

示例:
  # 安装（自动检测 openclaw.json）
  node scripts/install.js

  # 安装到指定配置
  node scripts/install.js --config /root/.openclaw/openclaw.json

  # 指定云端路径
  node scripts/install.js --path /root/projects/openclaw-agent-self-development

  # 预览变更
  node scripts/install.js --dry-run

  # 卸载
  node scripts/install.js --uninstall

环境变量:
  OPENCLAW_CONFIG       设置默认配置文件路径
`);
}

main();
