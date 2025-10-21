import axios from 'axios'
import { getToken } from '../stores/auth'

const API_URL = import.meta.env.VITE_API_URL  // آدرس API را از متغیر محیطی می‌گیرد

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to all requests
api.interceptors.request.use((config) => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle 401 errors (redirect to login)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Ingredients API
export const ingredientsAPI = {
  getAll: (location = null) => {
    const params = location ? { location } : {}
    return api.get('/ingredients/', { params })
  },
  getById: (id) => api.get(`/ingredients/${id}`),
  create: (data) => api.post('/ingredients/', data),
  update: (id, data) => api.put(`/ingredients/${id}`, data),
  delete: (id) => api.delete(`/ingredients/${id}`),
  getExpiringSoon: (days = 7) =>
    api.get('/ingredients/expiring/soon', { params: { days } }),
}

// Shopping Lists API
export const shoppingListsAPI = {
  getAll: () => api.get('/shopping-lists/'),
  getById: (id) => api.get(`/shopping-lists/${id}`),
  create: (data) => api.post('/shopping-lists/', data),
  delete: (id) => api.delete(`/shopping-lists/${id}`),
  addItem: (listId, item) => api.post(`/shopping-lists/${listId}/items`, item),
  updateItem: (itemId, isPurchased) =>
    api.put(`/shopping-lists/items/${itemId}`, null, {
      params: { is_purchased: isPurchased },
    }),
  deleteItem: (itemId) => api.delete(`/shopping-lists/items/${itemId}`),
}

// Recipes API
export const recipesAPI = {
  getAll: (healthyOnly = false) =>
    api.get('/recipes/', { params: { healthy_only: healthyOnly } }),
  getById: (id) => api.get(`/recipes/${id}`),
  create: (data) => api.post('/recipes/', data),
  delete: (id) => api.delete(`/recipes/${id}`),
  findMatching: () => api.get('/recipes/match/ingredients'),
  seedSample: () => api.post('/recipes/seed-sample'),
}

// News API
export const newsAPI = {
  getAllPublic: (skip = 0, limit = 10) =>
    api.get('/news/public', { params: { skip, limit } }),
  getBySlug: (slug) => api.get(`/news/public/${slug}`),

  // admin endpoints (نیاز به توکن admin)
  getAllAdmin: (token) =>
    api.get('/news/', { headers: { Authorization: `Bearer ${token}` } }),
  create: (data, token) =>
    api.post('/news/', data, { headers: { Authorization: `Bearer ${token}` } }),
  update: (id, data, token) =>
    api.put(`/news/${id}`, data, { headers: { Authorization: `Bearer ${token}` } }),
  delete: (id, token) =>
    api.delete(`/news/${id}`, { headers: { Authorization: `Bearer ${token}` } }),
}

export default api
