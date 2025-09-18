import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import App from './App.vue'
import Home from './views/Home.vue'
import ToolDetail from './views/ToolDetail.vue'

// 创建路由
const routes = [
  { path: '/', component: Home },
  { path: '/tool/:id', component: ToolDetail, props: true }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 创建Vue应用
const app = createApp(App)
app.use(ElementPlus)
app.use(router)

app.mount('#app')