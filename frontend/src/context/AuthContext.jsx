import { createContext, useState } from 'react'

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

  const saveUser = (authUser) => {
    localStorage.setItem('surplusx-auth', JSON.stringify(authUser))
    setUser(authUser)
  }

  // BUG FIX #1: Now uses token-based auth from backend instead of email pattern
  // BUG FIX #2: Uses actual role from backend instead of parsing email
  const login = ({ username, email, token, uid, role }) => {
    saveUser({ username, email, token, uid, role })
  }

  const register = ({ username, email, token, uid, role }) => {
    saveUser({ username, email, token, uid, role })
  }

  const logout = () => {
    localStorage.removeItem('surplusx-auth')
    setUser(null)
  }

  const value = {
    user,
    isAuthenticated: Boolean(user && user.token),
    login,
    register,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export default AuthContext
