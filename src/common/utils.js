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
  const formatter = new Intl.DateTimeFormat('en-CA', {
    timeZone: timezone,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });
  const now = new Date();
  now.setDate(now.getDate() - 1);
  return formatter.format(now);
}

export function getNow() {
  return new Date().toISOString();
}

/**
 * 根据任务内容推断会话类型（高维度分类）
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
 * 从阶段目标推断任务族（用于任务空间复用）
 */
export function inferTaskFamily(purpose) {
  const p = (purpose || '').toLowerCase();
  if (p.includes('代码') || p.includes('开发') || p.includes('实现') || p.includes('编程') || p.includes('重构')) return 'CODE';
  if (p.includes('检索') || p.includes('搜索') || p.includes('调研') || p.includes('文献') || p.includes('收集')) return 'RESEARCH';
  if (p.includes('分析') || p.includes('统计') || p.includes('数据') || p.includes('建模')) return 'ANALYSIS';
  if (p.includes('写作') || p.includes('撰写') || p.includes('报告') || p.includes('文档') || p.includes('大纲')) return 'WRITING';
  if (p.includes('测试') || p.includes('验证') || p.includes('调试') || p.includes('审查')) return 'TEST';
  if (p.includes('设计') || p.includes('架构') || p.includes('规划') || p.includes('方案')) return 'DESIGN';
  return 'TASK';
}

/**
 * 生成完整的 Plan 上下文对象
 *
 * Plan 不是步骤列表，而是一套完整的上下文语境，包括：
 * - context: 任务目标、约束、验收标准
 * - workspace: 任务空间、工具、文档
 * - execution: 阶段化执行计划
 */
