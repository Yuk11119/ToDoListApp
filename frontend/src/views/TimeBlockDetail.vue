<template>
  <div class="timeblock-detail">
    <div class="loading-error" v-if="loading || error">
      <div v-if="loading" class="loading">加载中...</div>
      <div v-if="error" class="error">{{ error }}</div>
    </div>
    
    <template v-else>
      <!-- 返回按钮 -->
      <div class="back-button" @click="goBack">
        <span class="icon">←</span> 返回时间段列表
      </div>
      
      <!-- 时间段信息 -->
      <div class="timeblock-header">
        <div class="timeblock-title">
          <h1>{{ formatDateRange(timeBlock.start_date, timeBlock.end_date) }}</h1>
          <button class="btn-icon" @click="editTimeBlock">
            <span class="icon">✏️</span>
          </button>
        </div>
        
        <div class="timeblock-meta">
          <div class="timeblock-progress">
            <div class="progress-bar">
              <div 
                class="progress-fill" 
                :style="{ width: `${timeBlock.progress}%` }"
              ></div>
            </div>
            <span class="progress-text">{{ timeBlock.progress }}% 完成</span>
          </div>
        </div>
      </div>
      
      <!-- 子任务列表 -->
      <div class="subtasks-section">
        <div class="subtasks-header">
          <h2>子任务列表</h2>
          <button class="btn-primary" @click="showSubTaskForm = true">
            <span class="icon">+</span> 添加子任务
          </button>
        </div>
        
        <div v-if="(timeBlock.subtasks || []).length === 0" class="empty-state">
          <div class="empty-icon">📋</div>
          <h3>没有子任务</h3>
          <p>点击"添加子任务"按钮创建您的第一个子任务</p>
        </div>
        
        <div v-else class="subtasks-list">
          <div 
            v-for="subtask in timeBlock.subtasks" 
            :key="subtask.id"
            class="subtask-item"
            :class="{ completed: subtask.completed }"
          >
            <div class="subtask-content">
              <div class="checkbox-wrapper">
                <input 
                  type="checkbox" 
                  :id="`subtask-${subtask.id}`"
                  :checked="subtask.completed" 
                  @change="toggleSubtaskComplete(subtask)"
                  class="custom-checkbox"
                />
                <label :for="`subtask-${subtask.id}`" class="checkbox-label"></label>
              </div>
              
              <div class="subtask-info" @click="editSubTask(subtask)">
                <div class="subtask-title">{{ subtask.title }}</div>
                <div class="subtask-description" v-if="subtask.description">
                  {{ subtask.description }}
                </div>
              </div>
            </div>
            
            <div class="subtask-actions">
              <button class="btn-icon" @click="editSubTask(subtask)">
                <span class="icon">✏️</span>
              </button>
              <button class="btn-icon" @click="confirmDeleteSubtask(subtask)">
                <span class="icon">🗑️</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </template>
    
    <!-- 时间段编辑表单 -->
    <div class="modal" v-if="showTimeBlockForm">
      <div class="modal-content">
        <div class="modal-header">
          <h2>编辑时间段</h2>
          <button class="btn-close" @click="showTimeBlockForm = false">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveTimeBlock">
            <div class="form-row">
              <div class="form-group">
                <label for="start_date">开始日期</label>
                <input 
                  type="date" 
                  id="start_date" 
                  v-model="timeBlockForm.start_date" 
                  required
                />
              </div>
              
              <div class="form-group">
                <label for="end_date">结束日期</label>
                <input 
                  type="date" 
                  id="end_date" 
                  v-model="timeBlockForm.end_date" 
                  required
                />
              </div>
            </div>
            
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="showTimeBlockForm = false">取消</button>
              <button type="submit" class="btn-primary">保存</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    
    <!-- 子任务表单 -->
    <div class="modal" v-if="showSubTaskForm">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ isEditingSubTask ? '编辑子任务' : '添加子任务' }}</h2>
          <button class="btn-close" @click="cancelSubTaskForm">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveSubTask">
            <div class="form-group">
              <label for="subtask-title">标题</label>
              <input 
                type="text" 
                id="subtask-title" 
                v-model="subTaskForm.title" 
                required 
                placeholder="输入子任务标题"
              />
            </div>
            
            <div class="form-group">
              <label for="subtask-description">描述</label>
              <textarea 
                id="subtask-description" 
                v-model="subTaskForm.description" 
                placeholder="输入子任务描述（可选）"
              ></textarea>
            </div>
            
            <div class="form-group" v-if="isEditingSubTask">
              <div class="checkbox-inline">
                <input 
                  type="checkbox" 
                  id="subtask-completed" 
                  v-model="subTaskForm.completed"
                />
                <label for="subtask-completed">标记为已完成</label>
              </div>
            </div>
            
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cancelSubTaskForm">取消</button>
              <button type="submit" class="btn-primary">保存</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    
    <!-- 删除确认对话框 -->
    <div class="modal" v-if="showDeleteConfirm">
      <div class="modal-content">
        <div class="modal-header">
          <h2>确认删除</h2>
          <button class="btn-close" @click="showDeleteConfirm = false">×</button>
        </div>
        <div class="modal-body">
          <p>确定要删除子任务 "{{ deleteTarget ? deleteTarget.title : '' }}" 吗？</p>
          <p class="warning">此操作不可撤销！</p>
          
          <div class="form-actions">
            <button class="btn-secondary" @click="showDeleteConfirm = false">取消</button>
            <button class="btn-danger" @click="deleteSubTask">删除</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { timeBlockAPI } from '@/api';
