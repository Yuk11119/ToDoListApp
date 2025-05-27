<template>
  <div class="about">
    <div class="container">
      <div class="card">
        <h2>关于本应用</h2>
        <p>这是一个使用Vue.js和Flask构建的Todo应用，用于管理您的日常任务。</p>
        
        <h3>技术栈</h3>
        <ul>
          <li><strong>前端:</strong> Vue.js 3, Vue Router, Axios</li>
          <li><strong>后端:</strong> Flask, Flask-SQLAlchemy, Flask-CORS</li>
          <li><strong>数据库:</strong> SQLite</li>
        </ul>
        
        <h3>功能</h3>
        <ul>
          <li>创建、查看、编辑和删除任务</li>
          <li>标记任务为已完成/未完成</li>
          <li>查看任务详情</li>
        </ul>
        
        <div class="actions">
          <button @click="$router.push('/')">返回首页</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.about {
  padding: 20px 0;
}

h2 {
  color: #3498db;
  margin-bottom: 20px;
}

h3 {
  color: #3498db;
  margin: 20px 0 10px;
}

p {
  margin-bottom: 15px;
  line-height: 1.5;
}

ul {
  margin-bottom: 20px;
  padding-left: 20px;
}

li {
  margin-bottom: 8px;
}

.actions {
  margin-top: 30px;
}
</style> 