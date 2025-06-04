/**
 * 格式化日期，将输出的日期精确到天
 * @param {Date|string} date - 日期对象或日期字符串
 * @param {string} format - 格式化模式
 * @returns {string} 格式化后的日期字符串
 * 
 * 支持的格式:
 * YYYY: 年份，如 2023
 * MM: 月份，如 01-12
 * DD: 日期，如 01-31
 */
export function formatDate(date, format = 'YYYY-MM-DD') {
  if (!date) return '';
  
  const d = typeof date === 'string' ? new Date(date) : date;
  
  if (isNaN(d.getTime())) {
    console.error('Invalid date:', date);
    return '';
  }
  
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  
  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day);
}

/**
 * 格式化日期范围
 * @param {string} startDate - 开始日期字符串
 * @param {string} endDate - 结束日期字符串
 * @returns {string} 格式化后的日期范围字符串
 */
export function formatDateRange(startDate, endDate) {
  if (!startDate || !endDate) return '';
  
  const start = new Date(startDate);
  const end = new Date(endDate);
  
  return `${formatDate(start, 'YYYY-MM-DD')} 至 ${formatDate(end, 'YYYY-MM-DD')}`;
}

/**
 * 格式化日期为HTML日期输入控件格式 (YYYY-MM-DD)
 * @param {string} dateString - ISO日期字符串
 * @returns {string} 格式化后的日期字符串，适用于日期输入控件
 */
export function formatDateForInput(dateString) {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  if (isNaN(date.getTime())) return '';
  
  return formatDate(date, 'YYYY-MM-DD');
}

/**
 * 计算两个日期之间的差值（天数）
 * @param {Date|string} date1 - 第一个日期
 * @param {Date|string} date2 - 第二个日期
 * @returns {number} 两个日期之间的天数差
 */
export function dateDiffInDays(date1, date2) {
  const d1 = typeof date1 === 'string' ? new Date(date1) : date1;
  const d2 = typeof date2 === 'string' ? new Date(date2) : date2;
  
  if (isNaN(d1.getTime()) || isNaN(d2.getTime())) {
    console.error('Invalid date:', date1, date2);
    return 0;
  }
  
  // 设置时间为00:00:00，只比较日期部分
  const date1UTC = Date.UTC(d1.getFullYear(), d1.getMonth(), d1.getDate());
  const date2UTC = Date.UTC(d2.getFullYear(), d2.getMonth(), d2.getDate());
  
  // 计算天数差（1天 = 86400000毫秒）
  return Math.abs(Math.floor((date2UTC - date1UTC) / 86400000));
}

/**
 * 检查日期是否今天
 * @param {Date|string} date - 要检查的日期
 * @returns {boolean} 如果是今天则返回true
 */
export function isToday(date) {
  const d = typeof date === 'string' ? new Date(date) : date;
  const today = new Date();
  
  return d.getDate() === today.getDate() &&
         d.getMonth() === today.getMonth() &&
         d.getFullYear() === today.getFullYear();
} 