import { formatDateRange, formatDateForInput } from '@/utils/dateUtils';

export default {
  name: 'TimeBlockDetail',
  props: {
    id: {
      type: [Number, String],
      required: true
    }
  },
  data() {
    return {
      timeBlock: {},
      loading: true,
      error: null,
      showTimeBlockForm: false,
      showSubTaskForm: false,
      isEditingSubTask: false,
      timeBlockForm: {
        start_date: '',
        end_date: ''
      },
      subTaskForm: {
        title: '',
        description: '',
        completed: false,
        order: 0
      },
      currentSubTask: null,
      showDeleteConfirm: false,
      deleteTarget: null
    };
  },
  created() {
    this.fetchTimeBlock();
  },
  methods: {
    formatDateRange,
    
    async fetchTimeBlock() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await timeBlockAPI.getTimeBlock(this.id);
        if (response.success) {
          this.timeBlock = response.data;
        } else {
          this.error = response.error || '获取时间段任务失败';
        }
      } catch (error) {
        console.error('获取时间段任务出错:', error);
        this.error = '获取时间段任务时发生错误';
      } finally {
        this.loading = false;
      }
    },
    
    goBack() {
      this.$router.push('/timeblocks');
    },
    
    editTimeBlock() {
      this.timeBlockForm = {
        start_date: formatDateForInput(this.timeBlock.start_date),
        end_date: formatDateForInput(this.timeBlock.end_date)
      };
      this.showTimeBlockForm = true;
    },
    
    async saveTimeBlock() {
      try {
        const response = await timeBlockAPI.updateTimeBlock(this.id, this.timeBlockForm);
        
        if (response.success) {
          // 重新获取时间段以更新数据
          await this.fetchTimeBlock();
          this.showTimeBlockForm = false;
        } else {
          this.error = response.error || '更新时间段失败';
        }
      } catch (error) {
        console.error('更新时间段出错:', error);
        this.error = '更新时间段时发生错误';
      }
    },
    
    resetSubTaskForm() {
      this.subTaskForm = {
        title: '',
        description: '',
        completed: false,
        order: this.timeBlock.subtasks ? this.timeBlock.subtasks.length : 0
      };
      this.isEditingSubTask = false;
      this.currentSubTask = null;
    },
    
    cancelSubTaskForm() {
      this.showSubTaskForm = false;
      this.resetSubTaskForm();
    },
    
    editSubTask(subtask) {
      this.isEditingSubTask = true;
      this.currentSubTask = subtask;
      this.subTaskForm = {
        title: subtask.title,
        description: subtask.description || '',
        completed: subtask.completed,
        order: subtask.order
      };
      this.showSubTaskForm = true;
    },
    
    async saveSubTask() {
      try {
        let response;
        
        if (this.isEditingSubTask && this.currentSubTask) {
          response = await timeBlockAPI.updateSubTask(
            this.id,
            this.currentSubTask.id,
            this.subTaskForm
          );
        } else {
          response = await timeBlockAPI.createSubTask(this.id, this.subTaskForm);
        }
        
        if (response.success) {
          // 重新获取时间段以更新子任务列表
          await this.fetchTimeBlock();
          this.showSubTaskForm = false;
          this.resetSubTaskForm();
        } else {
          this.error = response.error || '保存子任务失败';
        }
      } catch (error) {
        console.error('保存子任务出错:', error);
        this.error = '保存子任务时发生错误';
      }
    },
    
    async toggleSubtaskComplete(subtask) {
      try {
        const updatedData = {
          completed: !subtask.completed
        };
        
        const response = await timeBlockAPI.updateSubTask(
          this.id,
          subtask.id,
          updatedData
        );
        
        if (response.success) {
          // 更新本地状态
          subtask.completed = !subtask.completed;
          
          // 重新计算进度
          const completed = this.timeBlock.subtasks.filter(task => task.completed).length;
          this.timeBlock.progress = Math.round((completed / this.timeBlock.subtasks.length) * 100);
        } else {
          this.error = response.error || '更新子任务状态失败';
        }
      } catch (error) {
        console.error('更新子任务状态出错:', error);
        this.error = '更新子任务状态时发生错误';
      }
    },
    
    confirmDeleteSubtask(subtask) {
      this.deleteTarget = subtask;
      this.showDeleteConfirm = true;
    },
    
    async deleteSubTask() {
      if (!this.deleteTarget) return;
      
      try {
        const response = await timeBlockAPI.deleteSubTask(this.id, this.deleteTarget.id);
        
        if (response.success) {
          // 重新获取时间段以更新子任务列表
          await this.fetchTimeBlock();
          this.showDeleteConfirm = false;
          this.deleteTarget = null;
        } else {
          this.error = response.error || '删除子任务失败';
        }
      } catch (error) {
        console.error('删除子任务出错:', error);
        this.error = '删除子任务时发生错误';
      }
    }
  }
};
</script>

