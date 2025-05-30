<template>
  <div class="countdown-task" :style="backgroundStyle">
    <div class="countdown-content">
      <h2 class="task-name">{{ task.name }}</h2>
      <div class="countdown">
        <div class="days">
          <span class="number">{{ daysLeft }}</span>
          <span class="label">天</span>
        </div>
      </div>
      <div class="deadline">
        截止日期: {{ formattedDeadline }}
      </div>
      <div class="actions">
        <button class="edit-btn" @click="$emit('edit', task)">
          <i class="fas fa-edit"></i> 编辑
        </button>
        <button class="delete-btn" @click="$emit('delete', task.id)">
          <i class="fas fa-trash"></i> 删除
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CountdownTask',
  props: {
    task: {
      type: Object,
      required: true
    }
  },
  computed: {
    daysLeft() {
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      
      const deadline = new Date(this.task.deadline);
      deadline.setHours(0, 0, 0, 0);
      
      const diffTime = deadline - today;
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      
      return diffDays > 0 ? diffDays : 0;
    },
    
    formattedDeadline() {
      const date = new Date(this.task.deadline);
      return date.toLocaleDateString('zh-CN');
    },
    
    backgroundStyle() {
      if (this.task.background_image_path) {
        // 获取API的基础URL（通常是后端服务器URL）
        const baseURL = import.meta.env.VITE_API_BASE_URL || '';
        
        return {
          backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.1)), url(${baseURL}/${this.task.background_image_path})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        };
      } else {
        // 默认渐变背景
        return {
          background: 'linear-gradient(135deg, #3f51b5 0%, #7e57c2 100%)'
        };
      }
    }
  }
};
</script>

<style scoped>
.countdown-task {
  width: 100%;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 20px;
  color: white;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease;
}

.countdown-task:hover {
  transform: translateY(-5px);
}

.countdown-content {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.task-name {
  margin: 0 0 15px 0;
  font-size: 1.8rem;
  font-weight: 600;
}

.countdown {
  display: flex;
  justify-content: center;
  margin-bottom: 15px;
}

.days {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.number {
  font-size: 3rem;
  font-weight: 700;
  line-height: 1;
}

.label {
  font-size: 1rem;
  margin-top: 5px;
}

.deadline {
  font-size: 1rem;
  margin-bottom: 15px;
}

.actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

button {
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  gap: 5px;
}

.edit-btn {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
}

.edit-btn:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

.delete-btn {
  background-color: rgba(244, 67, 54, 0.7);
  color: white;
}

.delete-btn:hover {
  background-color: rgba(244, 67, 54, 0.9);
}
</style> 