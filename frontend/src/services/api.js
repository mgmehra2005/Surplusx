import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
})

// Add JWT token to all requests
apiClient.interceptors.request.use((config) => {
  const auth = localStorage.getItem('surplusx-auth')
  if (auth) {
    try {
      const authData = JSON.parse(auth)
      if (authData.token) {
        config.headers.Authorization = `Bearer ${authData.token}`
      }
    } catch (e) {
      console.error('Failed to parse auth data:', e)
    }
  }
  return config
})

// BUG FIX: All functions now call real backend API instead of mock data

export async function registerUser(email, username, password, role = 'DONOR') {
  try {
    const response = await apiClient.post('/auth/register', {
      email,
      name: username,
      password,
      role,
    })
    return response.data
  } catch (error) {
    throw error.response?.data || { message: 'Registration failed' }
  }
}

export async function loginUser(email, password) {
  try {
    const response = await apiClient.post('/auth/login', {
      email,
      password,
    })
    return response.data
  } catch (error) {
    throw error.response?.data || { message: 'Login failed' }
  }
}

export async function getDonorDonations() {
  try {
    const response = await apiClient.get('/food', {
      params: { status: 'AVAILABLE' },
    })
    return response.data.data || []
  } catch (error) {
    console.error('Failed to fetch donor donations:', error)
    return []
  }
}

export async function addFoodItem(foodData) {
  try {
    const response = await apiClient.post('/food/add', {
      title: foodData.name,
      food_type: foodData.type,
      quantity: foodData.quantity || 1,
      quantity_unit: foodData.quantity_unit || 'units',
      preparation_date: foodData.preparationTime || new Date().toISOString(),
      expiry_date: foodData.expiry_date || new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
      description: foodData.description,
      location: foodData.location,
    })
    return response.data.data
  } catch (error) {
    throw error.response?.data || { message: 'Failed to add food item' }
  }
}

export async function getAvailableFoodItems() {
  try {
    const response = await apiClient.get('/food', {
      params: { status: 'AVAILABLE' },
    })
    return response.data.data || []
  } catch (error) {
    console.error('Failed to fetch available food:', error)
    return []
  }
}

export async function getFoodItemById(foodId) {
  try {
    const response = await apiClient.get(`/food/${foodId}`)
    return response.data.data
  } catch (error) {
    throw error.response?.data || { message: 'Failed to fetch food item' }
  }
}

export async function updateFoodItem(foodId, updates) {
  try {
    const response = await apiClient.put(`/food/${foodId}`, updates)
    return response.data.data
  } catch (error) {
    throw error.response?.data || { message: 'Failed to update food item' }
  }
}

export async function claimFoodItem(itemId) {
  try {
    const response = await apiClient.put(`/food/${itemId}`, {
      status: 'MATCHED',
    })
    return { success: true, data: response.data.data }
  } catch (error) {
    throw error.response?.data || { message: 'Failed to claim food item' }
  }
}

export async function deleteFoodItem(itemId) {
  try {
    await apiClient.delete(`/food/${itemId}`)
    return { success: true }
  } catch (error) {
    throw error.response?.data || { message: 'Failed to delete food item' }
  }
}

export async function getAdminOverview() {
  try {
    const response = await apiClient.get('/admin/overview')
    return response.data.data
  } catch (error) {
    console.error('Failed to fetch admin overview:', error)
    return {
      totalUsers: 0,
      totalFoodRescuedKg: 0,
      logs: ['Error loading data'],
    }
  }
}