<style scoped>
.timeblock-detail {
  padding: 20px;
  height: 100%;
  overflow-y: auto;
}

.loading-error {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.loading {
  color: #3498db;
  font-size: 18px;
}

.error {
  color: #e74c3c;
  font-size: 16px;
}

.back-button {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: #3498db;
  cursor: pointer;
  margin-bottom: 20px;
  font-size: 16px;
}

.back-button:hover {
  text-decoration: underline;
}

.timeblock-header {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.timeblock-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.timeblock-title h1 {
  margin: 0;
  font-size: 24px;
}

.timeblock-meta {
  margin-bottom: 15px;
}

.timeblock-progress {
  margin-bottom: 10px;
}

.progress-bar {
  height: 8px;
  background-color: #ecf0f1;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 5px;
}

.progress-fill {
  height: 100%;
  background-color: #3498db;
  border-radius: 4px;
}

.progress-text {
  font-size: 14px;
  color: #7f8c8d;
}

.subtasks-section {
  margin-top: 30px;
}

.subtasks-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.subtasks-header h2 {
  margin: 0;
  font-size: 20px;
}

.btn-primary {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #7f8c8d;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 10px;
}

.subtasks-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.subtask-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  padding: 12px 16px;
  transition: background-color 0.2s;
}

.subtask-item.completed {
  background-color: #f9f9f9;
}

.subtask-content {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  flex: 1;
}

.checkbox-wrapper {
  position: relative;
  margin-top: 2px;
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
  width: 20px;
  height: 20px;
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
  width: 5px;
  height: 9px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: translate(-50%, -50%) rotate(45deg);
}

.subtask-info {
  flex: 1;
  cursor: pointer;
}

.subtask-title {
  font-size: 16px;
  margin-bottom: 4px;
}

.subtask-item.completed .subtask-title {
  text-decoration: line-through;
  color: #7f8c8d;
}

.subtask-description {
  font-size: 14px;
  color: #7f8c8d;
}

.subtask-actions {
  display: flex;
  gap: 5px;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  padding: 4px;
  border-radius: 4px;
}

.btn-icon:hover {
  background-color: #f1f1f1;
}

/* 模态框样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #e1e1e1;
}

.modal-header h2 {
  margin: 0;
  font-size: 20px;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #7f8c8d;
}

.modal-body {
  padding: 16px;
}

.form-group {
  margin-bottom: 16px;
}

.form-row {
  display: flex;
  gap: 16px;
}

.form-row .form-group {
  flex: 1;
}

.checkbox-inline {
  display: flex;
  align-items: center;
  gap: 8px;
}

.checkbox-inline input[type="checkbox"] {
  width: auto;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

input, textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

textarea {
  min-height: 80px;
  resize: vertical;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.btn-secondary {
  background-color: #ecf0f1;
  color: #333;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-secondary:hover {
  background-color: #dfe4ea;
}

.btn-danger {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-danger:hover {
  background-color: #c0392b;
}

.warning {
  color: #e74c3c;
  font-weight: bold;
}
</style> 