import { groupAPI } from '@/api';

// 简单的分组数据缓存服务
class GroupCacheService {
  constructor() {
    this.groups = null;
    this.lastFetchTime = null;
    this.isLoading = false;
    this.cacheTimeout = 30000; // 缓存有效期30秒
    this.callbacks = [];
  }
  
  // 获取分组数据，如果已缓存且未过期则使用缓存
  async getGroups(forceRefresh = false) {
    // 如果强制刷新或缓存过期或没有缓存，则获取新数据
    if (forceRefresh || this.shouldRefresh()) {
      return this.fetchGroups();
    }
    
    // 返回缓存的数据
    return {
      success: true,
      data: this.groups
    };
  }
  
  // 判断是否应该刷新缓存
  shouldRefresh() {
    if (!this.groups || !this.lastFetchTime) return true;
    
    const now = Date.now();
    return now - this.lastFetchTime > this.cacheTimeout;
  }
  
  // 从API获取分组数据
  async fetchGroups() {
    // 如果已经在加载中，返回一个promise等待加载完成
    if (this.isLoading) {
      return new Promise((resolve) => {
        this.callbacks.push(resolve);
      });
    }
    
    this.isLoading = true;
    
    try {
      const response = await groupAPI.getAllGroups();
      if (response.success) {
        this.groups = response.data;
        this.lastFetchTime = Date.now();
      }
      
      // 处理所有等待的回调
      this.callbacks.forEach(callback => callback(response));
      this.callbacks = [];
      
      return response;
    } catch (error) {
      console.error('获取分组失败:', error);
      return {
        success: false,
        error: '获取分组失败'
      };
    } finally {
      this.isLoading = false;
    }
  }
  
  // 清除缓存，强制下次获取从服务器加载
  invalidateCache() {
    this.groups = null;
    this.lastFetchTime = null;
  }
}

// 导出单例
export default new GroupCacheService(); 