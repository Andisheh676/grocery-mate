<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <nav v-if="isAuthenticated" class="bg-white shadow-lg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <!-- Logo -->
          <div class="flex-shrink-0 flex items-center">
            <h1 class="text-2xl font-bold text-primary-600">🥗 GroceryMate</h1>
          </div>

          <!-- Links -->
          <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
            <router-link
              to="/"
              class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              :class="$route.path === '/' ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
            >Dashboard</router-link>

            <router-link
              to="/ingredients"
              class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              :class="$route.path === '/ingredients' ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
            >Ingredients</router-link>

            <router-link
              to="/shopping"
              class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              :class="$route.path === '/shopping' ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
            >Shopping Lists</router-link>

            <router-link
              to="/recipes"
              class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              :class="$route.path === '/recipes' ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
            >Recipes</router-link>

            <!-- Admin Link -->
            <router-link
              v-if="user?.is_admin"
              to="/admin/users"
              class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              :class="$route.path === '/admin/users' ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
            >Admin</router-link>
          </div>

          <!-- Logout / User -->
          <div class="flex items-center">
            <span class="text-sm text-gray-700 mr-4">{{ user?.username }}</span>
            <button @click="handleLogout"
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md bg-red-500 text-white hover:bg-red-600"
            >Logout</button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { isAuthenticated, getUser, fetchCurrentUser, logout } from './stores/auth'

const router = useRouter()
const user = computed(() => getUser())

// Fetch user on app load
onMounted(async () => {
  if (isAuthenticated.value) {
    await fetchCurrentUser()
  }
})

const handleLogout = () => {
  logout()
  router.push('/login')
}
</script>
