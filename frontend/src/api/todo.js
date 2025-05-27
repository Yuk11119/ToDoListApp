import axios from 'axios';

const BASE_URL = '/api';

// Todo相关API
export default {
  // 获取所有任务
  getAllTodos: async () => {
    try {
      const response = await axios.get(`${BASE_URL}/todos`);
      return response.data;
    } catch (error) {
      console.error('获取所有任务失败:', error);
      throw error;
    }
  },

  // 获取单个任务
  getTodo: async (id) => {
    try {
      const response = await axios.get(`${BASE_URL}/todos/${id}`);
      return response.data;
    } catch (error) {
      console.error(`获取任务 ${id} 失败:`, error);
      throw error;
    }
  },

  // 按分组获取任务
  getTodosByGroup: async (groupId) => {
    try {
      const response = await axios.get(`${BASE_URL}/todos?group_id=${groupId}`);
      return response.data;
    } catch (error) {
      console.error(`获取分组 ${groupId} 的任务失败:`, error);
      throw error;
    }
  },

  // 创建新任务
  createTodo: async (todoData) => {
    try {
      const response = await axios.post(`${BASE_URL}/todos`, todoData);
      return response.data;
    } catch (error) {
      console.error('创建任务失败:', error);
      throw error;
    }
  },

  // 更新任务
  updateTodo: async (id, todoData) => {
    try {
      const response = await axios.put(`${BASE_URL}/todos/${id}`, todoData);
      return response.data;
    } catch (error) {
      console.error(`更新任务 ${id} 失败:`, error);
      throw error;
    }
  },

  // 删除任务
  deleteTodo: async (id) => {
    try {
      const response = await axios.delete(`${BASE_URL}/todos/${id}`);
      return response.data;
    } catch (error) {
      console.error(`删除任务 ${id} 失败:`, error);
      throw error;
    }
  },

  // 获取所有分组
  getAllGroups: async () => {
    try {
      const response = await axios.get(`${BASE_URL}/groups`);
      return response.data;
    } catch (error) {
      console.error('获取所有分组失败:', error);
      throw error;
    }
  }
}; 