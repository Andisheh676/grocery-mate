<template>
  <div class="min-h-screen bg-white">
    <!-- Hero Section -->
    <div class="relative bg-gradient-to-r from-primary-600 to-primary-800">
      <div class="max-w-7xl mx-auto py-24 px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-4xl font-extrabold text-white sm:text-5xl md:text-6xl">
            🥗 GroceryMate
          </h1>
          <p class="mt-3 max-w-md mx-auto text-base text-primary-100 sm:text-lg md:mt-5 md:text-xl">
            Your smart companion for grocery management, meal planning, and healthy eating
          </p>
          <div class="mt-10 flex justify-center gap-4">
            <router-link
              to="/register"
              class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md bg-white text-primary-700 hover:bg-gray-100"
            >
              Get Started
            </router-link>
            <router-link
              to="/login"
              class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md bg-primary-700 text-white hover:bg-primary-800"
            >
              Sign In
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="py-16 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h2 class="text-3xl font-extrabold text-gray-900">
            Everything you need to manage your groceries
          </h2>
        </div>
        <div class="mt-12 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          <div class="bg-white p-6 rounded-lg shadow">
            <div class="text-4xl mb-4">📦</div>
            <h3 class="text-lg font-medium text-gray-900 mb-2">Inventory Management</h3>
            <p class="text-gray-600">Track what's in your fridge and pantry. Never forget what you have at home.</p>
          </div>
          <div class="bg-white p-6 rounded-lg shadow">
            <div class="text-4xl mb-4">🛒</div>
            <h3 class="text-lg font-medium text-gray-900 mb-2">Shopping Lists</h3>
            <p class="text-gray-600">Create and manage shopping lists. Check off items as you shop.</p>
          </div>
          <div class="bg-white p-6 rounded-lg shadow">
            <div class="text-4xl mb-4">🍳</div>
            <h3 class="text-lg font-medium text-gray-900 mb-2">Recipe Suggestions</h3>
            <p class="text-gray-600">Get healthy recipe ideas based on ingredients you already have.</p>
          </div>
          <div class="bg-white p-6 rounded-lg shadow">
            <div class="text-4xl mb-4">⏰</div>
            <h3 class="text-lg font-medium text-gray-900 mb-2">Expiration Tracking</h3>
            <p class="text-gray-600">Receive alerts when items are about to expire. Reduce food waste.</p>
          </div>
          <div class="bg-white p-6 rounded-lg shadow">
            <div class="text-4xl mb-4">💚</div>
            <h3 class="text-lg font-medium text-gray-900 mb-2">Healthy Eating</h3>
            <p class="text-gray-600">Focus on nutritious meals with calorie and nutrition information.</p>
          </div>
          <div class="bg-white p-6 rounded-lg shadow">
            <div class="text-4xl mb-4">📱</div>
            <h3 class="text-lg font-medium text-gray-900 mb-2">Mobile Friendly</h3>
            <p class="text-gray-600">Access your lists anywhere, anytime, from any device.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- News Section -->
    <div class="py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-extrabold text-gray-900 text-center mb-12">
          Latest News & Updates
        </h2>
        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
        <div v-else class="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
          <div
            v-for="article in news"
            :key="article.id"
            class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow cursor-pointer"
            @click="viewArticle(article)"
          >
            <img
              v-if="article.image_url"
              :src="article.image_url"
              :alt="article.title"
              class="w-full h-48 object-cover"
            />
            <div class="p-6">
              <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ article.title }}</h3>
              <p class="text-gray-600 mb-4">{{ article.summary }}</p>
              <div class="text-sm text-gray-500">{{ formatDate(article.published_at) }}</div>
            </div>
          </div>
        </div>
        <div v-if="!loading && news.length === 0" class="text-center py-12">
          <p class="text-gray-500">No news articles available at this time.</p>
        </div>
      </div>
    </div>

    <!-- CTA Section -->
    <div class="bg-primary-700">
      <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:py-16 lg:px-8 lg:flex lg:items-center lg:justify-between">
        <h2 class="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
          <span class="block">Ready to get started?</span>
          <span class="block text-primary-200">Create your free account today.</span>
        </h2>
        <div class="mt-8 flex lg:mt-0 lg:flex-shrink-0">
          <div class="inline-flex rounded-md shadow">
            <router-link
              to="/register"
              class="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md bg-white text-primary-700 hover:bg-gray-100"
            >
              Get started
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="bg-gray-800">
      <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 class="text-white text-lg font-semibold mb-4">GroceryMate</h3>
            <p class="text-gray-400">Your smart companion for grocery management and healthy eating.</p>
          </div>
          <div>
            <h3 class="text-white text-lg font-semibold mb-4">Links</h3>
            <ul class="space-y-2">
              <li><router-link to="/privacy" class="text-gray-400 hover:text-white">Privacy Policy</router-link></li>
              <li><router-link to="/login" class="text-gray-400 hover:text-white">Sign In</router-link></li>
              <li><router-link to="/register" class="text-gray-400 hover:text-white">Register</router-link></li>
            </ul>
          </div>
          <div>
            <h3 class="text-white text-lg font-semibold mb-4">Contact</h3>
            <p class="text-gray-400">support@grocerymate.com</p>
          </div>
        </div>
        <div class="mt-8 border-t border-gray-700 pt-8 text-center text-gray-400">
          <p>&copy; 2025 GroceryMate. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const news = ref([])
const loading = ref(true)
const API_URL = 'http://localhost:8000'

const loadNews = async () => {
  try {
    const response = await axios.get(`${API_URL}/news/public`)
    news.value = response.data
  } catch (error) {
    console.error('Error loading news:', error)
  } finally {
    loading.value = false
  }
}

const viewArticle = (article) => {
  router.push(`/news/${article.slug}`)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  loadNews()
})
</script>
