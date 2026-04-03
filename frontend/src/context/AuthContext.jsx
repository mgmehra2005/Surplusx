import { createContext, useState } from 'react'

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

  const login = ({ username, email }) => {
    const role = resolveRole(email)
    saveUser({ username, email, role })
  }

  const register = ({ username, email, role }) => {
    // For registration, we use the role chosen by the user in the dropdown
    saveUser({ username, email, role })
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
