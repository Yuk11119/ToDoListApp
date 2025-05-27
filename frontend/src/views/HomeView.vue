<template>
  <div class="home">
    <div class="app-layout">
      <!-- 侧边栏 -->
      <SideBar 
        @filter-selected="applyFilter" 
        ref="sidebar"
      />
      
      <!-- 主内容区域 -->
      <div class="main-content">
        <div v-if="loading && !showForm" class="loading">
          加载中...
        </div>
        
        <div v-else-if="error" class="error">
          {{ error }}
        </div>
        
        <div v-else>
          <h2 class="page-title">{{ pageTitle }}</h2>
          
          <button class="add-button" @click="showForm = true" v-if="!showForm">添加新任务</button>
          
          <div class="todo-list" v-if="filteredTodos && filteredTodos.length > 0">
            <TodoItem 
              v-for="todo in filteredTodos" 
              :key="todo.id" 
              :todo="todo"
              @toggle="updateTodo"
              @edit="editTodo"
              @delete="deleteTodo"
            />
          </div>
          
          <div class="empty-state" v-else>
            <p>{{ emptyStateMessage }}</p>
          </div>
        </div>
        
        <!-- 使用条件渲染来显示TodoForm，而不是在v-else块内 -->
        <TodoForm 
          v-if="showForm" 
          :todo="currentTodo" 
          :isEdit="isEditing" 
          @submit="saveTodo" 
          @cancel="cancelForm"
        />
      </div>
    </div>
  </div>
</template>

<script>
import TodoItem from '@/components/TodoItem.vue'
import TodoForm from '@/components/TodoForm.vue'
import SideBar from '@/components/SideBar.vue'
import todoApi from '@/api/todo'

export default {
  name: 'HomeView',
  components: {
    TodoItem,
    TodoForm,
    SideBar
  },
  data() {
    return {
      todos: [],
      showForm: false,
      currentTodo: {},
      isEditing: false,
      loading: false,
      error: null,
      currentFilter: { type: 'filter', id: 'all' },
      filterCounts: {
        today: 0,
        scheduled: 0,
        all: 0,
        flagged: 0,
        completed: 0
      }
    }
  },
  computed: {
    filteredTodos() {
      if (!this.todos) return [];
      
      const { type, id } = this.currentFilter;
      
      if (type === 'filter') {
        switch (id) {
          case 'today':
            // 筛选今天的任务
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            const tomorrow = new Date(today);
            tomorrow.setDate(tomorrow.getDate() + 1);
            
            return this.todos.filter(todo => {
              if (!todo.deadline) return false;
              const deadline = new Date(todo.deadline);
              return deadline >= today && deadline < tomorrow;
            });
            
          case 'scheduled':
            // 筛选有截止日期的任务
            return this.todos.filter(todo => todo.deadline);
            
          case 'all':
            // 返回所有任务
            return this.todos;
            
          case 'flagged':
            // 在实际项目中，可以添加标记功能
            // 目前先返回空数组
            return [];
            
          case 'completed':
            // 筛选已完成的任务
            return this.todos.filter(todo => todo.completed);
            
          default:
            return this.todos;
        }
      } else if (type === 'group') {
        // 按分组筛选
        return this.todos.filter(todo => todo.group_id === parseInt(id));
      }
      
      return this.todos;
    },
    
    pageTitle() {
      const { type, id } = this.currentFilter;
      
      if (type === 'filter') {
        switch (id) {
          case 'today': return '今天';
          case 'scheduled': return '计划';
          case 'all': return '全部';
          case 'flagged': return '旗标';
          case 'completed': return '已完成';
          default: return '任务列表';
        }
      } else if (type === 'group') {
        // 查找分组名称
        const group = this.$refs.sidebar?.groups.find(g => g.id === parseInt(id));
        return group ? group.name : '分组';
      }
      
      return '任务列表';
    },
    
    emptyStateMessage() {
      const { type, id } = this.currentFilter;
      
      if (type === 'filter') {
        switch (id) {
          case 'today': return '今天没有任务，添加一些计划吧！';
          case 'scheduled': return '暂无计划中的任务';
          case 'all': return '暂无任务，点击"添加新任务"按钮创建一个吧！';
          case 'flagged': return '暂无标记的任务';
          case 'completed': return '暂无已完成的任务';
          default: return '暂无任务';
        }
      } else if (type === 'group') {
        return '该分组下暂无任务';
      }
      
      return '暂无任务';
    }
  },
  created() {
    this.fetchTodos();
  },
  methods: {
    async fetchTodos() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await todoApi.getAllTodos();
        // 适配新的API响应结构
        if (response.success) {
          this.todos = response.data || [];
          this.updateFilterCounts();
        } else {
          this.error = response.error || '获取任务列表失败';
        }
      } catch (error) {
        console.error('获取任务列表失败', error);
        this.error = '无法加载任务列表';
      } finally {
        this.loading = false;
      }
    },
    
    updateFilterCounts() {
      // 计算每个筛选选项的任务数量
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      const tomorrow = new Date(today);
      tomorrow.setDate(tomorrow.getDate() + 1);
      
      const counts = {
        all: this.todos.length,
        today: this.todos.filter(todo => {
          if (!todo.deadline) return false;
          const deadline = new Date(todo.deadline);
          return deadline >= today && deadline < tomorrow;
        }).length,
        scheduled: this.todos.filter(todo => todo.deadline).length,
        flagged: 0, // 暂不实现
        completed: this.todos.filter(todo => todo.completed).length
      };
      
      this.filterCounts = counts;
      
      // 如果侧边栏组件已经渲染，更新它的计数
      if (this.$refs.sidebar) {
        this.$refs.sidebar.updateCounts(counts);
      }
    },
    
    applyFilter(filter) {
      this.currentFilter = filter;
    },
    
    async saveTodo(formData) {
      try {
        if (!formData || !formData.title || formData.title.trim() === '') {
          alert('任务标题不能为空！');
          return;
        }
        
        const todoData = {
          title: formData.title,
          description: formData.description || '',
          group_id: formData.group_id,
          deadline: formData.deadline,
          completed: formData.completed || false
        };
        
        // 不再显示加载状态，这会影响弹窗的显示
        let newTodo;
        
        if (this.isEditing) {
          const response = await todoApi.updateTodo(this.currentTodo.id, todoData);
          if (response.success) {
            newTodo = response.data;
            // 本地更新而不是重新获取
            const index = this.todos.findIndex(t => t.id === this.currentTodo.id);
            if (index !== -1 && newTodo) {
              this.todos.splice(index, 1, newTodo);
            }
          }
        } else {
          const response = await todoApi.createTodo(todoData);
          if (response.success && response.data) {
            // 本地添加而不是重新获取
            this.todos.push(response.data);
          }
        }
        
        // 更新过滤器计数
        this.updateFilterCounts();
        this.cancelForm();
      } catch (error) {
        console.error('保存任务失败', error);
        if (error.response) {
          console.error('错误响应:', error.response.data);
        }
        // 发生错误时重新获取数据以确保同步
        await this.fetchTodos();
      }
    },
    
    async updateTodo(todo) {
      try {
        // 只有在API调用期间才显示loading状态
        const originalTodo = this.todos.find(t => t.id === todo.id);
        // 本地先更新，提供即时反馈
        const todoIndex = this.todos.findIndex(t => t.id === todo.id);
        if (todoIndex !== -1) {
          this.todos.splice(todoIndex, 1, todo);
          this.updateFilterCounts();
        }
        
        // 后台静默发送API请求，不显示loading状态
        await todoApi.updateTodo(todo.id, todo);
      } catch (error) {
        console.error('更新任务失败', error);
        // 如果API请求失败，回滚到原始状态
        if (originalTodo) {
          const todoIndex = this.todos.findIndex(t => t.id === todo.id);
          if (todoIndex !== -1) {
            this.todos.splice(todoIndex, 1, originalTodo);
            this.updateFilterCounts();
          }
        }
      }
    },
    
    async deleteTodo(id) {
      if (confirm('确定要删除这个任务吗？')) {
        try {
          // 保存被删除的任务以便出错时恢复
          const deletedTodoIndex = this.todos.findIndex(t => t.id === id);
          const deletedTodo = deletedTodoIndex !== -1 ? this.todos[deletedTodoIndex] : null;
          
          // 本地先删除，提供即时反馈
          if (deletedTodoIndex !== -1) {
            this.todos.splice(deletedTodoIndex, 1);
            this.updateFilterCounts();
          }
          
          // 后台静默发送API请求，不显示loading状态
          await todoApi.deleteTodo(id);
        } catch (error) {
          console.error('删除任务失败', error);
          // 如果API请求失败，恢复被删除的任务
          if (deletedTodo) {
            this.todos.push(deletedTodo);
            this.updateFilterCounts();
          }
        }
      }
    },
    
    editTodo(id) {
      const todo = this.todos.find(t => t.id === id);
      if (todo) {
        this.currentTodo = todo;
        this.isEditing = true;
        this.showForm = true;
      }
    },
    
    cancelForm() {
      this.showForm = false;
      this.currentTodo = {};
      this.isEditing = false;
    }
  }
}
</script>