export function generatePlan(prompt) {
  const sessionType = inferSessionType(prompt);
  const p = (prompt || '').toLowerCase();

  if (p.includes('代码') || p.includes('开发') || p.includes('实现')) {
    return {
      status: 'draft',
      context: {
        goal: '实现一个可运行的软件功能',
        constraints: ['遵循项目代码规范', '包含错误处理', '包含测试用例'],
        successCriteria: ['代码可编译/运行', '测试通过', '核心逻辑文档化']
      },
      workspace: {
        sessions: [],
        artifacts: [],
        tools: ['editor', 'git', 'test_framework', 'debugger']
      },
      execution: {
        phases: [
          { id: 'p1', name: '需求分析', goal: '明确接口和依赖', sessionId: null, outputs: ['需求说明'], status: 'pending' },
          { id: 'p2', name: '架构设计', goal: '设计数据结构和算法', sessionId: `session:${sessionType}:DESIGN`, outputs: ['设计文档'], status: 'pending' },
          { id: 'p3', name: '核心编码', goal: '编写核心逻辑代码', sessionId: `session:${sessionType}:CODE`, outputs: ['源码文件'], status: 'pending' },
          { id: 'p4', name: '错误处理', goal: '添加错误处理和边界情况', sessionId: `session:${sessionType}:CODE`, outputs: ['鲁棒性增强'], status: 'pending' },
          { id: 'p5', name: '测试验证', goal: '编写测试用例并验证', sessionId: `session:${sessionType}:TEST`, outputs: ['测试报告'], status: 'pending' },
          { id: 'p6', name: '审查重构', goal: '代码审查和重构', sessionId: null, outputs: ['审查记录'], status: 'pending' }
        ],
        currentPhase: 0
      }
    };
  }

  if (p.includes('写作') || p.includes('撰写') || p.includes('报告')) {
    return {
      status: 'draft',
      context: {
        goal: '产出结构清晰、论证充分的文档',
        constraints: ['符合格式规范', '引用来源可靠', '语言准确'],
        successCriteria: ['大纲完整', '论点有据', '语言通顺', '格式正确']
      },
      workspace: {
        sessions: [],
        artifacts: [],
        tools: ['editor', 'research_tools', 'citation_manager']
      },
      execution: {
        phases: [
          { id: 'p1', name: '素材收集', goal: '收集素材和背景信息', sessionId: `session:${sessionType}:RESEARCH`, outputs: ['素材库'], status: 'pending' },
          { id: 'p2', name: '结构确定', goal: '确定文章结构和核心论点', sessionId: null, outputs: ['大纲'], status: 'pending' },
          { id: 'p3', name: '正文撰写', goal: '撰写大纲和关键段落', sessionId: `session:${sessionType}:WRITING`, outputs: ['初稿'], status: 'pending' },
          { id: 'p4', name: '细节补充', goal: '补充细节和数据支撑', sessionId: `session:${sessionType}:WRITING`, outputs: ['充实稿'], status: 'pending' },
          { id: 'p5', name: '审校润色', goal: '审校语言、逻辑和格式', sessionId: null, outputs: ['审校记录'], status: 'pending' },
          { id: 'p6', name: '输出终稿', goal: '输出终稿', sessionId: null, outputs: ['终稿'], status: 'pending' }
        ],
        currentPhase: 0
      }
    };
  }

  if (p.includes('分析') || p.includes('研究') || p.includes('调查')) {
    return {
      status: 'draft',
      context: {
        goal: '通过系统分析得出可靠结论',
        constraints: ['数据来源可靠', '方法可复现', '结论有依据'],
        successCriteria: ['分析框架清晰', '数据完整', '结论可靠', '报告规范']
      },
      workspace: {
        sessions: [],
        artifacts: [],
        tools: ['data_tools', 'visualization', 'research_tools']
      },
      execution: {
        phases: [
          { id: 'p1', name: '目标界定', goal: '明确分析目标和范围', sessionId: null, outputs: ['分析目标'], status: 'pending' },
          { id: 'p2', name: '数据收集', goal: '收集相关数据和信息', sessionId: `session:${sessionType}:RESEARCH`, outputs: ['数据集'], status: 'pending' },
          { id: 'p3', name: '框架建立', goal: '建立分析框架', sessionId: `session:${sessionType}:ANALYSIS`, outputs: ['分析模型'], status: 'pending' },
          { id: 'p4', name: '分析执行', goal: '执行分析并记录发现', sessionId: `session:${sessionType}:ANALYSIS`, outputs: ['分析结果'], status: 'pending' },
          { id: 'p5', name: '结论验证', goal: '验证结论的可靠性', sessionId: null, outputs: ['验证报告'], status: 'pending' },
          { id: 'p6', name: '报告形成', goal: '形成分析报告', sessionId: `session:${sessionType}:WRITING`, outputs: ['分析报告'], status: 'pending' }
        ],
        currentPhase: 0
      }
    };
  }

  // 通用任务
  return {
    status: 'draft',
    context: {
      goal: '按质量要求完成指定任务',
      constraints: ['按时完成', '符合基本要求'],
      successCriteria: ['任务完成', '结果可验收']
    },
    workspace: {
      sessions: [],
      artifacts: [],
      tools: []
    },
    execution: {
      phases: [
        { id: 'p1', name: '目标理解', goal: '理解任务目标和约束条件', sessionId: null, outputs: ['目标确认'], status: 'pending' },
        { id: 'p2', name: '任务分解', goal: '分解任务为可执行的子步骤', sessionId: null, outputs: ['任务清单'], status: 'pending' },
        { id: 'p3', name: '分步执行', goal: '按优先级执行各子步骤', sessionId: null, outputs: ['中间成果'], status: 'pending' },
        { id: 'p4', name: '质量检查', goal: '检查中间结果质量', sessionId: null, outputs: ['检查记录'], status: 'pending' },
        { id: 'p5', name: '成果整合', goal: '整合输出并验证完整性', sessionId: null, outputs: ['最终成果'], status: 'pending' },
        { id: 'p6', name: '任务归档', goal: '归档任务记录', sessionId: null, outputs: ['归档记录'], status: 'pending' }
      ],
      currentPhase: 0
    }
  };
}

/**
 * 将任务空间分配给各阶段
 * 同一任务族的阶段复用同一任务空间
 */
export function assignSessionsToPhases(phases, prompt) {
  const sessionType = inferSessionType(prompt);
  const assignedPhases = phases.map((phase, index) => {
    // 第一阶段通常由主代理直接执行，不分配任务空间
    if (index === 0) return phase;

    const taskFamily = inferTaskFamily(phase.goal);
    const needsSession = ['CODE', 'RESEARCH', 'ANALYSIS', 'WRITING', 'TEST', 'DESIGN'].includes(taskFamily);

    if (needsSession) {
      return {
        ...phase,
        sessionId: `session:${sessionType}:${taskFamily}`,
        taskFamily
      };
    }
    return phase;
  });

  return assignedPhases;
}
