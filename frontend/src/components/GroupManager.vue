<template>
  <div class="group-manager">
    <h2>分组管理</h2>
    
    <!-- 添加新分组表单 -->
    <div class="group-form">
      <h3>添加新分组</h3>
      <form @submit.prevent="createGroup">
        <div class="form-group">
          <label for="name">分组名称:</label>
          <input 
            type="text" 
            id="name" 
            v-model="newGroup.name" 
            required
            placeholder="输入分组名称"
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
        
        <button type="submit" class="btn btn-primary">
          添加分组
        </button>
      </form>
    </div>
    
    <!-- 分组列表 -->
    <div class="group-list">
      <h3>现有分组</h3>
      <div v-if="loading">加载中...</div>
      <div v-else-if="groups.length === 0">暂无分组</div>
      <ul v-else>
        <li v-for="group in groups" :key="group.id" class="group-item">
          <div class="group-header">
            <div class="group-color" :style="{ backgroundColor: group.color }"></div>
            <h4>{{ group.name }}</h4>
            <span class="todo-count">{{ group.todo_count }} 个任务</span>
          </div>
          
          <div class="group-actions">
            <button @click="startEdit(group)" class="btn-edit">
              编辑
            </button>
            <button @click="confirmDelete(group)" class="btn-delete">
              删除
            </button>
          </div>
        </li>
      </ul>
    </div>
    
    <!-- 编辑分组弹窗 -->
    <div v-if="showEditModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="showEditModal = false">&times;</span>
        <h3>编辑分组</h3>
        
        <form @submit.prevent="updateGroup">
          <div class="form-group">
            <label for="edit-name">名称:</label>
            <input 
              type="text" 
              id="edit-name" 
              v-model="editingGroup.name" 
              required
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
          
          <button type="submit" class="btn btn-primary">
            保存
          </button>
        </form>
      </div>
    </div>
    
    <!-- 删除确认弹窗 -->
    <div v-if="showDeleteModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="showDeleteModal = false">&times;</span>
        <h3>确认删除</h3>
        
        <p>
          确定要删除分组 "{{ deletingGroup.name }}" 吗？
          <br />
          <small>该分组下的所有任务将被移动到"未分组"</small>
        </p>
        
        <div class="modal-actions">
          <button @click="showDeleteModal = false" class="btn">
            取消
          </button>
          <button @click="deleteGroup" class="btn btn-danger">
            删除
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { groupAPI } from '../api';

export default {
  name: 'GroupManager',
  data() {
    return {
      loading: true,
      groups: [],
      presetColors: [
        '#FF9F43', // 橙色
        '#3E7BFA', // 蓝色
        '#A66AFF', // 紫色
        '#98A4B5', // 灰色
        '#FFCC41', // 黄色
        '#FF5252'  // 红色
      ],
      newGroup: {
        name: '',
        color: '#FF9F43' // 默认选中第一个颜色
      },
      showEditModal: false,
      showDeleteModal: false,
      editingGroup: null,
      deletingGroup: null
    };
  },
  async created() {
    await this.loadGroups();
  },
  methods: {
    // 加载所有分组
    async loadGroups() {
      this.loading = true;
      try {
        const response = await groupAPI.getAllGroups();
        if (response.success) {
          this.groups = response.data;
        } else {
          console.error('加载分组失败:', response.error);
        }
      } catch (error) {
        console.error('加载分组出错:', error);
      } finally {
        this.loading = false;
      }
    },
    
    // 创建新分组
    async createGroup() {
      try {
        const response = await groupAPI.createGroup(this.newGroup);
        if (response.success) {
          // 发射事件通知父组件
          this.$emit('group-changed');
          
          // 重置表单
          this.newGroup = {
            name: '',
            color: this.presetColors[0] // 重置为第一个预设颜色
          };
          // 重新加载分组列表
          await this.loadGroups();
        } else {
          alert(`创建分组失败: ${response.error}`);
        }
      } catch (error) {
        console.error('创建分组出错:', error);
      }
    },
    
    // 开始编辑分组
    startEdit(group) {
      this.editingGroup = { 
        id: group.id,
        name: group.name,
        color: group.color
      };
      this.showEditModal = true;
    },
    
    // 更新分组
    async updateGroup() {
      try {
        const response = await groupAPI.updateGroup(
          this.editingGroup.id,
          {
            name: this.editingGroup.name,
            color: this.editingGroup.color
          }
        );
        
        if (response.success) {
          // 发射事件通知父组件
          this.$emit('group-changed');
          
          this.showEditModal = false;
          await this.loadGroups();
        } else {
          alert(`更新分组失败: ${response.error}`);
        }
      } catch (error) {
        console.error('更新分组出错:', error);
      }
    },
    
    // 确认删除
    confirmDelete(group) {
      this.deletingGroup = group;
      this.showDeleteModal = true;
    },
    
    // 删除分组
    async deleteGroup() {
      try {
        const response = await groupAPI.deleteGroup(this.deletingGroup.id);
        if (response.success) {
          // 发射事件通知父组件
          this.$emit('group-changed');
          
          this.showDeleteModal = false;
          await this.loadGroups();
        } else {
          alert(`删除分组失败: ${response.error}`);
        }
      } catch (error) {
        console.error('删除分组出错:', error);
      }
    }
  }
};
</script>

<style scoped>
.group-manager {
  padding: 20px;
}

h2 {
  margin-bottom: 20px;
}

.group-form, .group-list {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

input[type="text"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.color-presets {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 10px;
}

.color-option {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  border: 2px solid transparent;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: relative;
}

.color-option:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.color-option.active {
  border-color: #333;
  box-shadow: 0 0 0 2px rgba(255,255,255,0.8), 0 4px 8px rgba(0,0,0,0.2);
}

.check-icon {
  color: white;
  font-weight: bold;
  text-shadow: 0 1px 2px rgba(0,0,0,0.3);
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-danger {
  background-color: #e74c3c;
  color: white;
}

.group-item {
  border: 1px solid #eee;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 10px;
}

.group-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.group-color {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  margin-right: 10px;
}

.todo-count {
  margin-left: auto;
  color: #777;
  font-size: 0.9em;
}

.group-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn-edit, .btn-delete {
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-edit {
  background-color: #f39c12;
  color: white;
}

.btn-delete {
  background-color: #e74c3c;
  color: white;
}

/* 模态框样式 */
.modal {
  position: fixed;
  z-index: 999;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  position: relative;
}

.close {
  position: absolute;
  right: 15px;
  top: 10px;
  font-size: 24px;
  cursor: pointer;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 15px;
}

ul {
  list-style-type: none;
  padding: 0;
}
</style> 