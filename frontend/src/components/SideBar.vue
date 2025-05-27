<template>
  <div class="sidebar">
    <!-- 系统预设分类 -->
    <div class="filter-grid">
      <div 
        v-for="filter in filters" 
        :key="filter.id" 
        class="filter-card"
        :class="{ active: selectedFilter === filter.id }"
        @click="selectFilter(filter.id)"
      >
        <div class="filter-icon" :style="{ backgroundColor: filter.color }">
          <i v-if="filter.icon" :class="filter.icon"></i>
          <span v-else-if="filter.text">{{ filter.text }}</span>
        </div>
        <div class="filter-info">
          <div class="filter-name">{{ filter.name }}</div>
          <div class="filter-count">{{ filterCounts[filter.id] || 0 }}</div>
        </div>
      </div>
    </div>
    
    <!-- 分组列表 -->
    <div class="group-section">
      <div class="section-header">
        <h3>分组</h3>
        <button class="btn-manage" @click="manageGroups">管理</button>
      </div>
      
      <div 
        v-for="group in groups" 
        :key="group.id" 
        class="group-item"
        :class="{ active: selectedGroup === group.id }"
        @click="selectGroup(group.id)"
      >
        <div class="group-icon" :style="{ backgroundColor: group.color || '#8E8E93' }"></div>
        <span class="name">{{ group.name }}</span>
        <span class="count">{{ group.todo_count || 0 }}</span>
      </div>
      
      <div v-if="groups.length === 0" class="no-groups">
        暂无分组，请先创建分组
      </div>
    </div>
  </div>
</template>

<script>
import { groupAPI } from '@/api';

export default {
  name: 'SideBar',
  data() {
    return {
      filters: [
        { id: 'today', name: '今天', text: '26', color: '#5E72E4' },
        { id: 'all', name: '全部', text: '📋', color: '#11CDEF' },
        { id: 'completed', name: '完成', text: '✅', color: '#2DCE89' }
      ],
      groups: [],
      selectedFilter: 'all',
      selectedGroup: null,
      filterCounts: {}
    };
  },
  created() {
    this.loadGroups();
    
    // 示例数据，实际应该从后端获取
    this.filterCounts = {
      today: 0,
      all: 1,
      completed: 0
    };
  },
  methods: {
    async loadGroups() {
      try {
        const response = await groupAPI.getAllGroups();
        if (response.success) {
          this.groups = response.data;
        } else {
          console.error('加载分组失败:', response.error);
        }
      } catch (error) {
        console.error('加载分组出错:', error);
      }
    },
    
    selectFilter(filterId) {
      this.selectedFilter = filterId;
      this.selectedGroup = null;
      this.$emit('filter-selected', { type: 'filter', id: filterId });
    },
    
    selectGroup(groupId) {
      this.selectedGroup = groupId;
      this.selectedFilter = null;
      this.$emit('filter-selected', { type: 'group', id: groupId });
    },
    
    manageGroups() {
      this.$router.push('/groups');
    },
    
    // 更新各个筛选选项的任务数量
    updateCounts(counts) {
      this.filterCounts = {...counts};
    }
  }
};
</script>

<style scoped>
.sidebar {
  background-color: #F8F9FE;
  width: 250px;
  height: 100%;
  padding: 16px;
  border-right: 1px solid #E6E8F0;
  overflow-y: auto;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.05);
}

.filter-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
  margin-bottom: 24px;
}

.filter-card {
  background-color: white;
  border-radius: 12px;
  padding: 14px 16px;
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
  border: 1px solid #EAECEF;
}

.filter-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.filter-card.active {
  background-color: #F5F7FF;
  border-color: #DEE5FF;
  box-shadow: 0 3px 8px rgba(94, 114, 228, 0.15);
}

.filter-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
  font-weight: bold;
  margin-right: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.filter-icon span {
  font-size: 18px;
}

.filter-icon i {
  font-size: 18px;
}

.filter-info {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-name {
  font-size: 15px;
  color: #525F7F;
  font-weight: 600;
}

.filter-count {
  font-size: 16px;
  font-weight: 700;
  color: #8898AA;
  background-color: #F8F9FE;
  padding: 2px 8px;
  border-radius: 10px;
  min-width: 24px;
  text-align: center;
}

.group-section {
  margin-top: 24px;
}

.group-item {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  border-radius: 8px;
  margin-bottom: 4px;
}

.group-item:hover {
  background-color: #F5F7FF;
}

.group-item.active {
  background-color: #F5F7FF;
  font-weight: 500;
}

.group-icon {
  width: 20px;
  height: 20px;
  border-radius: 6px;
  margin-right: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.name {
  flex-grow: 1;
  font-size: 14px;
  color: #525F7F;
  font-weight: 400;
}

.count {
  font-size: 14px;
  color: #8898AA;
  font-weight: 500;
  background-color: #F8F9FE;
  padding: 1px 6px;
  border-radius: 8px;
  min-width: 20px;
  text-align: center;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 5px;
  margin-bottom: 10px;
}

.section-header h3 {
  font-size: 13px;
  color: #8898AA;
  margin: 0;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-manage {
  background: none;
  border: none;
  color: #5E72E4;
  cursor: pointer;
  font-size: 13px;
  padding: 0;
  font-weight: 500;
  transition: color 0.2s;
}

.btn-manage:hover {
  color: #324CDD;
  text-decoration: underline;
}

.no-groups {
  padding: 12px;
  color: #8898AA;
  font-style: italic;
  text-align: center;
  font-size: 13px;
  background-color: #F8F9FE;
  border-radius: 8px;
  margin-top: 10px;
}
</style> 