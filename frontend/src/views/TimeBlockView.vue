<template>
  <div class="home">
    <div class="app-layout">
      <!-- 侧边栏 -->
      <Sidebar @filter-selected="handleFilterSelected" />
      
      <!-- 主内容区域 -->
      <div class="main-content">
        <div class="header">
          <h1>时间段任务</h1>
          <button class="btn-add-timeblock" @click="showForm = true">+ 添加时间段任务</button>
        </div>
        
        <div class="loading-error" v-if="loading || error">
          <div v-if="loading" class="loading">加载中...</div>
          <div v-if="error" class="error">{{ error }}</div>
        </div>
        
        <div class="timeblocks-container" v-else>
          <div v-if="timeBlocks.length === 0" class="empty-state">
            <div class="empty-icon">📅</div>
            <h3>没有时间段任务</h3>
            <p>点击上方"添加时间段任务"按钮创建您的第一个时间段任务</p>
          </div>
          
          <div v-else class="timeblocks-list">
            <div 
              v-for="block in timeBlocks" 
              :key="block.id" 
              class="timeblock-card"
            >
              <!-- 时间段卡片头部 -->
              <div class="timeblock-header">
                <h3>{{ formatDateRange(block.start_date, block.end_date) }}</h3>
                <div class="actions">
                  <button class="btn-icon" @click.stop="editTimeBlock(block)">
                    <span class="icon">✏️</span>
                  </button>
                  <button class="btn-icon" @click.stop="confirmDelete(block)">
                    <span class="icon">🗑️</span>
                  </button>
                </div>
              </div>
              
              <!-- 进度条 -->
              <div class="timeblock-progress">
                <div class="progress-bar">
                  <div 
                    class="progress-fill" 
                    :style="{ width: `${block.progress}%` }"
                  ></div>
                </div>
                <span class="progress-text">{{ block.progress }}% 完成</span>
              </div>
              
              <!-- 子任务列表 -->
              <div class="timeblock-subtasks-container">
                <div class="subtasks-header">
                  <h4>子任务</h4>
                  <button class="btn-add-subtask" @click="showAddSubTaskForm(block)">
                    <span class="icon">+</span> 添加子任务
                  </button>
                </div>
                
                <div v-if="(block.subtasks || []).length === 0" class="empty-subtasks">
                  <p>暂无子任务</p>
                </div>
                
                <div v-else class="subtasks-list">
                  <div 
                    v-for="subtask in block.subtasks" 
                    :key="subtask.id"
                    class="subtask-item"
                    :class="{ completed: subtask.completed }"
                  >
                    <div class="subtask-content">
                      <div class="checkbox-wrapper">
                        <input 
                          type="checkbox" 
                          :id="`subtask-${block.id}-${subtask.id}`"
                          :checked="subtask.completed" 
                          @change="toggleSubtaskComplete(block.id, subtask)"
                          class="custom-checkbox"
                        />
                        <label :for="`subtask-${block.id}-${subtask.id}`" class="checkbox-label"></label>
                      </div>
                      
                      <div class="subtask-info" @click="editSubTask(block.id, subtask)">
                        <div class="subtask-title">{{ subtask.title }}</div>
                        <div class="subtask-description" v-if="subtask.description">
                          {{ subtask.description }}
                        </div>
                      </div>
                    </div>
                    
                    <div class="subtask-actions">
                      <button class="btn-icon" @click="editSubTask(block.id, subtask)">
                        <span class="icon">✏️</span>
                      </button>
                      <button class="btn-icon" @click="confirmDeleteSubtask(block.id, subtask)">
                        <span class="icon">🗑️</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 时间段表单 -->
    <div class="modal" v-if="showForm">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ isEditing ? '编辑时间段' : '新建时间段' }}</h2>
          <button class="btn-close" @click="cancelForm">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveTimeBlock">
            <div class="form-row">
              <div class="form-group">
                <label for="start_date">开始日期</label>
                <input 
                  type="date" 
                  id="start_date" 
                  v-model="form.start_date" 
                  required
                />
              </div>
              
              <div class="form-group">
                <label for="end_date">结束日期</label>
                <input 
                  type="date" 
                  id="end_date" 
                  v-model="form.end_date" 
                  required
                />
              </div>
            </div>
            
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cancelForm">取消</button>
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
    
    <!-- 时间段删除确认对话框 -->
    <div class="modal" v-if="showDeleteConfirm">
      <div class="modal-content">
        <div class="modal-header">
          <h2>确认删除</h2>
          <button class="btn-close" @click="showDeleteConfirm = false">×</button>
        </div>
        <div class="modal-body">
          <p>确定要删除此时间段及其所有子任务吗？</p>
          <p>日期范围: {{ deleteTarget ? formatDateRange(deleteTarget.start_date, deleteTarget.end_date) : '' }}</p>
          <p class="warning">此操作不可撤销！</p>
          
          <div class="form-actions">
            <button class="btn-secondary" @click="showDeleteConfirm = false">取消</button>
            <button class="btn-danger" @click="deleteTimeBlock">删除</button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 子任务删除确认对话框 -->
    <div class="modal" v-if="showSubtaskDeleteConfirm">
      <div class="modal-content">
        <div class="modal-header">
          <h2>确认删除</h2>
          <button class="btn-close" @click="showSubtaskDeleteConfirm = false">×</button>
        </div>
        <div class="modal-body">
          <p>确定要删除子任务 "{{ deleteSubtaskTarget ? deleteSubtaskTarget.title : '' }}" 吗？</p>
          <p class="warning">此操作不可撤销！</p>
          
          <div class="form-actions">
            <button class="btn-secondary" @click="showSubtaskDeleteConfirm = false">取消</button>
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
import Sidebar from '@/components/Sidebar.vue';

