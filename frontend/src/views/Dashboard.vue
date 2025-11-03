<template>
  <div class="relative min-h-screen px-8 py-10 bg-gradient-to-b from-gray-50 to-gray-100">
    <!-- Background Image -->
    <div 
      class="absolute inset-0 bg-center bg-cover opacity-10"
      style="background-image: url('https://images.unsplash.com/photo-1600891964599-f61ba0e24092?auto=format&fit=crop&w=1470&q=80');"
    ></div>

    <!-- Content Overlay -->
    <div class="relative z-10">
      <h1 class="text-4xl sm:text-5xl font-extrabold text-gray-900 mb-10 drop-shadow-md">🥗 GroceryMate Dashboard</h1>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
        <div class="bg-gradient-to-r from-green-400 to-green-600 text-white shadow-xl rounded-2xl p-6 hover:scale-105 transform transition-all duration-300">
          <div class="flex items-center space-x-4">
            <div class="text-5xl sm:text-6xl">🥬</div>
            <div>
              <p class="text-xs sm:text-sm font-medium uppercase tracking-wide">Total Ingredients</p>
              <p class="text-3xl sm:text-4xl font-bold">{{ stats.totalIngredients }}</p>
            </div>
          </div>
        </div>

        <div class="bg-gradient-to-r from-blue-400 to-blue-600 text-white shadow-xl rounded-2xl p-6 hover:scale-105 transform transition-all duration-300">
          <div class="flex items-center space-x-4">
            <div class="text-5xl sm:text-6xl">❄️</div>
            <div>
              <p class="text-xs sm:text-sm font-medium uppercase tracking-wide">In Fridge</p>
              <p class="text-3xl sm:text-4xl font-bold">{{ stats.fridgeItems }}</p>
            </div>
          </div>
        </div>

        <div class="bg-gradient-to-r from-yellow-400 to-yellow-600 text-white shadow-xl rounded-2xl p-6 hover:scale-105 transform transition-all duration-300">
          <div class="flex items-center space-x-4">
            <div class="text-5xl sm:text-6xl">🗄️</div>
            <div>
              <p class="text-xs sm:text-sm font-medium uppercase tracking-wide">In Pantry</p>
              <p class="text-3xl sm:text-4xl font-bold">{{ stats.pantryItems }}</p>
            </div>
          </div>
        </div>

        <div class="bg-gradient-to-r from-red-400 to-red-600 text-white shadow-xl rounded-2xl p-6 hover:scale-105 transform transition-all duration-300">
          <div class="flex items-center space-x-4">
            <div class="text-5xl sm:text-6xl">⚠️</div>
            <div>
              <p class="text-xs sm:text-sm font-medium uppercase tracking-wide">Expiring Soon</p>
              <p class="text-3xl sm:text-4xl font-bold">{{ stats.expiringSoon }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Expiring Items Alert -->
      <div v-if="expiringItems.length > 0" class="bg-red-50 border-l-8 border-red-500 p-6 rounded-2xl shadow-md mb-12 animate-fade-in">
        <div class="flex items-start space-x-4">
          <div class="text-3xl sm:text-4xl animate-pulse">⚠️</div>
          <div>
            <h2 class="text-xl sm:text-2xl font-bold text-red-700 mb-3 drop-shadow-sm">Items Expiring Soon</h2>
            <ul class="list-disc list-inside space-y-1 text-red-800">
              <li v-for="item in expiringItems" :key="item.id">
                <span class="font-semibold">{{ item.name }}</span> - Expires: {{ formatDate(item.expiry_date) }}
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <router-link
          to="/ingredients"
          class="bg-green-500 hover:bg-green-600 text-white rounded-2xl shadow-lg py-4 sm:py-5 flex justify-center items-center space-x-3 transition-all duration-300 transform hover:scale-105 hover:shadow-2xl"
        >
          <span class="text-2xl sm:text-3xl">➕</span>
          <span class="text-base sm:text-lg font-semibold">Add Ingredient</span>
        </router-link>

        <router-link
          to="/shopping"
          class="bg-blue-500 hover:bg-blue-600 text-white rounded-2xl shadow-lg py-4 sm:py-5 flex justify-center items-center space-x-3 transition-all duration-300 transform hover:scale-105 hover:shadow-2xl"
        >
          <span class="text-2xl sm:text-3xl">🛒</span>
          <span class="text-base sm:text-lg font-semibold">Create Shopping List</span>
        </router-link>

        <router-link
          to="/recipes"
          class="bg-purple-500 hover:bg-purple-600 text-white rounded-2xl shadow-lg py-4 sm:py-5 flex justify-center items-center space-x-3 transition-all duration-300 transform hover:scale-105 hover:shadow-2xl"
        >
          <span class="text-2xl sm:text-3xl">🍽️</span>
          <span class="text-base sm:text-lg font-semibold">Find Recipes</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ingredientsAPI } from '../services/api.js'

const stats = ref({
  totalIngredients: 0,
  fridgeItems: 0,
  pantryItems: 0,
  expiringSoon: 0
})

const expiringItems = ref([])

const loadDashboard = async () => {
  try {
    const [allItems, fridgeItems, pantryItems, expiring] = await Promise.all([
      ingredientsAPI.getAll(),
      ingredientsAPI.getAll('Fridge'),
      ingredientsAPI.getAll('Pantry'),
      ingredientsAPI.getExpiringSoon(7)
    ])

    stats.value = {
      totalIngredients: allItems.data.length,
      fridgeItems: fridgeItems.data.length,
      pantryItems: pantryItems.data.length,
      expiringSoon: expiring.data.length
    }

    expiringItems.value = expiring.data
  } catch (error) {
    console.error('Error loading dashboard:', error)
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

onMounted(() => {
  loadDashboard()
})
</script>

<style>
@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fade-in 0.5s ease-out forwards;
}
</style>
