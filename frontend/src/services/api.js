import axios from 'axios'

export const apiClient = axios.create({
  baseURL: 'http://localhost:5000/api',
})

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('surplusx-token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export async function loginUser({ username, password }) {
  const { data } = await apiClient.post('/auth/login', { username, password })
  return data
}

export async function registerUser(userData) {
  const { data } = await apiClient.post('/auth/register', userData)
  return data
}

/*
  TODO: Connect to Flask API: http://localhost:5000/api/....
  This service intentionally returns mock data right now.
  Replace these mocked async functions with real axios calls when backend APIs are finalized.
*/

const delay = (ms = 250) => new Promise((resolve) => {
  setTimeout(resolve, ms)
})

let donorDonations = [
  {
    id: 1,
    name: 'Cooked Rice Packs',
    type: 'Cooked Meal',
    preparationTime: '2026-03-30T08:15',
  },
  {
    id: 2,
    name: 'Fresh Vegetables Box',
    type: 'Raw Ingredients',
    preparationTime: '2026-03-30T07:00',
  },
]

let availableFood = [
  {
    id: 101,
    donorName: 'Helping Hands Restaurant',
    name: 'Veg Biryani',
    type: 'Cooked Meal',
    preparationTime: '2026-03-30T09:45',
  },
  {
    id: 102,
    donorName: 'Green Basket',
    name: 'Fruit Crates',
    type: 'Fresh Produce',
    preparationTime: '2026-03-30T07:30',
  },
]

export async function getDonorDonations() {
  await delay()
  return donorDonations
}

export async function addFoodItem(foodData) {
  await delay()
  const newItem = {
    id: Date.now(),
    ...foodData,
  }
  donorDonations = [newItem, ...donorDonations]
  return newItem
}

export async function getAvailableFoodItems() {
  await delay()
  return availableFood
}

export async function claimFoodItem(itemId) {
  await delay()
  availableFood = availableFood.filter((item) => item.id !== itemId)
  return { success: true }
}

export async function getAdminOverview() {
  await delay()
  return {
    totalUsers: 128,
    totalFoodRescuedKg: 4210,
    logs: [
      'New donor registration approved',
      'NGO claim completed for donation #102',
      'System health check: All services operational',
    ],
  }
}
