import axios from 'axios';

const API_URL = '/api';

// 任务相关API
export const todoAPI = {
  // 获取所有任务
  getAllTodos: async () => {
    const response = await axios.get(`${API_URL}/todos`);
    return response.data;
  },

  // 获取单个任务
  getTodo: async (id) => {
    const response = await axios.get(`${API_URL}/todos/${id}`);
    return response.data;
  },

  // 按分组获取任务
  getTodosByGroup: async (groupId) => {
    const response = await axios.get(`${API_URL}/todos?group_id=${groupId}`);
    return response.data;
  },

  // 创建任务
  createTodo: async (todoData) => {
    const response = await axios.post(`${API_URL}/todos`, todoData);
    return response.data;
  },

  // 更新任务
  updateTodo: async (id, todoData) => {
    const response = await axios.put(`${API_URL}/todos/${id}`, todoData);
    return response.data;
  },

  // 删除任务
  deleteTodo: async (id) => {
    const response = await axios.delete(`${API_URL}/todos/${id}`);
    return response.data;
  }
};

// 分组相关API
export const groupAPI = {
  // 获取所有分组
  getAllGroups: async () => {
    const response = await axios.get(`${API_URL}/groups`);
    return response.data;
  },

  // 获取单个分组
  getGroup: async (id) => {
    const response = await axios.get(`${API_URL}/groups/${id}`);
    return response.data;
  },

  // 创建分组
  createGroup: async (groupData) => {
    const response = await axios.post(`${API_URL}/groups`, groupData);
    return response.data;
  },

  // 更新分组
  updateGroup: async (id, groupData) => {
    const response = await axios.put(`${API_URL}/groups/${id}`, groupData);
    return response.data;
  },

  // 删除分组
  deleteGroup: async (id) => {
    const response = await axios.delete(`${API_URL}/groups/${id}`);
    return response.data;
  }
};

// 时间段任务相关API
export const timeBlockAPI = {
  // 获取所有时间段
  getAllTimeBlocks: async () => {
    const response = await axios.get(`${API_URL}/timeblocks`);
    return response.data;
  },

  // 获取单个时间段
  getTimeBlock: async (id) => {
    const response = await axios.get(`${API_URL}/timeblocks/${id}`);
    return response.data;
  },

  // 创建时间段
  createTimeBlock: async (data) => {
    const response = await axios.post(`${API_URL}/timeblocks`, data);
    return response.data;
  },

  // 更新时间段
  updateTimeBlock: async (id, data) => {
    const response = await axios.put(`${API_URL}/timeblocks/${id}`, data);
    return response.data;
  },

  // 删除时间段
  deleteTimeBlock: async (id) => {
    const response = await axios.delete(`${API_URL}/timeblocks/${id}`);
    return response.data;
  },

  // 获取时间段下的所有子任务
  getSubTasks: async (timeBlockId) => {
    const response = await axios.get(`${API_URL}/timeblocks/${timeBlockId}/subtasks`);
    return response.data;
  },

  // 创建子任务
  createSubTask: async (timeBlockId, data) => {
    const response = await axios.post(`${API_URL}/timeblocks/${timeBlockId}/subtasks`, data);
    return response.data;
  },

  // 更新子任务
  updateSubTask: async (timeBlockId, subtaskId, data) => {
    const response = await axios.put(`${API_URL}/timeblocks/${timeBlockId}/subtasks/${subtaskId}`, data);
    return response.data;
  },

  // 删除子任务
  deleteSubTask: async (timeBlockId, subtaskId) => {
    const response = await axios.delete(`${API_URL}/timeblocks/${timeBlockId}/subtasks/${subtaskId}`);
    return response.data;
  },

  // 重新排序子任务
  reorderSubTasks: async (timeBlockId, orderData) => {
    const response = await axios.post(`${API_URL}/timeblocks/${timeBlockId}/subtasks/reorder`, orderData);
    return response.data;
  }
};

export default {
  todoAPI,
  groupAPI,
  timeBlockAPI
}; 