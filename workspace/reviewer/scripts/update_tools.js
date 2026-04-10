/**
 * 自动更新TOOLS.md脚本
 * 功能：
 * 1. 添加最新项目到项目列表
 * 2. 移除不存在的项目
 * 3. 添加程序性记忆中的脚本索引
 * 4. 删除不存在的脚本索引
 */

const fs = require('fs');
const path = require('path');

// 配置路径
const WORKSPACE = '/root/.openclaw/workspace/reviewer';
const TOOLS_PATH = path.join(WORKSPACE, 'TOOLS.md');
const MEMORY_PATH = path.join(WORKSPACE, 'MEMORY.md');
const PROJECTS_ROOT = '/root/实验室仓库/项目文件/';
const LOG_ROOT = '/root/实验室仓库/日志文件/';

/**
 * 读取文件内容
 */
function readFile(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf8');
  } catch (error) {
    console.error(`读取文件失败: ${filePath}`, error);
    return null;
  }
}

/**
 * 写入文件内容
 */
function writeFile(filePath, content) {
  try {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`文件已更新: ${filePath}`);
    return true;
  } catch (error) {
    console.error(`写入文件失败: ${filePath}`, error);
    return false;
  }
}

/**
 * 获取实际存在的项目列表
 */
function getActualProjects() {
  try {
    const dirs = fs.readdirSync(PROJECTS_ROOT, { withFileTypes: true })
      .filter(dirent => dirent.isDirectory())
      .map(dirent => {
        const name = dirent.name;
        const projectPath = path.join(PROJECTS_ROOT, name);
        const readmePath = path.join(projectPath, 'README.md');
        let description = '';
        
        // 尝试读取README获取项目描述
        if (fs.existsSync(readmePath)) {
          const readmeContent = fs.readFileSync(readmePath, 'utf8');
          const descMatch = readmeContent.match(/^#.*\n\n(.+?)(\n|$)/s);
          if (descMatch) {
            description = descMatch[1].trim();
          }
        }
        
        return {
          name: name,
          path: `~/实验室仓库/项目文件/${name}/`,
          description: description
        };
      });
    
    // 按名称排序
    return dirs.sort((a, b) => a.name.localeCompare(b.name));
  } catch (error) {
    console.error('获取项目列表失败:', error);
    return [];
  }
}

/**
 * 从MEMORY.md中提取脚本索引
 * 根据当前MEMORY.md结构，脚本定义在程序性记忆部分
 */
function extractScriptsFromMemory(memoryContent) {
  const scripts = [];
  
  // 审稿助手特有的三个脚本（固定定义）
  scripts.push({
    id: 'S1',
    name: '质量审查脚本',
    trigger: '收到论文评审请求，需要评估论文质量',
    description: '对论文进行多维度质量审查，生成结构化评审报告和修改建议'
  });
  
  scripts.push({
    id: 'S2',
    name: '格式规范脚本',
    trigger: '需要检查论文格式规范',
    description: '对照学术标准检查文档格式，提供详细的格式修正建议'
  });
  
  scripts.push({
    id: 'S3',
    name: '审稿意见记录脚本',
    trigger: '完成论文评审，需要系统性记录审稿意见',
    description: '结构化记录评审意见，建立问题追踪系统，支持版本控制'
  });
  
  // 检查实际存在的脚本文件
  const scriptsDir = path.join(WORKSPACE, 'scripts');
  if (fs.existsSync(scriptsDir)) {
    const scriptFiles = fs.readdirSync(scriptsDir, { withFileTypes: true })
      .filter(dirent => dirent.isFile() && !dirent.name.startsWith('.'))
      .map(dirent => dirent.name);
    
    // 添加其他脚本文件（如果不在固定列表中）
    scriptFiles.forEach(filename => {
      const existingScript = scripts.find(s => s.name === filename.replace(/\.(js|sh)$/, ''));
      if (!existingScript && filename !== 'update_tools.js' && filename !== 'update_tools.sh') {
        scripts.push({
          id: '-',
          name: filename,
          trigger: filename.includes('维护') ? '工作记忆维护' : '系统维护',
          description: `脚本文件: ${filename}`
        });
      }
    });
  }
  
  return scripts;
}

/**
 * 生成项目列表Markdown
 */
function generateProjectsMarkdown(projects) {
  let markdown = '### 项目\n\n> 各个代理独立维护\n### 项目结构\n```\n项目文件/\n└── YYYY-MM-DD_项目名/\n    ├── 文档/                  # 用户上传的文档\n    ├── 草稿/                   # 论文草稿\n    ├── 终稿/                   # 最终版本\n    ├── 知识库/                 # 项目专属知识库\n    │   └── 索引.json          # 文献索引\n    ├── 元数据.json             # 项目元数据\n    └── README.md               # 项目说明\n```\n\n### 项目库\n> 大管家维护格式\n> 内容由各代理独立维护\n| 项目名 | 存储位置 | 描述 |\n|--------|----------|------|\n';
  
  projects.forEach(project => {
    markdown += `| ${project.name} | ${project.path} | ${project.description} |\n`;
  });
  
  return markdown + '\n';
}

/**
 * 生成脚本索引Markdown
 */
function generateScriptsMarkdown(scripts) {
  let markdown = '### 脚本索引\n> 各个代理独立维护，这里显示审稿助手特有脚本\n\n| 触发条件 | 脚本编号 | 脚本名称 | 功能描述 |\n|----------|----------|----------|----------|\n';
  
  scripts.forEach(script => {
    markdown += `| ${script.trigger} | ${script.id} | ${script.name} | ${script.description} |\n`;
  });
  
  return markdown + '\n';
}

/**
 * 创建工作日志
 */
function createWorkLog(success, projectsCount, scriptsCount) {
  const now = new Date();
  const dateStr = now.toISOString().split('T')[0];
  const timeStr = now.toTimeString().split(' ')[0].replace(/:/g, '-');
  const logDir = path.join(LOG_ROOT, dateStr);
  const logPath = path.join(logDir, `${timeStr}-reviewer-TOOLS更新.md`);
  
  // 创建日志目录
  if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true });
  }
  
  const status = success ? '成功' : '失败';
  const timestamp = now.toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
  const logContent = `${timestamp}
任务名称：TOOLS.md自动更新
任务类型：系统维护
执行状态：${status}
涉及项目：无

执行详情：
- 扫描到项目数量：${projectsCount} 个
- 扫描到脚本数量：${scriptsCount} 个
- 执行状态：${success ? 'TOOLS.md已成功更新' : 'TOOLS.md更新失败'}

存储路径：
- 脚本位置：~/.openclaw/workspace/reviewer/scripts/
- 日志位置：${logPath.replace('/root/', '~/')}

参与Agent：
- 审稿助手(reviewer)
`;
  
  try {
    fs.writeFileSync(logPath, logContent, 'utf8');
    console.log(`工作日志已创建: ${logPath}`);
    return true;
  } catch (error) {
    console.error('创建工作日志失败:', error);
    return false;
  }
}

