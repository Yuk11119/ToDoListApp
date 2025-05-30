<template>
  <div class="todo-item" 
       :class="{ completed: todo.completed }"
       :style="getItemStyle()"
  >
    <div class="group-indicator" v-if="todo.group_color" :style="{ backgroundColor: todo.group_color }"></div>
    <div class="todo-content">
      <div class="checkbox-wrapper">
      <input 
        type="checkbox" 
          :id="`todo-${todo.id}`"
        :checked="todo.completed" 
        @change="toggleComplete"
          class="custom-checkbox"
      />
        <label :for="`todo-${todo.id}`" class="checkbox-label"></label>
      </div>
      
      <div class="todo-info">
        <!-- 标题 - 双击可编辑 -->
        <div v-if="editingTitle" class="edit-title-container">
          <input 
            type="text" 
            v-model="editedTitle" 
            class="edit-title-input"
            ref="titleInput"
            @keyup.enter="saveTitle"
            @keyup.esc="cancelEditTitle"
            @blur="saveTitle"
          />
        </div>
        <span 
          v-else 
          class="todo-title" 
          @dblclick="startEditTitle"
          :title="'双击编辑标题'"
        >{{ todo.title }}</span>
        
        <div class="todo-details">
          <!-- 移除分组文字，改用阴影颜色 -->
          
          <!-- 截止日期 - 双击可编辑 -->
          <div v-if="editingDeadline" class="edit-deadline-container">
            <input 
              type="datetime-local" 
              v-model="editedDeadline" 
              class="edit-deadline-input"
              ref="deadlineInput"
              @change="saveDeadline"
              @blur="saveDeadline"
              @keyup.esc="cancelEditDeadline"
            />
          </div>
          <span 
            v-else-if="todo.deadline" 
            class="todo-deadline" 
            :class="{ overdue: isOverdue }"
            @dblclick="startEditDeadline"
            :title="'双击编辑截止日期'"
          >
            <i class="deadline-icon">⏰</i>
            {{ formatDeadline(todo.deadline) }}
          </span>
        </div>
      </div>
    </div>
    <div class="todo-actions">
      <button class="action-btn edit-btn" @click="$emit('edit', todo.id)" title="编辑任务">
        <span>✏️</span>
      </button>
      <button class="action-btn delete-btn" @click="$emit('delete', todo.id)" title="删除任务">
        <span>🗑️</span>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TodoItem',
  props: {
    todo: {
      type: Object,
      required: true
    },
    isNew: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      editingTitle: false,
      editedTitle: '',
      editingDeadline: false,
      editedDeadline: '',
      isSaving: false
    }
  },
  computed: {
    // 判断任务是否已过期
    isOverdue() {
      if (!this.todo.deadline) return false;
      
      const deadline = new Date(this.todo.deadline);
      const now = new Date();
      
      return !this.todo.completed && deadline < now;
    }
  },
  mounted() {
    // 如果是新任务，自动进入编辑模式
    if (this.isNew) {
      this.startEditTitle();
    }
  },
  methods: {
    // 获取带透明度的颜色
    getColorWithOpacity(color, opacity) {
      if (!color) return `rgba(0, 0, 0, ${opacity})`;
      
      // 如果是十六进制颜色
      if (color.startsWith('#')) {
        let r = parseInt(color.slice(1, 3), 16);
        let g = parseInt(color.slice(3, 5), 16);
        let b = parseInt(color.slice(5, 7), 16);
        return `rgba(${r}, ${g}, ${b}, ${opacity})`;
      }
      
      // 如果是rgb颜色
      if (color.startsWith('rgb')) {
        return color.replace('rgb', 'rgba').replace(')', `, ${opacity})`);
      }
      
      // 如果是rgba颜色
      if (color.startsWith('rgba')) {
        return color.replace(/[\d\.]+\)$/, `${opacity})`);
      }
      
      // 其他情况返回默认阴影
      return `rgba(0, 0, 0, ${opacity})`;
    },
    
    // 获取项目样式
    getItemStyle() {
      if (!this.todo.group_color) return {};
      
      // 获取分组颜色，已完成状态降低颜色饱和度
      const opacity = this.todo.completed ? 0.08 : 0.15;
      
      return {
        boxShadow: `0 4px 12px ${this.getColorWithOpacity(this.todo.group_color, opacity)}`,
        borderLeft: `3px solid ${this.todo.group_color}`
      };
    },
    
    // 切换完成状态
    toggleComplete() {
      const updatedTodo = {
        ...this.todo,
        completed: !this.todo.completed
      };
      this.$emit('toggle', updatedTodo);
    },
    
    // 标题编辑相关方法
    startEditTitle() {
      if (this.todo.completed && !this.isNew) return; // 已完成的任务不允许编辑，但新任务例外
      
      this.editedTitle = this.todo.title;
      this.editingTitle = true;
      this.$nextTick(() => {
        if (this.$refs.titleInput) {
          this.$refs.titleInput.focus();
        }
      });
    },
    
    saveTitle(event) {
      // 防止重复提交
      if (this.isSaving) return;
      
      // 如果是新任务且标题为空，则不保存
      if (this.isNew && (!this.editedTitle || this.editedTitle.trim() === '')) {
        // 对于新任务，保留编辑状态
        return;
      }
      
      if (this.editedTitle.trim() === '') {
        this.editedTitle = this.todo.title; // 如果为空，恢复原标题
      }
      
      if (this.editedTitle !== this.todo.title) {
        this.isSaving = true; // 设置保存状态为true
        
        const updatedTodo = {
          ...this.todo,
          title: this.editedTitle
        };
        this.$emit('toggle', updatedTodo);
        
        // 延迟重置保存状态，防止快速重复提交
        setTimeout(() => {
          this.isSaving = false;
        }, 300);
      }
      
      // 检查是否是按下回车键触发的保存
      const isEnterKey = event && event.type === 'keyup' && event.key === 'Enter';
      
      // 如果是新任务且按了回车键，则结束编辑
      if (this.isNew && isEnterKey) {
        this.editingTitle = false;
      } else if (!this.isNew) {
        // 非新任务正常结束编辑
        this.editingTitle = false;
      }
    },
    
    cancelEditTitle() {
      if (this.isNew) {
        // 如果是新任务，取消编辑意味着取消创建
        this.$emit('delete', this.todo.id);
      } else {
        this.editingTitle = false;
      }
    },
    
    // 截止日期编辑相关方法
    startEditDeadline() {
      if (this.todo.completed) return; // 已完成的任务不允许编辑
      
      this.editedDeadline = this.formatDateForInput(this.todo.deadline);
      this.editingDeadline = true;
      this.$nextTick(() => {
        this.$refs.deadlineInput.focus();
      });
    },
    
    saveDeadline() {
      let newDeadline = null;
      
      if (this.editedDeadline) {
        try {
          newDeadline = new Date(this.editedDeadline).toISOString();
        } catch (error) {
          console.error('日期转换错误', error);
          this.editingDeadline = false;
          return;
        }
      }
      
      if (newDeadline !== this.todo.deadline) {
        const updatedTodo = {
          ...this.todo,
          deadline: newDeadline
        };
        this.$emit('toggle', updatedTodo);
      }
      
      this.editingDeadline = false;
    },
    
    cancelEditDeadline() {
      this.editingDeadline = false;
    },
    
    // 日期格式化方法
    formatDateForInput(dateString) {
      if (!dateString) return '';
      
      try {
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return '';
        
        // 格式化为YYYY-MM-DDThh:mm
        return new Date(date.getTime() - (date.getTimezoneOffset() * 60000))
          .toISOString()
          .slice(0, 16);
      } catch (error) {
        console.error('日期格式化错误', error);
        return '';
      }
    },
    
    formatDeadline(dateString) {
      if (!dateString) return '';
      
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return '无效日期';
      
      const now = new Date();
      const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      const tomorrowStart = new Date(todayStart);
      tomorrowStart.setDate(tomorrowStart.getDate() + 1);
      
      // 如果是今天
      if (date >= todayStart && date < tomorrowStart) {
        return `今天 ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
      }
      
      // 如果是明天
      const nextDayStart = new Date(tomorrowStart);
      nextDayStart.setDate(nextDayStart.getDate() + 1);
      if (date >= tomorrowStart && date < nextDayStart) {
        return `明天 ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
      }
      
      // 如果是今年内的其他日期
      if (date.getFullYear() === now.getFullYear()) {
        return `${date.getMonth() + 1}月${date.getDate()}日 ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
      }
      
      // 其他年份
      return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`;
    }
  }
}
</script>

