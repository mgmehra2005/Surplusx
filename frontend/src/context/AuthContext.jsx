import { createContext, useState } from 'react'
import { loginUser, registerUser } from '../services/api.js'

const AuthContext = createContext(null)

function resolveRole(email) {
  const normalizedEmail = email.toLowerCase()
  if (normalizedEmail.includes('admin')) {
    return 'admin'
  }

  if (normalizedEmail.includes('ngo')) {
    return 'ngo'
  }

  return 'donor'
}

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

  const saveUser = (authUser) => {
    localStorage.setItem('surplusx-auth', JSON.stringify(authUser))
    setUser(authUser)
  }

  const login = async ({ username, password }) => {
    try {
      const data = await loginUser({ username, password })
      saveUser(data)
      return data
    } catch (error) {
      console.error('Login Error:', error)
      throw error
    }
  }

  const register = async (userData) => {
    try {
      const data = await registerUser(userData)
      saveUser(data)
      return data
    } catch (error) {
      console.error('Registration Error:', error)
      throw error
    }
  }

  const logout = () => {
    localStorage.removeItem('surplusx-auth')
    setUser(null)
  }

  const value = {
    user,
    isAuthenticated: Boolean(user),
    login,
    register,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export default AuthContext