<style scoped>
.home {
  height: 100%;
}

.app-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.main-content {
  flex: 1;
  padding: 24px 32px;
  overflow-y: auto;
  background-color: #f8f9fa;
}

.page-title {
  margin-bottom: 24px;
  color: #2d3436;
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.add-button {
  margin-bottom: 24px;
  padding: 12px 24px;
  font-size: 15px;
  font-weight: 500;
  background-color: #4cd137;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 12px rgba(76, 209, 55, 0.2);
}

.add-button:before {
  content: "+";
  margin-right: 8px;
  font-size: 18px;
  font-weight: 600;
}

.add-button:hover {
  background-color: #44bd32;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(76, 209, 55, 0.3);
}

.todo-list {
  margin-top: 24px;
  padding-bottom: 32px;
}

.empty-state {
  text-align: center;
  padding: 60px 40px;
  color: #636e72;
  background-color: white;
  border-radius: 16px;
  margin-top: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #f0f0f0;
}

.empty-state p {
  font-size: 16px;
  line-height: 1.6;
}

.empty-state:before {
  content: "📋";
  display: block;
  font-size: 48px;
  margin-bottom: 16px;
}

.loading, .error {
  text-align: center;
  padding: 32px 24px;
  margin: 24px 0;
  border-radius: 16px;
  font-size: 16px;
}

.loading {
  background-color: white;
  color: #636e72;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #f0f0f0;
}

.loading:before {
  content: "⏳";
  display: block;
  font-size: 32px;
  margin-bottom: 16px;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.error {
  background-color: #fff5f5;
  color: #e74c3c;
  border: 1px solid #ffd3d3;
}

.error:before {
  content: "⚠️";
  display: block;
  font-size: 32px;
  margin-bottom: 16px;
}

@media (max-width: 768px) {
  .main-content {
    padding: 16px;
  }
  
  .page-title {
    font-size: 24px;
  }
}
</style> 