<style scoped>
.todo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px 16px 24px;
  background-color: white;
  border-radius: 12px;
  margin-bottom: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  border: 1px solid #f0f0f0;
  position: relative;
  overflow: hidden;
}

.group-indicator {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  border-top-left-radius: 12px;
  border-bottom-left-radius: 12px;
}

.todo-item:hover {
  transform: translateY(-2px);
}

.todo-content {
  display: flex;
  align-items: center;
  flex: 1;
}

/* 自定义复选框 */
.checkbox-wrapper {
  position: relative;
  margin-right: 16px;
}

.custom-checkbox {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkbox-label {
  position: relative;
  display: inline-block;
  width: 24px;
  height: 24px;
  background-color: #f8f9fa;
  border: 2px solid #dfe4ea;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s ease;
}

.custom-checkbox:checked + .checkbox-label {
  background-color: #4cd137;
  border-color: #4cd137;
}

.custom-checkbox:checked + .checkbox-label:after {
  content: '';
  position: absolute;
  left: 50%;
  top: 45%;
  width: 6px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: translate(-50%, -50%) rotate(45deg);
}

.todo-info {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0; /* 防止内容溢出 */
}

.todo-title {
  font-size: 16px;
  font-weight: 500;
  color: #2d3436;
  margin-bottom: 6px;
  transition: all 0.2s ease;
  cursor: pointer;
  padding: 3px 6px;
  border-radius: 4px;
  margin: -3px -6px 6px -6px;
}

.todo-title:hover {
  background-color: rgba(116, 185, 255, 0.1);
}

/* 标题编辑 */
.edit-title-container {
  margin-bottom: 6px;
  width: 100%;
}

.edit-title-input {
  width: 100%;
  padding: 6px 10px;
  font-size: 16px;
  border: 1px solid #74b9ff;
  border-radius: 4px;
  outline: none;
  background-color: white;
  box-shadow: 0 0 0 3px rgba(116, 185, 255, 0.2);
}

.todo-details {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
}

.todo-deadline {
  display: inline-flex;
  align-items: center;
  font-size: 13px;
  color: #27ae60;
  padding: 3px 8px;
  background-color: rgba(39, 174, 96, 0.1);
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.todo-deadline:hover {
  background-color: rgba(39, 174, 96, 0.2);
}

/* 截止日期编辑 */
.edit-deadline-container {
  margin: 0;
}

.edit-deadline-input {
  padding: 4px 8px;
  font-size: 13px;
  border: 1px solid #74b9ff;
  border-radius: 4px;
  outline: none;
  background-color: white;
  box-shadow: 0 0 0 3px rgba(116, 185, 255, 0.2);
}

.deadline-icon {
  font-style: normal;
  margin-right: 4px;
  font-size: 12px;
}

.todo-deadline.overdue {
  color: #e74c3c;
  background-color: rgba(231, 76, 60, 0.1);
}

/* 完成状态样式 */
.completed .todo-title {
  text-decoration: line-through;
  color: #b2bec3;
  cursor: default;
}

.completed .todo-title:hover {
  background-color: transparent;
}

.completed .todo-deadline {
  color: #b2bec3;
  background-color: rgba(178, 190, 195, 0.1);
  text-decoration: line-through;
  cursor: default;
}

.completed .todo-deadline:hover {
  background-color: rgba(178, 190, 195, 0.1);
}

.completed .checkbox-label {
  background-color: #b2bec3;
  border-color: #b2bec3;
}

.completed .todo-group {
  opacity: 0.7;
  border-color: #b2bec3 !important;
  color: #b2bec3;
  text-decoration: line-through;
}

.completed .group-color-dot {
  opacity: 0.5;
}

.todo-actions {
  display: flex;
  gap: 8px;
  margin-left: 16px;
}

.action-btn {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 50%;
  background-color: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 16px;
}

.action-btn:hover {
  background-color: #f1f2f6;
  transform: scale(1.1);
}

.edit-btn:hover {
  color: #f39c12;
}

.delete-btn:hover {
  color: #e74c3c;
}

@media (max-width: 640px) {
  .todo-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .todo-actions {
    margin-left: 0;
    margin-top: 16px;
    align-self: flex-end;
  }
  
  .todo-details {
    flex-wrap: wrap;
    margin-top: 6px;
  }
  
  .todo-group {
    margin-bottom: 6px;
  }
}

/* 完成状态下的阴影颜色降低 */
.completed {
  opacity: 0.85;
}

.completed .group-indicator {
  opacity: 0.5;
}
</style> 