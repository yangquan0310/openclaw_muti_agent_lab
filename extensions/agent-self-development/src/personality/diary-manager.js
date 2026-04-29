/**
 * DiaryManager — 日记业务逻辑
 * 管理 Diary 对象：每日发展日记的创建、查询和信号提取
 */

export class DiaryManager {
  constructor(memoryAdapter) {
    this.memory = memoryAdapter;
  }

  /**
   * 创建或更新某日的日记
   */
  async createDiary(date, content) {
    const diary = {
      date,
      content,
      createdAt: Date.now(),
      updatedAt: Date.now()
    };
    await this.memory.saveDiary(date, diary);
    return diary;
  }

  /**
   * 获取某日的日记
   */
  async getDiary(date) {
    return this.memory.getDiary(date);
  }

  /**
   * 提取日记中的更新触发信号
   */
  async extractSignals(date) {
    const diary = await this.getDiary(date);
    if (!diary || !diary.content) return [];

    // TODO: 实现信号提取逻辑（同化/顺应判定）
    return [];
  }
}
