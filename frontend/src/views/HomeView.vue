<template>
  <div class="home">
    <div class="app-layout">
      <!-- 侧边栏 -->
      <SideBar 
        @filter-selected="applyFilter" 
        @group-updated="refreshTodos"
        ref="sidebar"
      />
      
      <!-- 主内容区域 -->
      <div class="main-content" @click="handleMainContentClick">
        <div v-if="loading && !showForm && !showCountdownForm" class="loading">
          加载中...
        </div>
        
        <div v-else-if="error" class="error">
          {{ error }}
        </div>
        
        <div v-else>
          <h2 class="page-title">{{ pageTitle }}</h2>
          
          <!-- 倒计时任务区域 -->
          <div class="countdown-tasks-section" v-if="countdownTasks.length > 0 || currentFilter.id === 'all'">
            <div class="section-header">
              <h3>倒计时任务</h3>
              <button class="add-countdown-btn" @click="showCountdownForm = true">
                <i class="fas fa-plus"></i> 添加倒计时
              </button>
            </div>
            
            <div class="countdown-tasks-list">
              <CountdownTask 
                v-for="task in countdownTasks" 
                :key="task.id" 
                :task="task"
                @edit="editCountdownTask"
                @delete="deleteCountdownTask"
          />
            </div>
          </div>
          
          <!-- 常规任务列表标题 -->
          <div class="section-header" v-if="countdownTasks.length > 0">
            <h3>待办事项</h3>
          </div>
          
          <!-- 常规任务列表，添加动画 -->
          <transition-group name="todo-list" tag="div" class="todo-list">
            <TodoItem 
              v-for="todo in filteredTodos" 
              :key="todo.id" 
              :todo="todo"
              :is-fading="todo.isCompleting"
              :class="{ 'no-animation-item': todo._skipAnimation }"
              @toggle="updateTodo"
              @edit="editTodo"
              @delete="deleteTodo"
              @transition-end="handleTransitionEnd"
            />
            
            <!-- 临时新任务使用transition包裹，单独添加动画 -->
            <transition 
              :name="isCancelling ? 'new-task' : (isSilentRemoval ? 'no-animation' : 'new-task-no-leave')" 
              :key="'new-task'"
              @before-leave="beforeTaskLeave"
              @after-leave="afterTaskLeave"
              @before-enter="beforeTaskEnter">
              <TodoItem 
                v-if="newTodo" 
                :key="newTodo.id"
                :todo="newTodo" 
                :isNew="true"
                @toggle="saveTempTodo"
                @delete="cancelTempTodo"
              />
            </transition>
          </transition-group>
        </div>
        
        <!-- 使用条件渲染来显示TodoForm，而不是在v-else块内 -->
        <TodoForm 
          v-if="showForm" 
          :todo="currentTodo" 
          :isEdit="isEditing" 
          @submit="saveTodo" 
          @cancel="cancelForm"
        />
        
        <!-- 倒计时任务表单 -->
        <CountdownTaskForm
          v-if="showCountdownForm"
          :task="currentCountdownTask"
          @submit="saveCountdownTask"
          @close="closeCountdownForm"
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
import CountdownTask from '@/components/CountdownTask.vue'
import CountdownTaskForm from '@/components/CountdownTaskForm.vue'
import { getAllCountdownTasks, createCountdownTask, updateCountdownTask, deleteCountdownTask } from '@/api/countdownTasks'

