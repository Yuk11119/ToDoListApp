<template>
  <div class="calendar-container">
    <div class="app-layout">
      <!-- 侧边栏 -->
      <SideBar 
        @filter-selected="applyFilter" 
        @group-updated="refreshTasks"
        ref="sidebar"
      />
      
      <!-- 主内容区域 -->
      <div class="calendar-view">
        <div class="calendar-header">
          <div class="month-navigation">
            <button class="nav-btn" @click="previousMonth">
              <span>&laquo;</span>
            </button>
            <h2>{{ currentMonthName }} {{ currentYear }}</h2>
            <button class="nav-btn" @click="nextMonth">
              <span>&raquo;</span>
            </button>
          </div>
        </div>
        
        <div class="calendar-grid">
          <!-- 星期头部 -->
          <div v-for="day in weekDays" :key="day" class="calendar-cell weekday">
            {{ day }}
          </div>
          
          <!-- 日历格子 -->
          <div 
            v-for="(day, index) in calendarDays" 
            :key="index"
            class="calendar-cell"
            :class="{ 
              'inactive': !day.isCurrentMonth,
              'today': day.isToday,
              'has-tasks': day.tasks && day.tasks.length
            }"
          >
            <div class="date-number">{{ day.date }}</div>
            
            <!-- 当天任务 -->
            <div class="tasks-container" v-if="day.tasks && day.tasks.length">
              <div 
                v-for="task in day.tasks.slice(0, maxTasksPerCell)" 
                :key="task.id"
                class="calendar-task"
                :class="{ 
                  'completed': task.completed,
                  'ungrouped-task': !task.group_color 
                }"
                @click="viewTaskDetails(task)"
                :style="getTaskStyle(task)"
              >
                <div class="task-title">
                  <span v-if="!task.group_color" class="ungrouped-indicator">◇</span>
                  {{ task.title }}
                </div>
              </div>
              
              <!-- 如果有更多任务则显示更多提示 -->
              <div class="more-tasks" v-if="day.tasks.length > maxTasksPerCell">
                +{{ day.tasks.length - maxTasksPerCell }} 更多
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import todoApi from '@/api/todo';
import SideBar from '@/components/SideBar.vue';

export default {
  name: 'CalendarView',
  components: {
    SideBar
  },
  data() {
    return {
      currentDate: new Date(),
      tasks: [],
      weekDays: ['日', '一', '二', '三', '四', '五', '六'],
      maxTasksPerCell: 3, // 每个日历格子最多显示的任务数
      loading: false
    };
  },
  computed: {
    currentYear() {
      return this.currentDate.getFullYear();
    },
    currentMonth() {
      return this.currentDate.getMonth();
    },
    currentMonthName() {
      return new Date(this.currentYear, this.currentMonth, 1).toLocaleString('zh-CN', { month: 'long' });
    },
    calendarDays() {
      // 获取当月第一天是星期几（0-6）
      const firstDayOfMonth = new Date(this.currentYear, this.currentMonth, 1).getDay();
      
      // 获取当月天数
      const daysInMonth = new Date(this.currentYear, this.currentMonth + 1, 0).getDate();
      
      // 获取上个月的天数
      const daysInPreviousMonth = new Date(this.currentYear, this.currentMonth, 0).getDate();
      
      // 日历格子数组
      const days = [];
      
      // 填充上个月的日期
      for (let i = firstDayOfMonth - 1; i >= 0; i--) {
        const prevMonthDate = daysInPreviousMonth - i;
        const date = new Date(this.currentYear, this.currentMonth - 1, prevMonthDate);
        days.push({
          date: prevMonthDate,
          isCurrentMonth: false,
          isToday: this.isToday(date),
          fullDate: date,
          tasks: this.getTasksForDate(date)
        });
      }
      
      // 填充当月的日期
      for (let i = 1; i <= daysInMonth; i++) {
        const date = new Date(this.currentYear, this.currentMonth, i);
        days.push({
          date: i,
          isCurrentMonth: true,
          isToday: this.isToday(date),
          fullDate: date,
          tasks: this.getTasksForDate(date)
        });
      }
      
      // 填充下个月的日期，确保日历格子总数是7的倍数（整行显示）
      const nextMonthDays = 42 - days.length; // 6行7列 = 42个格子
      for (let i = 1; i <= nextMonthDays; i++) {
        const date = new Date(this.currentYear, this.currentMonth + 1, i);
        days.push({
          date: i,
          isCurrentMonth: false,
          isToday: this.isToday(date),
          fullDate: date,
          tasks: this.getTasksForDate(date)
        });
      }
      
      return days;
    }
  },
  created() {
    this.fetchTasks();
    // nextTick确保DOM渲染后再执行
    this.$nextTick(() => {
      if (this.$refs.sidebar) {
        this.$refs.sidebar.loadGroups();
      }
    });
  },
  methods: {
    // 获取任务数据
    async fetchTasks() {
      this.loading = true;
      try {
        const response = await todoApi.getAllTodos();
        if (response.success) {
          this.tasks = response.data || [];
          // 更新侧边栏任务计数
          this.updateFilterCounts();
        } else {
          console.error('获取任务失败:', response.error);
        }
      } catch (error) {
        console.error('获取任务出错:', error);
      } finally {
        this.loading = false;
      }
    },
    
    // 更新过滤器计数
    updateFilterCounts() {
      // 计算每个筛选选项的任务数量
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      const tomorrow = new Date(today);
      tomorrow.setDate(tomorrow.getDate() + 1);
      
      const counts = {
        all: this.tasks.length,
        today: this.tasks.filter(todo => {
          if (!todo.deadline) return false;
          const deadline = new Date(todo.deadline);
          return deadline >= today && deadline < tomorrow;
        }).length,
        scheduled: this.tasks.filter(todo => todo.deadline).length,
        flagged: 0, // 暂不实现
        completed: this.tasks.filter(todo => todo.completed).length
      };
      
      // 如果侧边栏组件已经渲染，更新它的计数
      if (this.$refs.sidebar) {
        this.$refs.sidebar.updateCounts(counts);
      }
    },
    
    // 刷新任务（响应分组更新事件）
    async refreshTasks() {
      await this.fetchTasks();
    },
    
    // 处理侧边栏筛选
    applyFilter(filter) {
      // 跳转到主页并应用过滤条件
      this.$router.push({
        path: '/',
        query: { filter: filter.type, id: filter.id }
      });
    },
    
    // 月份导航
    previousMonth() {
      this.currentDate = new Date(this.currentYear, this.currentMonth - 1, 1);
    },
    
    nextMonth() {
      this.currentDate = new Date(this.currentYear, this.currentMonth + 1, 1);
    },
    
    // 判断日期是否为今天
    isToday(date) {
      const today = new Date();
      return date.getDate() === today.getDate() &&
             date.getMonth() === today.getMonth() &&
             date.getFullYear() === today.getFullYear();
    },
    
    // 获取指定日期的任务
    getTasksForDate(date) {
      if (!this.tasks || !this.tasks.length) return [];
      
      // 设置日期范围为当天的开始到结束
      const startOfDay = new Date(date);
      startOfDay.setHours(0, 0, 0, 0);
      
      const endOfDay = new Date(date);
      endOfDay.setHours(23, 59, 59, 999);
      
      // 筛选出当天截止的任务
      return this.tasks.filter(task => {
        if (!task.deadline) return false;
        
        const taskDate = new Date(task.deadline);
        return taskDate >= startOfDay && taskDate <= endOfDay;
      });
    },
    
    // 查看任务详情（修改为跳转到HomeView并编辑任务）
    viewTaskDetails(task) {
      this.$router.push({ 
        path: '/',
        query: { editTask: task.id }
      });
    },
    
    // 获取任务的样式，基于分组颜色
    getTaskStyle(task) {
      // 当任务没有分组颜色时，提供默认样式
      if (!task.group_color) {
        return {
          borderLeft: '3px solid #8E8E93', // 使用灰色作为未分组任务的标识
          backgroundColor: 'rgba(142, 142, 147, 0.1)', // 灰色背景，低透明度
        };
      }
      
      // 有分组颜色的任务保持原来的样式
      return {
        borderLeft: `3px solid ${task.group_color}`,
        backgroundColor: this.getColorWithOpacity(task.group_color, 0.1)
      };
    },
    
    // 获取带透明度的颜色
    getColorWithOpacity(color, opacity) {
      if (!color) return 'rgba(0, 0, 0, 0.1)';
      
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
      
      return `rgba(0, 0, 0, ${opacity})`;
    }
  }
};
</script>

