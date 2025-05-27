<template>
  <div class="modal-backdrop" @click.self="$emit('cancel')">
  <div class="todo-form">
      <div class="form-header">
    <h2>{{ isEdit ? '编辑任务' : '添加新任务' }}</h2>
        <button type="button" class="close-btn" @click="$emit('cancel')">&times;</button>
      </div>
      
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="title">标题</label>
        <input 
          type="text" 
          id="title" 
          v-model="form.title" 
          required 
          placeholder="请输入任务标题"
            autofocus
        />
      </div>
      
      <div class="form-group">
        <label for="description">描述</label>
        <textarea 
          id="description" 
          v-model="form.description" 
          rows="3" 
          placeholder="请输入任务描述（可选）"
        ></textarea>
      </div>
      
        <!-- 分组选项 -->
        <div class="toggle-section">
          <div class="toggle-header">
            <span>添加分组</span>
            <div class="toggle-switch">
              <input type="checkbox" id="group-toggle" v-model="showGroup" />
              <label for="group-toggle"></label>
            </div>
          </div>
          
          <div class="toggle-content" v-if="showGroup">
      <div class="form-group">
              <label for="group">选择分组</label>
        <select id="group" v-model="form.group_id">
          <option :value="null">未分组</option>
          <option v-for="group in groups" :key="group.id" :value="group.id">
            {{ group.name }}
          </option>
        </select>
            </div>
          </div>
        </div>
        
        <!-- 截止日期选项 -->
        <div class="toggle-section">
          <div class="toggle-header">
            <span>添加截止日期</span>
            <div class="toggle-switch">
              <input type="checkbox" id="deadline-toggle" v-model="showDeadline" />
              <label for="deadline-toggle"></label>
            </div>
      </div>
      
          <div class="toggle-content" v-if="showDeadline">
            <div class="deadline-selection">
              <!-- 日期选择 -->
              <div class="deadline-date-selection">
                <label>选择日期</label>
        <input 
                  type="date" 
                  v-model="deadlineDate"
                  @change="updateDeadline"
        />
      </div>
      
              <!-- 时间选择 -->
              <div class="deadline-time-selection">
                <label>选择时间</label>
                <div class="time-inputs">
                  <select v-model.number="deadlineHour" @change="updateDeadline">
                    <option v-for="hour in 24" :key="`hour-${hour-1}`" :value="hour-1">
                      {{ (hour-1).toString().padStart(2, '0') }}
                    </option>
                  </select>
                  <span>:</span>
                  <select v-model.number="deadlineMinute" @change="updateDeadline">
                    <option v-for="minute in [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]" :key="`minute-${minute}`" :value="minute">
                      {{ minute.toString().padStart(2, '0') }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
          </div>
      </div>
      
      <div class="form-actions">
          <button type="button" class="submit-btn" @click="submitForm">{{ isEdit ? '保存' : '添加' }}</button>
          <button type="button" class="cancel-btn" @click="$emit('cancel')">取消</button>
      </div>
    </form>
    </div>
  </div>
</template>

<script>
import todoApi from '@/api/todo';

export default {
  name: 'TodoForm',
  props: {
    todo: {
      type: Object,
      default: () => ({
        title: '',
        description: '',
        completed: false,
        group_id: null,
        deadline: null
      })
    },
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  data() {
    // 解析截止日期到年、月、日、时、分
    const deadlineInfo = this.parseDeadline(this.todo.deadline);
    
    return {
      form: {
        title: this.todo.title,
        description: this.todo.description || '',
        group_id: this.todo.group_id || null,
      },
      groups: [],
      showGroup: false,
      showDeadline: false,
      deadlineDate: deadlineInfo.date,
      deadlineHour: deadlineInfo.hour,
      deadlineMinute: deadlineInfo.minute
    }
  },
  created() {
    this.loadGroups();
    // 如果编辑的任务已有分组，则自动展开分组选项
    if (this.isEdit && this.todo.group_id) {
      this.showGroup = true;
    }
    // 如果编辑的任务已有截止日期，则自动展开截止日期选项
    if (this.isEdit && this.todo.deadline) {
      this.showDeadline = true;
    }
    // 当组件创建时，阻止背景滚动
    document.body.style.overflow = 'hidden';
  },
  destroyed() {
    // 当组件销毁时，恢复背景滚动
    document.body.style.overflow = '';
  },
  watch: {
    todo(newTodo) {
      this.form = {
        title: newTodo.title,
        description: newTodo.description || '',
        group_id: newTodo.group_id || null,
      }
      
      // 解析新的截止日期
      const deadlineInfo = this.parseDeadline(newTodo.deadline);
      this.deadlineDate = deadlineInfo.date;
      this.deadlineHour = parseInt(deadlineInfo.hour);
      this.deadlineMinute = parseInt(deadlineInfo.minute);
      
      console.log('加载任务截止日期:', newTodo.deadline, {
        date: this.deadlineDate,
        hour: this.deadlineHour,
        minute: this.deadlineMinute
      });
      
      // 如果编辑的任务已有分组，则自动展开分组选项
      if (newTodo.group_id) {
        this.showGroup = true;
      }
      // 如果编辑的任务已有截止日期，则自动展开截止日期选项
      if (newTodo.deadline) {
        this.showDeadline = true;
      }
    }
  },
  methods: {
    async loadGroups() {
      try {
        const response = await todoApi.getAllGroups();
        if (response.success) {
          this.groups = response.data;
        } else {
          console.error('加载分组失败:', response.error);
        }
      } catch (error) {
        console.error('加载分组出错:', error);
      }
    },
    
    // 解析日期时间字符串为各个组件
    parseDeadline(deadlineStr) {
      if (!deadlineStr) {
        // 默认设置为当前时间的下一个整点，向上取整到5分钟间隔
        const now = new Date();
        const minute = Math.ceil(now.getMinutes() / 5) * 5;
        now.setMinutes(minute >= 60 ? 55 : minute, 0, 0); // 设置为5分钟间隔
        
        return {
          date: now.toISOString().split('T')[0],
          hour: parseInt(now.getHours()),
          minute: parseInt(now.getMinutes())
        };
      }
      
      try {
        // 解析ISO日期字符串为本地时间
        const date = new Date(deadlineStr);
        if (isNaN(date.getTime())) {
          throw new Error('Invalid date');
        }
        
        // 处理为本地时间，不需要时区调整，因为new Date()自动将ISO字符串转换为本地时区
        // 将分钟四舍五入到最接近的5分钟间隔
        const localMinute = Math.round(date.getMinutes() / 5) * 5;
        
        // 创建用于显示的日期对象
        const displayDate = new Date(date);
        displayDate.setMinutes(localMinute >= 60 ? 55 : localMinute, 0, 0);
        
        // 获取年月日
        const year = displayDate.getFullYear();
        const month = (displayDate.getMonth() + 1).toString().padStart(2, '0');
        const day = displayDate.getDate().toString().padStart(2, '0');
        
        console.log('解析日期时间:', {
          original: deadlineStr,
          parsed: displayDate.toString(),
          date: `${year}-${month}-${day}`,
          hour: displayDate.getHours(),
          minute: displayDate.getMinutes()
        });
        
        return {
          date: `${year}-${month}-${day}`,
          hour: parseInt(displayDate.getHours()),
          minute: parseInt(displayDate.getMinutes())
        };
      } catch (error) {
        console.error('解析日期出错:', error);
        return { date: '', hour: 0, minute: 0 };
      }
    },
    
    // 更新截止日期
    updateDeadline() {
      // 确保所有日期时间组件都已设置
      if (!this.deadlineDate) return;
      
      // 确保时间组件为数字类型
      this.deadlineHour = parseInt(this.deadlineHour);
      this.deadlineMinute = parseInt(this.deadlineMinute);
      
      // 处理分钟为5分钟的倍数
      this.deadlineMinute = Math.round(this.deadlineMinute / 5) * 5;
      if (this.deadlineMinute >= 60) {
        this.deadlineMinute = 55;
      }
      
      console.log('更新截止日期:', {
        date: this.deadlineDate,
        hour: this.deadlineHour,
        minute: this.deadlineMinute
      });
    },
    
    // 设置快捷截止日期
    setQuickDeadline(option) {
      const now = new Date();
      // 向上取整到5分钟间隔
      const minute = Math.ceil(now.getMinutes() / 5) * 5;
      now.setMinutes(minute >= 60 ? 55 : minute);
      
      if (option === 'today') {
        // 今天，当前时间
        this.deadlineDate = now.toISOString().split('T')[0];
        this.deadlineHour = now.getHours();
        this.deadlineMinute = now.getMinutes();
      } else if (option === 'tomorrow') {
        // 明天，同一时间
        const tomorrow = new Date(now);
        tomorrow.setDate(now.getDate() + 1);
        this.deadlineDate = tomorrow.toISOString().split('T')[0];
        this.deadlineHour = tomorrow.getHours();
        this.deadlineMinute = tomorrow.getMinutes();
      } else if (option === 'nextWeek') {
        // 下周，同一时间
        const nextWeek = new Date(now);
        nextWeek.setDate(now.getDate() + 7);
        this.deadlineDate = nextWeek.toISOString().split('T')[0];
        this.deadlineHour = nextWeek.getHours();
        this.deadlineMinute = nextWeek.getMinutes();
      }
    },
    
    // 设置快捷时间
    setQuickTime(hour, minute) {
      this.deadlineHour = hour;
      this.deadlineMinute = minute;
    },
    
    // 格式化日期为输入框格式
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
    
    submitForm() {
      // 验证表单
      if (!this.form.title || this.form.title.trim() === '') {
        alert('请输入任务标题');
        return;
      }
      
      // 先确保整数类型
      if (this.deadlineHour !== undefined) {
        this.deadlineHour = parseInt(this.deadlineHour);
      }
      if (this.deadlineMinute !== undefined) {
        this.deadlineMinute = parseInt(this.deadlineMinute);
      }
      
      // 处理截止日期
      let formData = { 
        ...this.form,
        completed: this.isEdit ? this.todo.completed : false // 保留编辑时的状态，或默认为未完成
      };
      
      // 如果未启用分组选项，清空分组ID
      if (!this.showGroup) {
        formData.group_id = null;
      }
      
      // 如果未启用截止日期选项，清空截止日期
      if (!this.showDeadline) {
        formData.deadline = null;
      } else if (this.deadlineDate) {
        try {
          // 创建日期对象并设置为用户选择的本地时间
          const [year, month, day] = this.deadlineDate.split('-').map(Number);
          const hour = !isNaN(this.deadlineHour) ? this.deadlineHour : 0;
          const minute = !isNaN(this.deadlineMinute) ? this.deadlineMinute : 0;
          
          // 注意：JavaScript中月份从0开始，所以需要减1
          const localDate = new Date(year, month - 1, day, hour, minute, 0, 0);
          
          // 计算时区偏移量（分钟）
          const timezoneOffset = localDate.getTimezoneOffset();
          
          // 创建一个新的日期，加上时区偏移，这样转换为ISO时会保留用户选择的本地时间
          const utcDate = new Date(localDate.getTime() - timezoneOffset * 60000);
          formData.deadline = utcDate.toISOString();
          
          console.log('设置的截止日期:', {
            localTime: localDate.toString(),
            utcTime: utcDate.toISOString(),
            timezoneOffset,
            formValues: {
              date: this.deadlineDate,
              hour: this.deadlineHour,
              minute: this.deadlineMinute
            }
          });
        } catch (error) {
          console.error('日期转换错误', error);
          formData.deadline = null;
        }
      }
      
      // 发送表单数据
      this.$emit('submit', formData);
    }
  }
}
</script>

<style scoped>
.modal-backdrop {
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
  padding: 20px;
}

.todo-form {
  background-color: white;
  border-radius: 16px;
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 0;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  animation: slide-in 0.3s ease;
  position: relative;
}

@keyframes slide-in {
  from { transform: translateY(30px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #f1f2f6;
  position: sticky;
  top: 0;
  background-color: white;
  z-index: 1;
  border-radius: 16px 16px 0 0;
}

.form-header h2 {
  margin: 0;
  color: #2d3436;
  font-size: 20px;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: #636e72;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background-color: #f1f2f6;
  transform: none;
  box-shadow: none;
}

form {
  padding: 20px 24px 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #636e72;
  font-size: 14px;
}

input[type="text"],
textarea,
select,
input[type="datetime-local"] {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #dfe6e9;
  border-radius: 8px;
  font-size: 15px;
  transition: all 0.2s ease;
  color: #2d3436;
  background-color: #f8f9fa;
}

input[type="text"]:focus,
textarea:focus,
select:focus,
input[type="datetime-local"]:focus {
  outline: none;
  border-color: #74b9ff;
  box-shadow: 0 0 0 3px rgba(116, 185, 255, 0.2);
  background-color: white;
}

input[type="text"]::placeholder,
textarea::placeholder {
  color: #b2bec3;
}

textarea {
  resize: vertical;
  min-height: 100px;
  max-height: 200px;
}

select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23636e72' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 16px;
  padding-right: 40px;
}

/* 切换开关样式 */
.toggle-section {
  margin-bottom: 16px;
  border: 1px solid #f1f2f6;
  border-radius: 12px;
  overflow: hidden;
}

.toggle-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background-color: #f8f9fa;
  transition: background-color 0.2s ease;
}

.toggle-header span {
  font-weight: 500;
  color: #2d3436;
  user-select: none;
}

.toggle-switch {
  position: relative;
  width: 44px;
  height: 24px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
  position: absolute;
}

.toggle-switch label {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #dfe6e9;
  border-radius: 34px;
  cursor: pointer;
  transition: .4s;
}

.toggle-switch label:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  border-radius: 50%;
  transition: .4s;
}

.toggle-switch input:checked + label {
  background-color: #74b9ff;
}

.toggle-switch input:checked + label:before {
  transform: translateX(20px);
}

.toggle-content {
  padding: 0 16px 16px;
  border-top: 1px solid #f1f2f6;
  animation: fade-in 0.3s ease;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.submit-btn, .cancel-btn {
  padding: 12px 24px;
  font-size: 15px;
  font-weight: 500;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.submit-btn {
  background-color: #4cd137;
  color: white;
}

.submit-btn:hover {
  background-color: #44bd32;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(76, 209, 55, 0.2);
}

.cancel-btn {
  background-color: #f1f2f6;
  color: #636e72;
}

.cancel-btn:hover {
  background-color: #dfe4ea;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(99, 110, 114, 0.1);
}

@media (max-width: 640px) {
  .modal-backdrop {
    padding: 0;
    align-items: flex-end;
}

  .todo-form {
    max-width: 100%;
    border-radius: 16px 16px 0 0;
    max-height: 85vh;
    animation: slide-up 0.3s ease;
  }

  @keyframes slide-up {
    from { transform: translateY(100%); }
    to { transform: translateY(0); }
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .submit-btn, .cancel-btn {
    width: 100%;
  }
}

.deadline-selection {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.deadline-date-selection, .deadline-time-selection {
  margin-top: 8px;
}

.deadline-date-selection label, .deadline-time-selection label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #636e72;
  font-size: 14px;
}

.time-inputs {
  display: flex;
  align-items: center;
  gap: 4px;
}

.time-inputs select {
  background-color: #f8f9fa;
  border: 1px solid #dfe6e9;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 15px;
  width: auto;
  min-width: 70px;
}

.time-inputs span {
  font-weight: bold;
  font-size: 18px;
  color: #636e72;
}
</style> 