// stores/auth.js
import { ref, computed } from 'vue'
import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000'

// ---------- State ----------
const user = ref(null)
export const token = ref(localStorage.getItem('token') || '')
export const isAuthenticated = ref(!!token.value)
export const isAdmin = computed(() => user.value?.is_admin ?? false)

// ---------- Axios Interceptor ----------
axios.interceptors.request.use(config => {
  if (token.value) {
    config.headers.Authorization = `Bearer ${token.value}`
  }
  return config
})

// ---------- Token Management ----------
export const saveToken = (newToken) => {
  token.value = newToken
  isAuthenticated.value = true
  localStorage.setItem('token', newToken)
}

export const getToken = () => token.value

// ---------- Actions ----------
export async function login(email, password) {
  try {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)

    const response = await axios.post(`${API_URL}/auth/login`, formData)
    saveToken(response.data.access_token)

    await fetchCurrentUser()
    return true
  } catch (error) {
    console.error('Login failed:', error)
    return false
  }
}

export async function register(email, username, password) {
  try {
    await axios.post(`${API_URL}/auth/register`, { email, username, password })
    return await login(email, password)
  } catch (error) {
    console.error('Registration failed:', error)
    throw error
  }
}

export async function fetchCurrentUser() {
  try {
    const response = await axios.get(`${API_URL}/auth/me`)
    user.value = response.data
  } catch (error) {
    console.error('Failed to fetch user:', error)
    alert('Session expired, please login again.')
    logout()
  }
}

export function logout() {
  token.value = null
  user.value = null
  isAuthenticated.value = false
  localStorage.removeItem('token')
}

// ---------- Getters ----------
export function getUser() {
  return user.value
}
