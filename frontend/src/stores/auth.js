// stores/auth.js
import { ref, computed } from 'vue'
import axios from 'axios'
import qs from 'qs'

// ---------- API URL ----------
const API_URL = import.meta.env.VITE_API_URL  // از فایل .env

// ---------- State ----------
const user = ref(null)
export const token = ref(localStorage.getItem('token') || '')
export const isAuthenticated = ref(!!token.value)
export const isAdmin = computed(() => user.value?.is_admin ?? false)

// ---------- Axios Instance ----------
const api = axios.create({
  baseURL: API_URL,
  withCredentials: true  // ← اجباری برای کوکی و header ها
})

// ---------- Axios Interceptor ----------
api.interceptors.request.use(config => {
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

export function logout() {
  token.value = null
  user.value = null
  isAuthenticated.value = false
  localStorage.removeItem('token')
}

// ---------- Actions ----------
export async function login(email, password) {
  try {
    const formData = qs.stringify({
      grant_type: 'password',
      username: email,
      password: password
    })

    const response = await api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })

    saveToken(response.data.access_token)
    await fetchCurrentUser()
    return true
  } catch (error) {
    console.error('Login failed:', error)
    alert('Login failed: check your credentials or server CORS')
    return false
  }
}

export async function fetchCurrentUser() {
  try {
    const response = await api.get('/auth/me')
    user.value = response.data
  } catch (error) {
    console.error('Failed to fetch user:', error)
    alert('Session expired, please login again.')
    logout()
  }
}

export async function register(email, username, password) {
  try {
    await api.post('/auth/register', { email, username, password })
    return await login(email, password)
  } catch (error) {
    console.error('Registration failed:', error)
    throw error
  }
}

// ---------- Getters ----------
export function getUser() {
  return user.value
}

export default api
