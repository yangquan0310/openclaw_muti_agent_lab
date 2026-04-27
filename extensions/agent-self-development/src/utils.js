/**
 * 工具函数
 */

function getToday() {
  return new Date().toISOString().split('T')[0];
}

function getNow() {
  return new Date().toISOString();
}

/**
 * 调用外部 LLM（插件未暴露 LLM API，需自行 HTTP 调用）
 */
async function callLLM(prompt, config = {}) {
  const provider = config.provider || 'kimicode';
  const model = config.model || 'kimi-for-coding';

  if (provider === 'kimicode') {
    const apiKey = process.env.KIMICODE_API_KEY;
    const baseUrl = config.baseUrl || 'https://api.kimi.com/coding/v1';

    if (!apiKey) {
      throw new Error('环境变量 KIMICODE_API_KEY 未设置');
    }

    const response = await fetch(`${baseUrl}/messages`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model,
        messages: [
          { role: 'system', content: '你是 Agent 自我发展系统的分析引擎。' },
          { role: 'user', content: prompt }
        ],
        max_tokens: 2048,
        temperature: 0.3
      })
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`LLM 调用失败: ${response.status} ${text}`);
    }

    const data = await response.json();
    return data.content?.[0]?.text || data.choices?.[0]?.message?.content || '';
  }

  throw new Error(`不支持的 Provider: ${provider}`);
}

function generatePlanItems(prompt) {
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

module.exports = {
  getToday,
  getNow,
  callLLM,
  generatePlanItems
};
