<template>
  <div class="app">
    <header class="navbar">
      <div class="navbar-brand">
        <router-link to="/">
          Todo 应用
        </router-link>
      </div>
    </header>
    
    <main class="main-container">
      <router-view />
    </main>
    
    <footer>
      <p>© {{ new Date().getFullYear() }} Todo 应用 | 使用 Vue.js 和 Flask 构建</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
:root {
  --primary-color: #3498db;
  --secondary-color: #2ecc71;
  --background-color: #f8f9fa;
  --text-color: #333;
  --light-gray: #ddd;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Arial', sans-serif;
  line-height: 1.6;
  color: var(--text-color);
  background-color: var(--background-color);
  height: 100vh;
  margin: 0;
}

html {
  height: 100%;
}

.app {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 2rem;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.navbar-brand a {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary-color);
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-links a {
  color: var(--text-color);
  text-decoration: none;
  padding: 0.5rem 0;
  position: relative;
}

.nav-links a:hover {
  color: var(--primary-color);
}

.nav-links a.router-link-active {
  color: var(--primary-color);
  font-weight: bold;
}

.nav-links a.router-link-active:after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: var(--primary-color);
}

.main-container {
  flex: 1;
  overflow: hidden; /* 确保内容不会溢出 */
}

footer {
  padding: 1rem;
  text-align: center;
  background-color: white;
  border-top: 1px solid var(--light-gray);
  font-size: 0.9rem;
  color: #666;
}

button {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #2980b9;
}

button.danger {
  background-color: #e74c3c;
}

button.danger:hover {
  background-color: #c0392b;
}

h1, h2, h3 {
  margin-bottom: 1rem;
}
</style> 