/**
 * LogAdapter — 日志适配器
 * 封装核心 Log API
 */

export class LogAdapter {
  constructor(logAPI) {
    this.log = logAPI;
  }

  async write(entry) {
    await this.log.write(entry);
  }

  async read(options) {
    return this.log.read(options);
  }

  async query(options) {
    return this.log.query(options);
  }
}
