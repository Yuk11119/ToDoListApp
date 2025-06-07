import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CalendarView from '../views/CalendarView.vue'
import TimeBlockView from '../views/TimeBlockView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/calendar',
    name: 'calendar',
    component: CalendarView
  },
  {
    path: '/timeblocks',
    name: 'timeblocks',
    component: TimeBlockView
  }
]

const router = createRouter({
  history: createWebHistory('/'),
  routes
})

export default router 