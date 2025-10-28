<template>
  <div class="px-4 py-6">
    <!-- Loading -->
    <div v-if="loading" class="text-center py-10 text-gray-600">Loading admin data...</div>

    <!-- Error -->
    <div v-else-if="error" class="text-center py-10 text-red-600">{{ error }}</div>

    <!-- Main Content -->
    <div v-else>
      <!-- Header -->
      <div class="mb-6">
        <h2 class="text-3xl font-bold text-gray-900">User Management</h2>
        <p class="text-gray-600">Manage all users and their permissions</p>
      </div>

      <!-- Statistics Cards -->
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        <div
          class="bg-white overflow-hidden shadow rounded-lg"
          v-for="(value, key) in stats"
          :key="key"
        >
          <div class="p-5">
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">{{ formatStatTitle(key) }}</dt>
                <dd class="text-2xl font-semibold text-gray-900">{{ value }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <!-- Users Table -->
      <div class="bg-white shadow overflow-hidden sm:rounded-lg">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Joined</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Last Login</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="user in users" :key="user.id">
              <td class="px-6 py-4 whitespace-nowrap">
                <div>
                  <div class="text-sm font-medium text-gray-900">{{ user.username }}</div>
                  <div class="text-sm text-gray-500">{{ user.email }}</div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span v-if="user.is_active" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">Active</span>
                <span v-else class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">Inactive</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span v-if="user.is_admin" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-purple-100 text-purple-800">Admin</span>
                <span v-else class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800">User</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(user.created_at) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ user.last_login ? formatDate(user.last_login) : 'Never' }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button @click="toggleUserStatus(user)" class="text-indigo-600 hover:text-indigo-900 mr-3">{{ user.is_active ? 'Deactivate' : 'Activate' }}</button>
                <button @click="toggleAdminStatus(user)" class="text-purple-600 hover:text-purple-900 mr-3">{{ user.is_admin ? 'Remove Admin' : 'Make Admin' }}</button>
                <button @click="confirmDelete(user)" class="text-red-600 hover:text-red-900">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { getToken, isAdmin, fetchCurrentUser } from '../../stores/auth'

const users = ref([])
const stats = ref({
  total_users: 0,
  active_users: 0,
  admin_users: 0,
  new_users_this_month: 0
})
const loading = ref(true)
const error = ref(null)

const API_URL = 'http://91.99.23.49:8000'

const loadUsers = async () => {
  try {
    const response = await axios.get(`${API_URL}/admin/users`, {
      headers: { Authorization: `Bearer ${getToken()}` }
    })
    users.value = response.data
  } catch (err) {
    console.error('Error loading users:', err)
    error.value = 'Failed to load users.'
  }
}

const loadStats = async () => {
  try {
    const response = await axios.get(`${API_URL}/admin/users/stats`, {
      headers: { Authorization: `Bearer ${getToken()}` }
    })
    stats.value = response.data
  } catch (err) {
    console.error('Error loading stats:', err)
    error.value = 'Failed to load stats.'
  }
}

const toggleUserStatus = async (user) => {
  try {
    await axios.patch(`${API_URL}/admin/users/${user.id}`, { is_active: !user.is_active }, { headers: { Authorization: `Bearer ${getToken()}` } })
    await loadUsers()
    await loadStats()
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to update user')
  }
}

const toggleAdminStatus = async (user) => {
  try {
    await axios.patch(`${API_URL}/admin/users/${user.id}`, { is_admin: !user.is_admin }, { headers: { Authorization: `Bearer ${getToken()}` } })
    await loadUsers()
    await loadStats()
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to update user')
  }
}

const confirmDelete = async (user) => {
  if (!confirm(`Are you sure you want to delete ${user.username}? This cannot be undone.`)) return
  try {
    await axios.delete(`${API_URL}/admin/users/${user.id}`, { headers: { Authorization: `Bearer ${getToken()}` } })
    await loadUsers()
    await loadStats()
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to delete user')
  }
}

const formatDate = (dateString) => new Date(dateString).toLocaleDateString()

const formatStatTitle = (key) => {
  switch (key) {
    case 'total_users': return 'Total Users'
    case 'active_users': return 'Active Users'
    case 'admin_users': return 'Admins'
    case 'new_users_this_month': return 'New This Month'
    default: return key
  }
}

onMounted(async () => {
  loading.value = true
  error.value = null
  try {
    await fetchCurrentUser()
    if (!isAdmin.value) {
      error.value = 'Access denied. Admins only.'
      return
    }
    await loadUsers()
    await loadStats()
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load admin data.'
  } finally {
    loading.value = false
  }
})
</script>
