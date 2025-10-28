<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-3xl font-bold text-gray-900">Recipes</h2>
      <div class="flex space-x-3">
        <button
          @click="findMatchingRecipes"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700"
        >
          🔍 Find Recipes with Available Ingredients
        </button>
        <button
          @click="seedSampleRecipes"
          class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
        >
          📚 Load Sample Recipes
        </button>
      </div>
    </div>

    <!-- Filter -->
    <div class="mb-6">
      <button
        @click="showHealthyOnly = !showHealthyOnly"
        :class="showHealthyOnly ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
        class="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium"
      >
        {{ showHealthyOnly ? '✓' : '' }} Healthy Recipes Only
      </button>
    </div>

    <!-- Matching Recipes Alert -->
    <div v-if="showMatchingOnly" class="bg-green-50 border-l-4 border-green-400 p-4 mb-6">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <p class="text-sm text-green-700">
            Showing recipes you can make with your available ingredients! 
            <button @click="showMatchingOnly = false" class="font-medium underline">Show all recipes</button>
          </p>
        </div>
      </div>
    </div>

    <!-- Recipes Grid -->
    <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <div v-for="recipe in displayedRecipes" :key="recipe.id" class="bg-white overflow-hidden shadow rounded-lg hover:shadow-xl transition-shadow">
        <div class="p-6">
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-xl font-semibold text-gray-900">{{ recipe.name }}</h3>
            <span v-if="recipe.is_healthy" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
              Healthy
            </span>
          </div>
          
          <p class="text-gray-600 text-sm mb-4">{{ recipe.description }}</p>
          
          <div class="space-y-2 mb-4">
            <div class="flex items-center text-sm text-gray-500">
              ⏱️ Prep time: {{ recipe.prep_time }} min
            </div>
            <div class="flex items-center text-sm text-gray-500">
              👥 Servings: {{ recipe.servings }}
            </div>
            <div v-if="recipe.calories" class="flex items-center text-sm text-gray-500">
              🔥 Calories: {{ recipe.calories }}
            </div>
          </div>

          <button
            @click="viewRecipe(recipe)"
            class="w-full mt-4 inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
          >
            View Recipe
          </button>
        </div>
      </div>
    </div>

    <div v-if="displayedRecipes.length === 0" class="text-center py-12 bg-white rounded-lg shadow">
      <p class="text-gray-500">No recipes found. Try loading sample recipes or adjust your filters!</p>
    </div>

    <!-- Recipe Detail Modal -->
    <div v-if="selectedRecipe" class="fixed z-10 inset-0 overflow-y-auto">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="flex justify-between items-start mb-4">
              <div>
                <h3 class="text-2xl font-bold text-gray-900">{{ selectedRecipe.name }}</h3>
                <p class="text-gray-600 mt-2">{{ selectedRecipe.description }}</p>
              </div>
              <button @click="selectedRecipe = null" class="text-gray-400 hover:text-gray-500">✖️</button>
            </div>

            <div class="mb-6">
              <h4 class="text-lg font-semibold text-gray-900 mb-2">Ingredients</h4>
              <ul class="list-disc list-inside space-y-1">
                <li v-for="(ingredient, index) in parseIngredients(selectedRecipe.ingredients)" :key="index" class="text-gray-700">
                  {{ ingredient }}
                </li>
              </ul>
            </div>

            <div>
              <h4 class="text-lg font-semibold text-gray-900 mb-2">Instructions</h4>
              <div class="text-gray-700 whitespace-pre-line">{{ selectedRecipe.instructions }}</div>
            </div>

            <div class="mt-6 pt-4 border-t border-gray-200 flex items-center justify-between text-sm text-gray-500">
              <span>⏱️ {{ selectedRecipe.prep_time }} min</span>
              <span>👥 {{ selectedRecipe.servings }} servings</span>
              <span v-if="selectedRecipe.calories">🔥 {{ selectedRecipe.calories }} cal</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { recipesAPI } from '../services/api.js'

const API_BASE = 'http://91.99.23.49:8000'

const recipes = ref([])
const matchingRecipes = ref([])
const showHealthyOnly = ref(false)
const showMatchingOnly = ref(false)
const selectedRecipe = ref(null)
const userIngredients = ref([])

const displayedRecipes = computed(() => {
  let filtered = showMatchingOnly.value ? matchingRecipes.value : recipes.value
  if (showHealthyOnly.value) filtered = filtered.filter(r => r.is_healthy)
  return filtered
})

const loadRecipes = async () => {
  try {
    const response = await recipesAPI.getAll()
    recipes.value = response.data

    // ساخت لیست مواد اولیه موجود کاربر
    userIngredients.value = []
    response.data.forEach(r => {
      try {
        const ingList = JSON.parse(r.ingredients)
        ingList.forEach(i => {
          if (!userIngredients.value.includes(i)) userIngredients.value.push(i)
        })
      } catch {}
    })
  } catch (error) {
    console.error('Error loading recipes:', error)
  }
}

const findMatchingRecipes = async () => {
  try {
    if (userIngredients.value.length === 0) {
      alert('No ingredients available to match recipes!')
      return
    }

    // مطمئن شویم همه عناصر رشته‌ای هستند
    const ingredientsStr = userIngredients.value.map(i => i.toString())

    // تبدیل آرایه به query string
    const params = new URLSearchParams()
    ingredientsStr.forEach(ing => params.append('ingredients', ing))

    console.log('Requesting:', `${API_BASE}/recipes/match/ingredients?${params.toString()}`)

    const response = await axios.get(`${API_BASE}/recipes/match/ingredients?${params.toString()}`)
    matchingRecipes.value = response.data
    showMatchingOnly.value = true

    if (matchingRecipes.value.length === 0) {
      alert('No matching recipes found!')
    }
  } catch (error) {
    console.error('Error finding matching recipes:', error)
    if (error.response) {
      console.error('Server response:', error.response.status, error.response.data)
      alert(`Server error: ${error.response.status}`)
    } else {
      alert('Network error. Check server connection.')
    }
  }
}

const seedSampleRecipes = async () => {
  try {
    await recipesAPI.seedSample()
    await loadRecipes()
    alert('Sample recipes loaded successfully!')
  } catch (error) {
    console.error('Error seeding recipes:', error)
  }
}

const viewRecipe = (recipe) => {
  selectedRecipe.value = recipe
}

const parseIngredients = (ingredientsString) => {
  try {
    return JSON.parse(ingredientsString)
  } catch {
    return []
  }
}

onMounted(() => {
  loadRecipes()
})
</script>
