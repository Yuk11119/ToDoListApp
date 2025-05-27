<template>
  <div class="groups-view">
    <div class="app-layout">
      <!-- 侧边栏 -->
      <SideBar 
        @filter-selected="handleFilterSelected" 
        ref="sidebar"
      />
      
      <!-- 主内容区域 -->
      <div class="main-content">
        <h1>分组管理</h1>
        <group-manager @group-changed="refreshSidebar" />
      </div>
    </div>
  </div>
</template>

<script>
import GroupManager from '@/components/GroupManager.vue';
import SideBar from '@/components/SideBar.vue';

export default {
  name: 'GroupsView',
  components: {
    GroupManager,
    SideBar
  },
  methods: {
    handleFilterSelected(filter) {
      // 在分组管理页面，可以选择跳转回首页并应用筛选
      this.$router.push('/');
    },
    refreshSidebar() {
      // 当分组变更时，刷新侧边栏
      if (this.$refs.sidebar) {
        this.$refs.sidebar.loadGroups();
      }
    }
  }
}
</script>

<style scoped>
.groups-view {
  height: 100%;
}

.app-layout {
  display: flex;
  height: 100%;
  overflow: hidden;
}

.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

h1 {
  margin-bottom: 30px;
  color: #34495e;
  text-align: center;
}
</style> 