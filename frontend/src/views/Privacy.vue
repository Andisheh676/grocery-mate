<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-4xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div class="bg-white shadow overflow-hidden sm:rounded-lg">
        <!-- Header -->
        <div class="px-4 py-5 sm:px-6">
          <h1 class="text-3xl font-bold text-gray-900">{{ pageContent.title }}</h1>
          <p class="mt-1 text-sm text-gray-500">
            Last updated: {{ formatDate(pageContent.updated_at) }}
          </p>
        </div>
        <!-- Content -->
        <div class="border-t border-gray-200 px-4 py-5 sm:px-6">
          <div class="prose max-w-none" v-html="pageContent.content"></div>
        </div>
      </div>

      <!-- Back link -->
      <div class="mt-8 text-center">
        <router-link to="/" class="text-primary-600 hover:text-primary-800">
          &larr; Back to Home
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_URL = 'http://91.99.23.49:8000'

const pageContent = ref({
  title: 'Privacy Policy',
  content: 'Loading...',
  updated_at: new Date()
})

const loadPageContent = async () => {
  try {
    const response = await axios.get(`${API_URL}/pages/public/privacy`)
    pageContent.value = response.data
  } catch (error) {
    console.error('Error loading page:', error)
    pageContent.value.content = 'Failed to load content.'
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'Not specified'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  loadPageContent()
})
</script>

<style scoped>
.prose {
  color: #374151;
  line-height: 1.75;
}
.prose h2 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-top: 2rem;
  margin-bottom: 1rem;
}
.prose h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}
.prose p {
  margin-bottom: 1rem;
}
.prose ul, .prose ol {
  margin-left: 1.5rem;
  margin-bottom: 1rem;
}
.prose li {
  margin-bottom: 0.5rem;
}
</style>
