<template>
  <div class="todo-detail">
    <div class="app-layout">
      <!-- 侧边栏 -->
      <SideBar 
        @filter-selected="handleFilterSelected" 
      />
      
      <!-- 主内容区域 -->
      <div class="main-content">
        <div class="card" v-if="todo">
          <div class="header">
            <h2>{{ todo.title }}</h2>
            <span class="status" :class="{ completed: todo.completed }">
              {{ todo.completed ? '已完成' : '未完成' }}
            </span>
          </div>
          
          <div class="meta-info">
            <div v-if="todo.group" class="group" :style="{ borderLeftColor: todo.group_color || '#3498db' }">
              <h3>分组</h3>
              <p>{{ todo.group }}</p>
            </div>
            
            <div v-if="todo.deadline" class="deadline" :class="{ overdue: isOverdue }">
              <h3>截止日期</h3>
              <p>{{ formatDeadline(todo.deadline) }}</p>
            </div>
          </div>
          
          <div class="description" v-if="todo.description">
            <h3>描述</h3>
            <p>{{ todo.description }}</p>
          </div>
          
          <div class="meta">
            <p>创建时间: {{ formatDate(todo.created_at) }}</p>
            <p>更新时间: {{ formatDate(todo.updated_at) }}</p>
          </div>
          
          <div class="actions">
            <button @click="goBack">返回列表</button>
            <button @click="goToEdit">编辑</button>
          </div>
        </div>
        
        <div class="loading" v-else-if="loading">
          <p>加载中...</p>
        </div>
        
        <div class="error" v-else>
          <p>{{ error }}</p>
          <button @click="goBack">返回列表</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import todoApi from '@/api/todo'
import SideBar from '@/components/SideBar.vue'

export default {
  name: 'TodoDetailView',
  components: {
    SideBar
  },
  data() {
    return {
      todo: null,
      loading: true,
      error: null
    }
  },
  created() {
    this.fetchTodo()
  },
  computed: {
    // 判断任务是否已过期
    isOverdue() {
      if (!this.todo || !this.todo.deadline) return false;
      
      const deadline = new Date(this.todo.deadline);
      const now = new Date();
      
      return !this.todo.completed && deadline < now;
    }
  },
  methods: {
    async fetchTodo() {
      try {
        const todoId = this.$route.params.id;
        this.loading = true;
        this.error = null;
        
        const response = await todoApi.getTodo(todoId);
        if (response.success) {
          this.todo = response.data;
        } else {
          this.error = response.error || '无法加载任务详情';
        }
      } catch (error) {
        console.error('获取任务详情失败', error);
        this.error = '无法加载任务详情或任务不存在';
      } finally {
        this.loading = false;
      }
    },
    
    formatDate(dateString) {
      if (!dateString) return '未知';
      
      try {
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return '无效日期';
        
        return new Intl.DateTimeFormat('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        }).format(date);
      } catch (error) {
        console.error('日期格式化错误', error);
        return '无效日期';
      }
    },
    
    formatDeadline(dateString) {
      if (!dateString) return '未知';
      
      try {
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return '无效日期';
        
        return new Intl.DateTimeFormat('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          weekday: 'long'
        }).format(date);
      } catch (error) {
        console.error('日期格式化错误', error);
        return '无效日期';
      }
    },
    
    goToEdit() {
      this.$router.push('/');
    },
    
    goBack() {
      this.$router.push('/');
    },
    
    handleFilterSelected(filter) {
      // 重定向到首页并应用筛选
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
.todo-detail {
  height: 100%;
}

.app-layout {
  display: flex;
  height: 100%;
  overflow: hidden;
}

.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
  background-color: #e74c3c;
  color: white;
}

.status.completed {
  background-color: #2ecc71;
}

.meta-info {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
}

.group, .deadline {
  background-color: #f8f9fa;
  padding: 10px 15px;
  border-radius: 6px;
  min-width: 200px;
}

.group {
  border-left: 4px solid #3498db;
}

.group h3, .deadline h3 {
  font-size: 14px;
  margin-bottom: 5px;
  color: #7f8c8d;
}

.group p {
  color: #3498db;
  font-weight: bold;
}

.deadline p {
  color: #27ae60;
  font-weight: bold;
}

.deadline.overdue p {
  color: #e74c3c;
}

.description {
  margin-bottom: 20px;
}

.description h3 {
  margin-bottom: 10px;
  color: #3498db;
}

.meta {
  margin-bottom: 20px;
  font-size: 14px;
  color: #7f8c8d;
}

.meta p {
  margin-bottom: 5px;
}

.actions {
  display: flex;
  gap: 10px;
}

.loading, .error {
  text-align: center;
  padding: 40px 0;
}

.error p {
  margin-bottom: 20px;
  color: #e74c3c;
}
</style> 