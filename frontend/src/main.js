import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/main.css'

const app = createApp(App)

app.use(router)
app.mount('#app') 

if (import.meta.env.DEV) {
  import('@stagewise/toolbar-vue').then(({ StagewiseToolbar }) => {
    const stagewiseConfig = {
      plugins: []
    }
    
    const toolbarContainer = document.createElement('div')
    toolbarContainer.id = 'stagewise-container'
    document.body.appendChild(toolbarContainer)
    
    const toolbarApp = createApp(StagewiseToolbar, { config: stagewiseConfig })
    toolbarApp.mount('#stagewise-container')
  })
} 