import { createContext, useState } from 'react'
import { loginUser, registerUser } from '../services/api.js'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const savedAuth = localStorage.getItem('surplusx-auth')
    if (!savedAuth) {
      return null
    }

    try {
      return JSON.parse(savedAuth)
    } catch {
      return null
    }
  })

  const [token, setToken] = useState(() => localStorage.getItem('surplusx-token'))

  const saveAuth = (userData, authToken) => {
    localStorage.setItem('surplusx-auth', JSON.stringify(userData))
    localStorage.setItem('surplusx-token', authToken)
    setUser(userData)
    setToken(authToken)
  }

  const login = async ({ username, password }) => {
    try {
      const data = await loginUser({ username, password })
      // Assuming API returns { user: {...}, token: "..." }
      saveAuth(data.user, data.token)
      return data
    } catch (error) {
      console.error('Login Error:', error)
      throw error
    }
  }

  const register = async (userData) => {
    try {
      const data = await registerUser(userData)
      // Assuming API returns { user: {...}, token: "..." }
      saveAuth(data.user, data.token)
      return data
    } catch (error) {
      console.error('Registration Error:', error)
      throw error
    }
  }

  const logout = () => {
    localStorage.removeItem('surplusx-auth')
    localStorage.removeItem('surplusx-token')
    setUser(null)
    setToken(null)
  }

  const value = {
    user,
    token,
    isAuthenticated: Boolean(user && token),
    login,
    register,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export default AuthContext