<style scoped>
.calendar-container {
  height: 100%;
}

.app-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.calendar-view {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  background-color: #f8f9fa;
}

.calendar-header {
  margin-bottom: 24px;
}

.month-navigation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.month-navigation h2 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.nav-btn {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 18px;
  transition: all 0.2s ease;
}

.nav-btn:hover {
  /* 移除悬浮动画效果 */
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 16px;
}

.calendar-cell {
  min-height: 100px;
  padding: 8px;
  border-radius: 8px;
  background-color: #f8f9fa;
  position: relative;
}

.weekday {
  background-color: #5E72E4;
  color: white;
  font-weight: bold;
  min-height: auto;
  padding: 12px 8px;
  text-align: center;
  margin-bottom: 8px;
}

.date-number {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #333;
}

.today {
  background-color: #f5f7ff;
  border: 2px solid #5E72E4;
}

.today .date-number {
  color: #5E72E4;
}

.inactive {
  opacity: 0.5;
}

.has-tasks {
  background-color: #fcfcfc;
}

.tasks-container {
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-height: calc(100% - 30px);
  overflow-y: auto;
}

.calendar-task {
  padding: 4px 8px;
  border-radius: 4px;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.calendar-task:hover {
  /* 移除悬浮动画效果 */
}

.calendar-task.completed {
  opacity: 0.7;
  text-decoration: line-through;
}

.task-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.calendar-task.ungrouped-task {
  position: relative;
  /* 自定义未分组任务样式 */
}

.ungrouped-indicator {
  font-size: 10px;
  margin-right: 3px;
  opacity: 0.6;
}

.more-tasks {
  font-size: 11px;
  color: #5E72E4;
  text-align: center;
  margin-top: 4px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .calendar-view {
    padding: 16px;
  }
  
  .calendar-grid {
    gap: 4px;
    padding: 8px;
  }
  
  .calendar-cell {
    min-height: 80px;
    padding: 4px;
  }
  
  .weekday {
    padding: 8px 4px;
    font-size: 12px;
  }
  
  .date-number {
    font-size: 14px;
    margin-bottom: 4px;
  }
  
  .calendar-task {
    padding: 2px 4px;
    font-size: 10px;
  }
  
  .more-tasks {
    font-size: 9px;
  }
  
  .month-navigation h2 {
    font-size: 18px;
  }
  
  .nav-btn {
    width: 32px;
    height: 32px;
    font-size: 14px;
  }
}
</style> 