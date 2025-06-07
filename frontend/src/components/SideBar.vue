<template>
  <div class="sidebar" @click="hideContextMenu">
    <!-- 系统预设分类 -->
    <div class="filter-grid">
      <!-- 日历视图按钮 -->
      <router-link to="/calendar" class="calendar-link">
        <div class="filter-card calendar-card">
          <div class="left-section">
            <div class="filter-icon circle-icon" style="background-color: #FF9F43">
            <i class="calendar-icon">📅</i>
          </div>
            <div class="filter-name">日历</div>
          </div>
          <div class="right-section">
            <!-- 右侧可为空或放置其他内容 -->
          </div>
        </div>
      </router-link>
      
      <!-- 时间段任务按钮 -->
      <router-link to="/timeblocks" class="timeblock-link">
        <div class="filter-card timeblock-card">
          <div class="left-section">
            <div class="filter-icon circle-icon" style="background-color: #FF9F43">
            <span>⏱️</span>
          </div>
            <div class="filter-name">时间段</div>
          </div>
          <div class="right-section">
            <!-- 右侧可为空或放置其他内容 -->
          </div>
        </div>
      </router-link>
      
      <div 
        v-for="filter in filters" 
        :key="filter.id" 
        class="filter-card"
        :class="{ active: selectedFilter === filter.id }"
        @click="selectFilter(filter.id)"
      >
        <div class="left-section">
          <div class="filter-icon circle-icon" :style="{ backgroundColor: filter.color }">
          <i v-if="filter.icon" :class="filter.icon"></i>
          <span v-else-if="filter.text">{{ filter.text }}</span>
        </div>
          <div class="filter-name">{{ filter.name }}</div>
        </div>
        <div class="right-section">
        <div class="filter-count">{{ filterCounts[filter.id] || 0 }}</div>
        </div>
      </div>
    </div>
    
    <!-- 分组列表 -->
    <div class="group-section">
      <div class="section-header">
        <h3>分组</h3>
        <button class="btn-add" @click="showCreateModal = true">+</button>
      </div>
      
      <div 
        v-for="group in groups" 
        :key="group.id" 
        class="group-item"
        :class="{ active: selectedGroup === group.id }"
        @click="selectGroup(group.id)"
        @contextmenu.prevent="showContextMenuForGroup($event, group)"
      >
        <div class="group-icon" :style="{ backgroundColor: group.color || '#8E8E93' }"></div>
        <span class="name">{{ group.name }}</span>
        <span class="count">{{ group.todo_count || 0 }}</span>
      </div>
      
      <div v-if="groups.length === 0" class="no-groups">
        暂无分组，点击"+"创建分组
      </div>
    </div>
    
    <!-- 右键菜单 -->
    <div 
      v-if="showContextMenu" 
      class="context-menu"
      :style="{ top: contextMenuPosition.y + 'px', left: contextMenuPosition.x + 'px' }"
    >
      <div class="menu-item" @click="startEditGroup">
        <span>✏️ 编辑分组</span>
      </div>
      <div class="menu-item" @click="confirmDeleteGroup">
        <span>🗑️ 删除分组</span>
      </div>
    </div>
    
    <!-- 创建分组模态框 -->
    <div v-if="showCreateModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="showCreateModal = false">&times;</span>
        <h3>创建新分组</h3>
        
        <form @submit.prevent="createGroup">
          <div class="form-group">
            <label for="name">分组名称:</label>
            <input 
              type="text" 
              id="name" 
              v-model="newGroup.name" 
              required
              placeholder="输入分组名称"
              ref="newGroupNameInput"
            />
          </div>
          
          <div class="form-group">
            <label>选择颜色:</label>
            <div class="color-presets">
              <div 
                v-for="(color, index) in presetColors" 
                :key="index"
                class="color-option"
                :class="{ active: newGroup.color === color }"
                :style="{ backgroundColor: color }"
                @click="newGroup.color = color"
              >
                <span v-if="newGroup.color === color" class="check-icon">✓</span>
              </div>
            </div>
          </div>
          
          <div class="modal-actions">
            <button type="button" class="btn" @click="showCreateModal = false">取消</button>
            <button type="submit" class="btn btn-primary">创建</button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- 编辑分组模态框 -->
    <div v-if="showEditModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="showEditModal = false">&times;</span>
        <h3>编辑分组</h3>
        
        <form @submit.prevent="updateGroup" v-if="editingGroup">
          <div class="form-group">
            <label for="edit-name">名称:</label>
            <input 
              type="text" 
              id="edit-name" 
              v-model="editingGroup.name" 
              required
              ref="editGroupNameInput"
            />
          </div>
          
          <div class="form-group">
            <label>选择颜色:</label>
            <div class="color-presets">
              <div 
                v-for="(color, index) in presetColors" 
                :key="index"
                class="color-option"
                :class="{ active: editingGroup.color === color }"
                :style="{ backgroundColor: color }"
                @click="editingGroup.color = color"
              >
                <span v-if="editingGroup.color === color" class="check-icon">✓</span>
              </div>
            </div>
          </div>
          
          <div class="modal-actions">
            <button type="button" class="btn" @click="showEditModal = false">取消</button>
            <button type="submit" class="btn btn-primary">保存</button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- 删除确认模态框 -->
    <div v-if="showDeleteModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="showDeleteModal = false">&times;</span>
        <h3>确认删除</h3>
        
        <p v-if="deletingGroup">
          确定要删除分组 "{{ deletingGroup.name }}" 吗？
          <br />
          <small>该分组下的所有任务将被移动到"未分组"</small>
        </p>
        
        <div class="modal-actions">
          <button type="button" class="btn" @click="showDeleteModal = false">取消</button>
          <button type="button" class="btn btn-danger" @click="deleteGroup">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { groupAPI } from '@/api';
