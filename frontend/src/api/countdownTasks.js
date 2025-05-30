import axios from 'axios';

const API_URL = '/api';

// 获取所有倒计时任务
export const getAllCountdownTasks = async () => {
  try {
    const response = await axios.get(`${API_URL}/countdown-tasks`);
    return response.data;
  } catch (error) {
    console.error('获取倒计时任务失败:', error);
    throw error;
  }
};

// 获取单个倒计时任务
export const getCountdownTask = async (id) => {
  try {
    const response = await axios.get(`${API_URL}/countdown-tasks/${id}`);
    return response.data;
  } catch (error) {
    console.error(`获取倒计时任务 ${id} 失败:`, error);
    throw error;
  }
};

// 创建倒计时任务
export const createCountdownTask = async (taskData) => {
  try {
    // 使用 FormData 处理文件上传
    const formData = new FormData();
    
    // 添加文本字段
    formData.append('name', taskData.name);
    if (taskData.deadline) {
      formData.append('deadline', taskData.deadline);
    }
    
    // 添加背景图片（如果有）
    if (taskData.backgroundImage) {
      formData.append('background_image', taskData.backgroundImage);
    }
    
    const response = await axios.post(`${API_URL}/countdown-tasks`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    return response.data;
  } catch (error) {
    console.error('创建倒计时任务失败:', error);
    throw error;
  }
};

// 更新倒计时任务
export const updateCountdownTask = async (id, taskData) => {
  try {
    // 使用 FormData 处理文件上传
    const formData = new FormData();
    
    // 添加文本字段
    if (taskData.name) {
      formData.append('name', taskData.name);
    }
    if (taskData.deadline) {
      formData.append('deadline', taskData.deadline);
    }
    
    // 添加背景图片（如果有）
    if (taskData.backgroundImage) {
      formData.append('background_image', taskData.backgroundImage);
    }
    
    const response = await axios.put(`${API_URL}/countdown-tasks/${id}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    return response.data;
  } catch (error) {
    console.error(`更新倒计时任务 ${id} 失败:`, error);
    throw error;
  }
};

// 删除倒计时任务
export const deleteCountdownTask = async (id) => {
  try {
    const response = await axios.delete(`${API_URL}/countdown-tasks/${id}`);
    return response.data;
  } catch (error) {
    console.error(`删除倒计时任务 ${id} 失败:`, error);
    throw error;
  }
}; 