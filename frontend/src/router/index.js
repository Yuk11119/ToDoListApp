import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import TodoDetailView from '../views/TodoDetailView.vue'
import GroupsView from '../views/GroupsView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/todo/:id',
    name: 'todoDetail',
    component: TodoDetailView,
    props: true
  },
  {
    path: '/groups',
    name: 'groups',
    component: GroupsView
  },
  {
    path: '/about',
    name: 'about',
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHistory('/'),
  routes
})

export default router 