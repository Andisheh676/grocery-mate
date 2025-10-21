import { createRouter, createWebHistory } from 'vue-router'
import { isAuthenticated, isAdmin } from '../stores/auth'
import Dashboard from '../views/Dashboard.vue'
import Ingredients from '../views/Ingredients.vue'
import ShoppingLists from '../views/ShoppingLists.vue'
import Recipes from '../views/Recipes.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import UserManagement from '../views/admin/UserManagement.vue'
import NewsList from '../views/news/NewsList.vue'

const routes = [
  { path: '/login', name: 'login', component: Login, meta: { requiresAuth: false } },
  { path: '/register', name: 'register', component: Register, meta: { requiresAuth: false } },
  { path: '/', name: 'dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/ingredients', name: 'ingredients', component: Ingredients, meta: { requiresAuth: true } },
  { path: '/shopping', name: 'shopping', component: ShoppingLists, meta: { requiresAuth: true } },
  { path: '/recipes', name: 'recipes', component: Recipes, meta: { requiresAuth: true } },
  { path: '/admin/users', name: 'user-management', component: UserManagement, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/news', name: 'news', component: NewsList, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !isAuthenticated.value) {
    next('/login')
  } else if (to.meta.requiresAdmin && !isAdmin.value) {
    alert("Access denied. Admin only.")
    next('/')
  } else if ((to.path === '/login' || to.path === '/register') && isAuthenticated.value) {
    next('/')
  } else {
    next()
  }
})

export default router