export default {
  name: 'TimeBlockView',
  components: {
    Sidebar
  },
  data() {
    return {
      timeBlocks: [],
      loading: true,
      error: null,
      showForm: false,
      isEditing: false,
      form: {
        start_date: '',
        end_date: ''
      },
      showDeleteConfirm: false,
      deleteTarget: null,
      
      // 子任务相关
      showSubTaskForm: false,
      isEditingSubTask: false,
      currentTimeBlockId: null,
      currentSubTask: null,
      subTaskForm: {
        title: '',
        description: '',
        completed: false,
        order: 0
      },
      showSubtaskDeleteConfirm: false,
      deleteSubtaskTarget: null,
      deleteSubtaskTimeBlockId: null
    };
  },
  created() {
    this.fetchTimeBlocks();
  },
  methods: {
    formatDateRange,
    
    handleFilterSelected(data) {
      // 处理过滤器选择事件，根据选择的过滤器或分组进行路由导航
      if (data.type === 'filter') {
        if (data.id === 'today' || data.id === 'all' || data.id === 'completed') {
          this.$router.push('/');
        } else if (data.id === 'calendar') {
          this.$router.push('/calendar');
        }
      } else if (data.type === 'group') {
        // 导航到带有分组ID的主页面
        this.$router.push(`/?group=${data.id}`);
      }
    },
    
    async fetchTimeBlocks() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await timeBlockAPI.getAllTimeBlocks();
        if (response.success) {
          this.timeBlocks = response.data;
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
    
    editTimeBlock(timeBlock) {
      this.isEditing = true;
      this.form = {
        start_date: formatDateForInput(timeBlock.start_date),
        end_date: formatDateForInput(timeBlock.end_date)
      };
      this.currentTimeBlock = timeBlock;
      this.showForm = true;
    },
    
    confirmDelete(timeBlock) {
      this.deleteTarget = timeBlock;
      this.showDeleteConfirm = true;
    },
    
    async deleteTimeBlock() {
      if (!this.deleteTarget) return;
      
      try {
        const response = await timeBlockAPI.deleteTimeBlock(this.deleteTarget.id);
        if (response.success) {
          // 从列表中移除
          this.timeBlocks = this.timeBlocks.filter(block => block.id !== this.deleteTarget.id);
          this.showDeleteConfirm = false;
          this.deleteTarget = null;
        } else {
          this.error = response.error || '删除时间段失败';
        }
      } catch (error) {
        console.error('删除时间段出错:', error);
        this.error = '删除时间段时发生错误';
      }
    },
    
    resetForm() {
      this.form = {
        start_date: '',
        end_date: ''
      };
      this.isEditing = false;
      this.currentTimeBlock = null;
    },
    
    cancelForm() {
      this.showForm = false;
      this.resetForm();
    },
    
    async saveTimeBlock() {
      try {
        let response;
        
        if (this.isEditing && this.currentTimeBlock) {
          response = await timeBlockAPI.updateTimeBlock(this.currentTimeBlock.id, this.form);
        } else {
          response = await timeBlockAPI.createTimeBlock(this.form);
        }
        
        if (response.success) {
          // 重新获取列表以确保数据同步
          await this.fetchTimeBlocks();
          this.showForm = false;
          this.resetForm();
        } else {
          this.error = response.error || '保存时间段失败';
        }
      } catch (error) {
        console.error('保存时间段出错:', error);
        this.error = '保存时间段时发生错误';
      }
    },
    
    // 子任务相关方法
    showAddSubTaskForm(timeBlock) {
      this.isEditingSubTask = false;
      this.currentTimeBlockId = timeBlock.id;
      this.currentSubTask = null;
      this.subTaskForm = {
        title: '',
        description: '',
        completed: false,
        order: timeBlock.subtasks ? timeBlock.subtasks.length : 0
      };
      this.showSubTaskForm = true;
    },
    
    editSubTask(timeBlockId, subtask) {
      this.isEditingSubTask = true;
      this.currentTimeBlockId = timeBlockId;
      this.currentSubTask = subtask;
      this.subTaskForm = {
        title: subtask.title,
        description: subtask.description || '',
        completed: subtask.completed,
        order: subtask.order
      };
      this.showSubTaskForm = true;
    },
    
    cancelSubTaskForm() {
      this.showSubTaskForm = false;
      this.currentTimeBlockId = null;
      this.currentSubTask = null;
    },
    
    async saveSubTask() {
      if (!this.currentTimeBlockId) return;
      
      try {
        let response;
        
        if (this.isEditingSubTask && this.currentSubTask) {
          response = await timeBlockAPI.updateSubTask(
            this.currentTimeBlockId,
            this.currentSubTask.id,
            this.subTaskForm
          );
        } else {
          response = await timeBlockAPI.createSubTask(this.currentTimeBlockId, this.subTaskForm);
        }
        
        if (response.success) {
          // 重新获取列表以更新子任务
          await this.fetchTimeBlocks();
          this.showSubTaskForm = false;
          this.currentTimeBlockId = null;
          this.currentSubTask = null;
        } else {
          this.error = response.error || '保存子任务失败';
        }
      } catch (error) {
        console.error('保存子任务出错:', error);
        this.error = '保存子任务时发生错误';
      }
    },
    
    async toggleSubtaskComplete(timeBlockId, subtask) {
      try {
        const updatedData = {
          completed: !subtask.completed
        };
        
        const response = await timeBlockAPI.updateSubTask(
          timeBlockId,
          subtask.id,
          updatedData
        );
        
        if (response.success) {
          // 更新本地状态
          subtask.completed = !subtask.completed;
          
          // 找到对应的时间段
          const timeBlock = this.timeBlocks.find(block => block.id === timeBlockId);
          if (timeBlock) {
            // 重新计算进度
            const completed = timeBlock.subtasks.filter(task => task.completed).length;
            timeBlock.progress = Math.round((completed / timeBlock.subtasks.length) * 100);
          }
        } else {
          this.error = response.error || '更新子任务状态失败';
        }
      } catch (error) {
        console.error('更新子任务状态出错:', error);
        this.error = '更新子任务状态时发生错误';
      }
    },
    
    confirmDeleteSubtask(timeBlockId, subtask) {
      this.deleteSubtaskTarget = subtask;
      this.deleteSubtaskTimeBlockId = timeBlockId;
      this.showSubtaskDeleteConfirm = true;
    },
    
    async deleteSubTask() {
      if (!this.deleteSubtaskTarget || !this.deleteSubtaskTimeBlockId) return;
      
      try {
        const response = await timeBlockAPI.deleteSubTask(
          this.deleteSubtaskTimeBlockId, 
          this.deleteSubtaskTarget.id
        );
        
        if (response.success) {
          // 重新获取列表以更新子任务
          await this.fetchTimeBlocks();
          this.showSubtaskDeleteConfirm = false;
          this.deleteSubtaskTarget = null;
          this.deleteSubtaskTimeBlockId = null;
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

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
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

.btn-add-timeblock {
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 6px;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: all 0.2s ease;
}

.btn-add-timeblock:hover {
  /* 移除悬浮动画效果 */
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

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: #7f8c8d;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 10px;
}

.timeblocks-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.timeblock-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 16px;
  transition: box-shadow 0.2s;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

.timeblock-card:hover {
  /* 移除悬浮动画效果 */
}

.timeblock-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.timeblock-header h3 {
  margin: 0;
  font-size: 18px;
}

.actions {
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
  /* 移除悬浮动画效果 */
}

.timeblock-progress {
  margin: 15px 0;
}

.progress-bar {
  height: 6px;
  background-color: #ecf0f1;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 5px;
}

.progress-fill {
  height: 100%;
  background-color: #3498db;
  border-radius: 3px;
}

.progress-text {
  font-size: 12px;
  color: #7f8c8d;
}

.timeblock-subtasks-container {
  margin-top: 15px;
  border-top: 1px solid #ecf0f1;
  padding-top: 10px;
}

.subtasks-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.subtasks-header h4 {
  margin: 0;
  font-size: 16px;
  color: #555;
}

.btn-add-subtask {
  background: none;
  border: none;
  color: #3498db;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
}

.btn-add-subtask:hover {
  /* 移除悬浮动画效果 */
}

.empty-subtasks {
  padding: 10px;
  color: #7f8c8d;
  text-align: center;
  font-style: italic;
  font-size: 14px;
}

.subtasks-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 250px;
  overflow-y: auto;
}

.subtask-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f9f9f9;
  border-radius: 6px;
  padding: 10px 12px;
  transition: background-color 0.2s;
}

.subtask-item.completed {
  background-color: #f0f0f0;
}

.subtask-content {
  display: flex;
  align-items: flex-start;
  gap: 10px;
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
  font-size: 14px;
  margin-bottom: 2px;
}

.subtask-item.completed .subtask-title {
  text-decoration: line-through;
  color: #7f8c8d;
}

.subtask-description {
  font-size: 12px;
  color: #7f8c8d;
}

.subtask-actions {
  display: flex;
  gap: 5px;
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
  font-size: 14px;
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