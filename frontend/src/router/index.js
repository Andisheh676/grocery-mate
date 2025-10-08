import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Ingredients from '../views/Ingredients.vue'
import ShoppingLists from '../views/ShoppingLists.vue'
import Recipes from '../views/Recipes.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: Dashboard
    },
    {
      path: '/ingredients',
      name: 'ingredients',
      component: Ingredients
    },
    {
      path: '/shopping',
      name: 'shopping',
      component: ShoppingLists
    },
    {
      path: '/recipes',
      name: 'recipes',
      component: Recipes
    }
  ]
})

export default router