/**
 * 主函数
 */
function main() {
  console.log('开始更新TOOLS.md...');
  
  // 读取现有文件
  const toolsContent = readFile(TOOLS_PATH);
  const memoryContent = readFile(MEMORY_PATH);
  
  if (!toolsContent || !memoryContent) {
    console.error('必要文件读取失败，退出');
    createWorkLog(false, 0, 0);
    process.exit(1);
  }
  
  // 获取实际项目和脚本
  const actualProjects = getActualProjects();
  const actualScripts = extractScriptsFromMemory(memoryContent);
  
  console.log(`找到 ${actualProjects.length} 个项目，${actualScripts.length} 个脚本`);
  
  // 替换项目部分
  let newContent = toolsContent.replace(
    /### 项目\n\n> 各个代理独立维护\n### 项目结构\n```[\s\S]+?```\n\n### 项目库\n> 大管家维护格式\n> 内容由各代理独立维护\n\| 项目名 \| 存储位置 \| 描述 \|\n\|[-| ]+\|[-| ]+\|[-| ]+\|\n([\s\S]+?)\n### /,
    (match, projectsTable) => {
      return generateProjectsMarkdown(actualProjects) + '### ';
    }
  );
  
  // 替换脚本索引部分
  newContent = newContent.replace(
    /### 脚本索引\n> 各个代理独立维护，这里显示审稿助手特有脚本\n\n\| 触发条件 \| 脚本编号 \| 脚本名称 \| 功能描述 \|\n\|[-| ]+\|[-| ]+\|[-| ]+\|[-| ]+\|\n([\s\S]+?)(\n---|\n\*|$)/,
    (match, scriptsTable, suffix) => {
      return generateScriptsMarkdown(actualScripts) + suffix;
    }
  );
  
  // 写入更新后的内容
  const success = writeFile(TOOLS_PATH, newContent);
  
  // 创建工作日志
  createWorkLog(success, actualProjects.length, actualScripts.length);
  
  if (success) {
    console.log('TOOLS.md 更新成功');
    process.exit(0);
  } else {
    console.error('TOOLS.md 更新失败');
    process.exit(1);
  }
}

main();
