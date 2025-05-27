import axios from 'axios';

// 创建axios实例，设置基础配置
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  timeout: 10000 // 请求超时时间
});

// 请求拦截器
api.interceptors.request.use(
  config => {
    console.log('API请求:', config.method.toUpperCase(), config.url);
    return config;
  },
  error => {
    console.error('请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  response => {
    console.log('API响应成功:', response.config.url);
    return response;
  },
  error => {
    console.error('API响应错误:', error.response?.status, error.message);
    return Promise.reject(error);
  }
);

export default api; 