export default {
  name: 'HomeView',
  components: {
    TodoItem,
    TodoForm,
    SideBar,
    CountdownTask,
    CountdownTaskForm
  },
  data() {
    return {
      todos: [],
      countdownTasks: [],
      showForm: false,
      showCountdownForm: false,
      currentTodo: {},
      currentCountdownTask: null,
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
      },
      newTodo: null, // 临时创建的新任务
      isCreatingTask: false, // 防止快速重复创建标记
      isCancelling: false, // 标记是否为取消操作
      isSilentRemoval: false // 新增：标记是否为静默移除（不显示动画）
    }
  },
  computed: {
    filteredTodos() {
      if (!this.todos) return [];
      
      const { type, id } = this.currentFilter;
      
      // 使用单次过滤操作代替多次过滤和拼接，减少不必要的数组操作
      return this.todos.filter(todo => {
        // 如果是正在完成状态的任务，始终显示（无论在哪个视图）
        if (todo.isCompleting) {
          return true;
        }
        
        // 已完成任务仅在"已完成"视图显示
        if (todo.completed && id !== 'completed') {
          return false;
        }
      
      if (type === 'filter') {
        switch (id) {
            case 'today': {
            // 筛选今天的任务
              if (!todo.deadline) return false;
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            const tomorrow = new Date(today);
            tomorrow.setDate(tomorrow.getDate() + 1);
              const deadline = new Date(todo.deadline);
              return deadline >= today && deadline < tomorrow;
            }
          case 'scheduled':
            // 筛选有截止日期的任务
              return !!todo.deadline;
          case 'all':
              // 返回全部任务（已排除已完成）
              return true;
          case 'flagged':
            // 在实际项目中，可以添加标记功能
              return false;
          case 'completed':
              // 已完成任务视图
              return todo.completed;
          default:
              return true;
        }
      } else if (type === 'group') {
        // 按分组筛选
          return todo.group_id === parseInt(id);
      }
      
        return true;
      });
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
    this.fetchCountdownTasks();
    
    // 检查URL参数
    const queryParams = this.$route.query;
    
    // 处理编辑任务参数
    if (queryParams.editTask) {
      // 等待任务加载完成后，编辑指定任务
      this.$watch('todos', (newTodos) => {
        if (newTodos.length > 0) {
          const taskToEdit = newTodos.find(t => t.id == queryParams.editTask);
          if (taskToEdit) {
            this.editTodo(taskToEdit.id);
          }
        }
      }, { immediate: true });
    }
    
    // 处理过滤参数
    if (queryParams.filter && queryParams.id) {
      this.currentFilter = {
        type: queryParams.filter,
        id: queryParams.filter === 'group' ? parseInt(queryParams.id) : queryParams.id
      };
      // 更新侧边栏选中状态
      this.$nextTick(() => {
        if (this.$refs.sidebar) {
          if (queryParams.filter === 'filter') {
            this.$refs.sidebar.selectFilter(queryParams.id);
          } else if (queryParams.filter === 'group') {
            this.$refs.sidebar.selectGroup(parseInt(queryParams.id));
          }
        }
      });
    }
    
    // 清除URL参数，避免刷新页面时重复应用
    if (Object.keys(queryParams).length > 0) {
      this.$router.replace({ path: this.$route.path });
    }
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
    
    async fetchCountdownTasks() {
      try {
        const tasks = await getAllCountdownTasks();
        this.countdownTasks = tasks;
      } catch (error) {
        console.error('获取倒计时任务失败', error);
      }
    },
    
    updateFilterCounts() {
      // 计算每个筛选选项的任务数量
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      const tomorrow = new Date(today);
      tomorrow.setDate(tomorrow.getDate() + 1);
      
      const counts = {
        all: this.todos.filter(todo => !todo.completed).length, // 只统计未完成任务
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
        const originalTodo = this.todos.find(t => t.id === todo.id);
        const todoIndex = this.todos.findIndex(t => t.id === todo.id);
        
        // 检查是否从未完成变为已完成
        const isNewlyCompleted = !originalTodo.completed && todo.completed;
        
        // 检查是否从已完成变为未完成（撤销完成）
        const isUndo = originalTodo.completed && !todo.completed;
        
        if (isNewlyCompleted) {
          // 添加过渡标记，但不立即从视图中删除
          todo.isCompleting = true;
        }
        
        // 如果是撤销完成操作，立即移除isCompleting标记
        if (isUndo && originalTodo.isCompleting) {
          delete todo.isCompleting;
        }
        
        // 本地先更新，提供即时反馈
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
    },
    
    // 处理主内容区域的点击事件
    handleMainContentClick(event) {
      // 如果已经有弹窗或正在创建任务中，则不处理
      if (this.showForm || this.isCreatingTask) {
        return;
      }
      
      // 如果点击的是TodoItem内部元素，不做处理
      if (event.target.closest('.todo-item')) {
        return;
      }
      
      // 如果有正在编辑的新任务，先处理它
      if (this.newTodo) {
        this.cancelTempTodo();
        // 防止同一次点击创建新任务
        event.stopPropagation();
        event.preventDefault();
        return;
      }
      
      // 判断点击区域是否为空白区域（不是任务项）
      const isEmptyAreaClick = event.target.classList.contains('main-content') || 
                              event.target.classList.contains('todo-list') ||
                              (event.target.classList.contains('empty-state') || 
                               event.target.closest('.empty-state'));
      
      if (isEmptyAreaClick) {
        // 设置创建状态为true
        this.isCreatingTask = true;
        
        // 创建一个临时新任务
        this.newTodo = {
          id: 'temp-' + Date.now(), // 临时ID
          title: '',
          description: '',
          completed: false,
          group_id: null,
          deadline: null
        };
        
        // 延迟重置创建状态
        setTimeout(() => {
          this.isCreatingTask = false;
        }, 300);
      }
    },
    
    // 保存临时创建的任务
    async saveTempTodo(todo) {
      // 设置创建状态为true，防止重复创建
      this.isCreatingTask = true;
      this.isCancelling = false; // 标记为非取消操作
      
      // 如果标题为空，则取消创建
      if (!todo.title || todo.title.trim() === '') {
        this.cancelTempTodo();
        // 延迟重置创建状态
        setTimeout(() => {
          this.isCreatingTask = false;
        }, 300);
        return;
      }
      
      // 创建新任务
      try {
        const todoData = {
          title: todo.title,
          description: todo.description || '',
          group_id: todo.group_id,
          deadline: todo.deadline,
          completed: todo.completed || false
        };
        
        // 先将临时ID保存下来
        const tempId = this.newTodo.id;
        
        const response = await todoApi.createTodo(todoData);
        if (response.success && response.data) {
          // 直接添加到todos数组，不使用动画
          this.todos.push({
            ...response.data,
            _skipAnimation: true // 添加标记指示跳过动画
          });
          this.updateFilterCounts();
        }
      } catch (error) {
        console.error('保存任务失败', error);
        if (error.response) {
          console.error('错误响应:', error.response.data);
        }
        // 发生错误时重新获取数据以确保同步
        await this.fetchTodos();
      } finally {
        // 静默移除临时任务，添加特殊标记避免动画
        this.isSilentRemoval = true;
        this.newTodo = null;
        
        // 短暂延时后重置状态
        setTimeout(() => {
          this.isSilentRemoval = false;
          this.isCreatingTask = false;
        }, 50); // 非常短的延时，仅确保DOM更新
      }
    },
    
    // 取消临时创建的任务
    cancelTempTodo() {
      this.isCancelling = true; // 标记为取消操作
      
      // 先开始动画
      this.isCreatingTask = true;
      
      // 确保状态变更在下一帧（动画开始后）
      requestAnimationFrame(() => {
        this.newTodo = null;
        
        // 在动画持续时间结束后重置状态
        setTimeout(() => {
          requestAnimationFrame(() => {
            this.isCreatingTask = false;
            this.isCancelling = false; // 重置取消标记
          });
        }, 400);
      });
    },
    
    // 倒计时任务相关方法
    editCountdownTask(task) {
      this.currentCountdownTask = task;
      this.showCountdownForm = true;
    },
    
    closeCountdownForm() {
      this.showCountdownForm = false;
      this.currentCountdownTask = null;
    },
    
    async saveCountdownTask(formData) {
      try {
        if (this.currentCountdownTask) {
          // 更新
          await updateCountdownTask(this.currentCountdownTask.id, formData);
        } else {
          // 创建
          await createCountdownTask(formData);
        }
        
        // 重新获取最新的倒计时任务列表
        await this.fetchCountdownTasks();
        this.closeCountdownForm();
      } catch (error) {
        console.error('保存倒计时任务失败', error);
      }
    },
    
    async deleteCountdownTask(id) {
      if (confirm('确定要删除这个倒计时任务吗？')) {
        try {
          await deleteCountdownTask(id);
          await this.fetchCountdownTasks();
        } catch (error) {
          console.error('删除倒计时任务失败', error);
        }
      }
    },
    
    async refreshTodos() {
      await this.fetchTodos();
      await this.fetchCountdownTasks();
    },
    
    handleTransitionEnd(todoId) {
      // 找到任务并移除isCompleting标记
      const todoIndex = this.todos.findIndex(t => t.id === todoId);
      if (todoIndex !== -1 && this.todos[todoIndex].isCompleting) {
        const updatedTodo = { ...this.todos[todoIndex] };
        delete updatedTodo.isCompleting;
        
        // 防止过渡期间出现闪烁，等待下一帧更新
        requestAnimationFrame(() => {
          this.todos.splice(todoIndex, 1, updatedTodo);
        });
      }
    },
    
    // 动画开始前记录元素宽度
    beforeTaskLeave(el) {
      // 如果是取消操作，记录元素的当前宽度
      if (this.isCancelling) {
        const width = el.offsetWidth + 'px';
        el.style.width = width;
      }
    },
    
    // 设置任务元素的初始状态
    beforeTaskEnter(el) {
      // 设置初始状态，避免状态切换时的闪烁
      el.style.opacity = '0';
      el.style.transform = 'translateY(-20px)';
    },
    
    // 动画结束后清理
    afterTaskLeave(el) {
      // 彻底清理内联样式
      el.style.width = '';
      el.style.opacity = '';
      el.style.transform = '';
      el.style.visibility = '';
      
      // 强制重绘以消除任何残留视觉效果
      requestAnimationFrame(() => {
        document.body.offsetHeight; // 触发重排/重绘
      });
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

/* 倒计时任务区域样式 */
.countdown-tasks-section {
  margin-bottom: 32px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #2d3436;
  margin: 0;
}

.add-countdown-btn {
  background-color: #7e57c2;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 12px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: background-color 0.2s;
}

.add-countdown-btn:hover {
  background-color: #6a48b0;
}

.countdown-tasks-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

/* 常规任务列表样式 */
.todo-list {
  margin-top: 24px;
  padding-bottom: 32px;
  min-height: 100px; /* 确保有足够的空间可点击 */
  position: relative; /* 为绝对定位的元素提供参考 */
}

/* 临时新任务的动画样式 */
.new-task-enter-active {
  animation: slide-down 0.4s ease-out;
}

.new-task-leave-active {
  animation: slide-up 0.4s ease-in forwards; /* 添加forwards保持最终状态 */
  position: absolute;
  width: 100%;
  left: 0;
  right: 0;
  will-change: transform, opacity; /* 告知浏览器优化这些属性的变化 */
  z-index: 1; /* 确保动画元素在上层 */
}

/* 只有进入动画，没有离开动画的过渡效果 */
.new-task-no-leave-enter-active {
  animation: slide-down 0.4s ease-out;
}

/* 没有动画效果的离开过渡 */
.new-task-no-leave-leave-active {
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.01s, visibility 0.01s;
  position: absolute;
  width: 100%;
  left: 0;
  right: 0;
}

@keyframes slide-down {
  0% {
    transform: translateY(-20px);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes slide-up {
  0% {
    transform: translateY(0);
    opacity: 1;
    visibility: visible;
  }
  99% {
    transform: translateY(20px);
    opacity: 0;
    visibility: visible;
  }
  100% {
    transform: translateY(20px);
    opacity: 0;
    visibility: hidden; /* 确保元素真正不可见 */
  }
}

/* 任务列表动画 */
.todo-list-enter-active {
  transition: all 0.3s ease;
}

.todo-list-leave-active {
  transition: all 0.3s ease;
  position: absolute;
  width: 100%;
}

.todo-list-enter-from,
.todo-list-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* 完全无动画的过渡 */
.no-animation-enter-active,
.no-animation-leave-active {
  transition: none;
}

.no-animation-enter-from,
.no-animation-enter-to,
.no-animation-leave-from,
.no-animation-leave-to {
  opacity: 1;
}

/* 跳过动画的项目 */
.no-animation-item {
  transition: none !important;
}

/* 确保transition-group中跳过动画的项目不受动画影响 */
.todo-list-enter-active .no-animation-item,
.todo-list-leave-active .no-animation-item {
  transition: none !important;
  transform: none !important;
  opacity: 1 !important;
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
  
  /* 移动端下保持动画样式一致 */
  .new-task-leave-active,
  .new-task-no-leave-leave-active {
    width: 100%;
    left: 0;
    right: 0;
  }
  
  .countdown-tasks-list {
    grid-template-columns: 1fr;
  }
}
</style> 