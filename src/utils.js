/**
 * 工具函数
 */

export function getToday(timezone = 'Asia/Shanghai') {
  const formatter = new Intl.DateTimeFormat('en-CA', {
    timeZone: timezone,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });
  return formatter.format(new Date());
}

export function getYesterday(timezone = 'Asia/Shanghai') {
  const today = getToday(timezone);
  const [year, month, day] = today.split('-').map(Number);
  const date = new Date(year, month - 1, day);
  date.setDate(date.getDate() - 1);
  return date.toISOString().split('T')[0];
}

export function getNow() {
  return new Date().toISOString();
}

/**
 * 根据任务内容推断会话类型
 */
export function inferSessionType(prompt) {
  const p = (prompt || '').toLowerCase();
  if (p.includes('项目') || p.includes('project') || p.includes('开发') || p.includes('代码')) return 'PROJECT';
  if (p.includes('研究') || p.includes('调研') || p.includes('文献') || p.includes('research')) return 'RESEARCH';
  if (p.includes('定时') || p.includes('cron') || p.includes('schedule')) return 'CORN';
  if (p.includes('写作') || p.includes('撰写') || p.includes('报告') || p.includes('论文')) return 'WRITING';
  return 'TASK';
}

/**
 * 为计划步骤分配建议的会话标识
 * 格式: session:{TYPE}:{任务标识}
 * 例: session:PROJECT:博士论文、session:TASK:文献检索
 * 注: 此标识用于指导 Agent 创建会话时的命名/ID选择，OpenClaw 中通过 agent/subagent 工具创建会话后直接以该 ID 通信
 */
export function assignSessions(planItems, prompt) {
  const sessionType = inferSessionType(prompt);
  const assignments = [];

  // 通常第一个步骤由主代理直接执行，后续需要独立上下文的步骤分配会话
  const needsSessionKeywords = ['检索', '搜索', '调研', '分析', '编写', '开发', '实现', '测试', '验证', '撰写', '设计'];

  planItems.forEach((item, index) => {
    const itemLower = item.toLowerCase();
    // 判断该步骤是否需要独立会话（含特定关键词且非第一步）
    const needsSession = index > 0 && needsSessionKeywords.some(k => itemLower.includes(k));

    if (needsSession) {
      // 生成会话标识：取步骤前10个字符 + 随机后缀，避免冲突
      const taskSlug = item.slice(0, 10).trim().replace(/\s+/g, '_').replace(/[^\w\u4e00-\u9fa5]/g, '');
      const randomSuffix = Math.random().toString(36).slice(2, 6);
      assignments.push({
        step: index + 1,
        sessionId: `session:${sessionType}:${taskSlug}_${randomSuffix}`,
        purpose: item
      });
    }
  });

  return assignments;
}

export function generatePlanItems(prompt) {
  const p = (prompt || '').toLowerCase();
  if (p.includes('代码') || p.includes('开发') || p.includes('实现')) {
    return [
      '分析需求，明确接口和依赖',
      '设计数据结构和算法',
      '编写核心逻辑代码',
      '添加错误处理和边界情况',
      '编写测试用例并验证',
      '代码审查和重构'
    ];
  }
  if (p.includes('写作') || p.includes('撰写') || p.includes('报告')) {
    return [
      '收集素材和背景信息',
      '确定文章结构和核心论点',
      '撰写大纲和关键段落',
      '补充细节和数据支撑',
      '审校语言、逻辑和格式',
      '输出终稿'
    ];
  }
  if (p.includes('分析') || p.includes('研究') || p.includes('调查')) {
    return [
      '明确分析目标和范围',
      '收集相关数据和信息',
      '建立分析框架',
      '执行分析并记录发现',
      '验证结论的可靠性',
      '形成分析报告'
    ];
  }
  return [
    '理解任务目标和约束条件',
    '分解任务为可执行的子步骤',
    '按优先级执行各子步骤',
    '检查中间结果质量',
    '整合输出并验证完整性',
    '归档任务记录'
  ];
}
