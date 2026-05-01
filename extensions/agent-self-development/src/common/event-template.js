/**
 * Event 模板与工具函数
 */

export function createEventTemplate(type, data) {
  const templates = {
    plan: {
      title: '计划制定',
      fields: ['runId', 'goal', 'phaseCount', 'successCriteria']
    },
    deviation: {
      title: '偏差检测',
      fields: ['runId', 'phaseId', 'expected', 'actual', 'gap']
    },
    attribution: {
      title: '归因调节',
      fields: ['runId', 'deviationId', 'rootCause', 'adjustmentType']
    },
    session: {
      title: '会话变更',
      fields: ['sessionId', 'taskFamily', 'status', 'action']
    },
    tool: {
      title: '工具调用',
      fields: ['toolName', 'status', 'error', 'duration']
    }
  };

  const template = templates[type] || { title: '未知事件', fields: [] };
  return {
    type,
    title: template.title,
    timestamp: Date.now(),
    data: Object.fromEntries(
      template.fields.map(f => [f, data[f] ?? null])
    )
  };
}