import { timeBlockAPI } from '@/api';
import groupCache from '@/api/groupCache';
import { formatDateForInput } from '@/utils/dateUtils';

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
      filterCounts: {},
      
      // 右键菜单
      showContextMenu: false,
      contextMenuPosition: { x: 0, y: 0 },
      contextMenuGroup: null,
      
      // 模态框
      showCreateModal: false,
      showEditModal: false,
      showDeleteModal: false,
      
      // 分组操作
      newGroup: {
        name: '',
        color: '#FF9F43',
        description: ''
      },
      editingGroup: null,
      deletingGroup: null,
      
      // 预设颜色
      presetColors: [
        '#FF9F43', // 橙色
        '#3E7BFA', // 蓝色
        '#A66AFF', // 紫色
        '#98A4B5', // 灰色
        '#FFCC41', // 黄色
        '#FF5252'  // 红色
      ]
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
    
    // 添加全局点击事件监听器，用于关闭右键菜单
    document.addEventListener('click', this.hideContextMenu);
    
    // 根据当前路由设置选中状态
    this.updateSelectedFromRoute();
  },
  beforeDestroy() {
    // 移除全局点击事件监听器
    document.removeEventListener('click', this.hideContextMenu);
  },
  watch: {
    // 监听路由变化
    '$route'() {
      this.updateSelectedFromRoute();
    }
  },
  methods: {
    // 根据当前路由更新选中状态
    updateSelectedFromRoute() {
      const path = this.$route.path;
      
      if (path === '/') {
        const groupId = this.$route.query.group;
        if (groupId) {
          this.selectedFilter = null;
          this.selectedGroup = groupId;
        } else {
          this.selectedFilter = 'all';
          this.selectedGroup = null;
        }
      } else if (path === '/calendar') {
        this.selectedFilter = null;
        this.selectedGroup = null;
      } else if (path === '/timeblocks') {
        this.selectedFilter = null;
        this.selectedGroup = null;
      }
    },
    
    async loadGroups() {
      try {
        const response = await groupCache.getGroups();
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
    
    // 右键菜单相关方法
    showContextMenuForGroup(event, group) {
      // 设置右键菜单位置
      this.contextMenuPosition = {
        x: event.clientX,
        y: event.clientY
      };
      
      // 设置当前操作的分组
      this.contextMenuGroup = group;
      
      // 显示右键菜单
      this.showContextMenu = true;
      
      // 阻止事件冒泡
      event.stopPropagation();
    },
    
    hideContextMenu() {
      this.showContextMenu = false;
    },
    
    // 开始编辑分组
    startEditGroup() {
      if (!this.contextMenuGroup) return;
      
      this.editingGroup = { 
        id: this.contextMenuGroup.id,
        name: this.contextMenuGroup.name,
        color: this.contextMenuGroup.color,
        description: this.contextMenuGroup.description || ''
      };
      
      this.showEditModal = true;
      this.hideContextMenu();
      
      // 自动聚焦到名称输入框
      this.$nextTick(() => {
        if (this.$refs.editGroupNameInput) {
          this.$refs.editGroupNameInput.focus();
        }
      });
    },
    
    // 确认删除分组
    confirmDeleteGroup() {
      if (!this.contextMenuGroup) return;
      
      this.deletingGroup = this.contextMenuGroup;
      this.showDeleteModal = true;
      this.hideContextMenu();
    },
    
    // 创建新分组
    async createGroup() {
      try {
        if (!this.newGroup.name.trim()) {
          alert('请输入分组名称');
          return;
        }
        
        const response = await groupAPI.createGroup(this.newGroup);
        if (response.success) {
          // 清除分组缓存
          groupCache.invalidateCache();
          // 重新加载分组列表
          await this.loadGroups();
          
          // 重置表单并关闭模态框
          this.newGroup = {
            name: '',
            color: this.presetColors[0],
            description: ''
          };
          this.showCreateModal = false;
        } else {
          alert(`创建分组失败: ${response.error}`);
        }
      } catch (error) {
        console.error('创建分组出错:', error);
        alert('创建分组失败，请稍后重试');
      }
    },
    
    // 更新分组
    async updateGroup() {
      try {
        if (!this.editingGroup || !this.editingGroup.name.trim()) {
          alert('请输入分组名称');
          return;
        }
        
        const response = await groupAPI.updateGroup(
          this.editingGroup.id,
          {
            name: this.editingGroup.name,
            color: this.editingGroup.color,
            description: this.editingGroup.description || ''
          }
        );
        
        if (response.success) {
          // 清除分组缓存
          groupCache.invalidateCache();
          // 重新加载分组列表
          await this.loadGroups();
          
          // 关闭模态框
          this.showEditModal = false;
          this.editingGroup = null;
          
          // 发出分组更新事件通知父组件
          this.$emit('group-updated');
        } else {
          alert(`更新分组失败: ${response.error}`);
        }
      } catch (error) {
        console.error('更新分组出错:', error);
        alert('更新分组失败，请稍后重试');
      }
    },
    
    // 删除分组
    async deleteGroup() {
      try {
        if (!this.deletingGroup) return;
        
        const response = await groupAPI.deleteGroup(this.deletingGroup.id);
        if (response.success) {
          // 清除分组缓存
          groupCache.invalidateCache();
          
          // 如果当前选中的是被删除的分组，则切换到全部
          if (this.selectedGroup === this.deletingGroup.id) {
            this.selectFilter('all');
          }
          
          // 重新加载分组列表
          await this.loadGroups();
          
          // 关闭模态框
          this.showDeleteModal = false;
          this.deletingGroup = null;
          
          // 发出分组删除事件通知父组件
          this.$emit('group-updated');
        } else {
          alert(`删除分组失败: ${response.error}`);
        }
      } catch (error) {
        console.error('删除分组出错:', error);
        alert('删除分组失败，请稍后重试');
      }
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
  width: 280px; /* 加宽侧边栏 */
  height: 100%;
  padding: 16px;
  border-right: 1px solid #E6E8F0;
  overflow-y: auto;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.05);
  position: relative;
}

/* 日历视图链接样式 */
.calendar-link {
  text-decoration: none;
  display: block;
}

.calendar-card {
  background-color: #fff5e6;
  transition: all 0.3s ease;
}

.calendar-card:hover {
  /* 移除悬浮动画效果 */
}

.calendar-icon {
  font-style: normal;
  font-size: 20px;
}

.filter-grid {
  display: grid;
  grid-template-columns: 1fr 1fr; /* 修改为两列布局 */
  gap: 12px;
  margin-bottom: 24px;
}

.filter-card {
  background-color: white;
  border-radius: 12px;
  padding: 14px 16px;
  position: relative; /* 确保可以进行绝对定位 */
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: row; /* 改回横向排列 */
  align-items: center;
  justify-content: space-between; /* 左右两端对齐 */
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
  border: 1px solid #EAECEF;
  text-align: center;
  height: 70px; /* 固定高度确保横向长方形 */
}

.filter-card:hover {
  /* 移除悬浮动画效果 */
}

.filter-card.active {
  background-color: #F5F7FF;
  border-color: #DEE5FF;
  box-shadow: 0 3px 8px rgba(94, 114, 228, 0.15);
}

.filter-icon {
  width: 30px; /* 缩小图标 */
  height: 30px; /* 缩小图标 */
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 16px; /* 缩小字体 */
  font-weight: bold;
  margin-right: 0;
  margin-bottom: 0;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.circle-icon {
  border-radius: 50%;
}

.filter-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start; /* 左对齐 */
  padding-left: 10px; /* 与图标保持距离 */
}

.filter-name {
  font-size: 13px;
  color: #525F7F;
  font-weight: 600;
  margin-bottom: 0;
}

.filter-count {
  position: absolute; /* 绝对定位 */
  top: 10px; /* 顶部距离 */
  right: 10px; /* 右侧距离 */
  font-size: 17px; /* 稍微减小字体大小 */
  font-weight: 700;
  color: #8898AA;
  background-color: transparent; /* 移除背景 */
  padding: 2px 0; /* 调整内边距 */
  min-width: 20px;
  text-align: center;
  margin-right: 5px; /* 右侧留出空间 */
}

/* 左侧布局容器：图标+文字 */
.left-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: auto;
}

/* 右侧数字计数 */
.right-section {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 时间段链接样式 */
.timeblock-section {
  margin-bottom: 24px;
}

.timeblock-link {
  text-decoration: none;
  display: block;
}

.timeblock-link.active .timeblock-button {
  background-color: #F5F7FF;
  border-color: #DEE5FF;
  box-shadow: 0 3px 8px rgba(94, 114, 228, 0.15);
}

.timeblock-button {
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

.timeblock-button:hover {
  /* 移除悬浮动画效果 */
}

.timeblock-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #FF9F43;
  color: white;
  font-size: 18px;
  margin-right: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.timeblock-text {
  font-size: 15px;
  color: #525F7F;
  font-weight: 600;
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
  /* 移除悬浮动画效果 */
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

.btn-add {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: #F1F5FF;
  color: #5E72E4;
  border: none;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.btn-add:hover {
  background-color: #5E72E4;
  color: white;
  transform: scale(1.1);
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

/* 右键菜单样式 */
.context-menu {
  position: fixed;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 8px 0;
  min-width: 150px;
  z-index: 1000;
  animation: fade-in 0.15s ease-out;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}

.menu-item {
  padding: 8px 12px;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  transition: all 0.2s ease;
}

.menu-item:hover {
  background-color: #F5F7FF;
}

.menu-item span {
  margin-left: 4px;
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
  border-radius: 12px;
  padding: 24px;
  width: 90%;
  max-width: 400px;
  position: relative;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  animation: slide-up 0.2s ease-out;
}

@keyframes slide-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.close {
  position: absolute;
  top: 16px;
  right: 16px;
  font-size: 24px;
  color: #8898AA;
  cursor: pointer;
  transition: color 0.2s ease;
}

.close:hover {
  color: #5E72E4;
}

.modal h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #525F7F;
  font-size: 18px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #8898AA;
  font-weight: 500;
  font-size: 14px;
}

.form-group input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #E6E8F0;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.2s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #5E72E4;
  box-shadow: 0 0 0 3px rgba(94, 114, 228, 0.15);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.btn {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn:hover {
  transform: translateY(-1px);
}

.btn-primary {
  background-color: #5E72E4;
  color: white;
  box-shadow: 0 4px 10px rgba(94, 114, 228, 0.3);
}

.btn-primary:hover {
  background-color: #4d61c9;
  box-shadow: 0 6px 15px rgba(94, 114, 228, 0.4);
}

.btn-danger {
  background-color: #f5365c;
  color: white;
  box-shadow: 0 4px 10px rgba(245, 54, 92, 0.3);
}

.btn-danger:hover {
  background-color: #e82753;
  box-shadow: 0 6px 15px rgba(245, 54, 92, 0.4);
}

/* 颜色选择器样式 */
.color-presets {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 8px;
}

.color-option {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  border: 2px solid transparent;
}

.color-option:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.color-option.active {
  border-color: white;
  box-shadow: 0 0 0 2px #5E72E4;
}

.check-icon {
  color: white;
  font-size: 14px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.timeblock-card {
  background-color: #fff5e6;
  transition: all 0.3s ease;
}

.timeblock-card:hover {
  background-color: #ffebcc;
}
</style> 