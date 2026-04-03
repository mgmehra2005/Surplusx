import { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.js'
import { loginUser, registerUser } from '../services/api.js'

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d]).{8,}$/
const phoneRegex = /^\d{10}$/

function getRouteByRole(role) {
  if (role === 'NGO') {
    return '/ngo'
  }

  if (role === 'ADMIN') {
    return '/admin'
  }

  return '/donor'
}

function AuthPage() {
  const [mode, setMode] = useState('login')
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    firstName: '',
    lastName: '',
    phone: '',
    countryCode: '+91',
    role: '',
    confirmPassword: ''
  })
  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(false)
  const { login, register } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  useEffect(() => {
    if (location.state?.mode) {
      setMode(location.state.mode)
    }
  }, [location.state])

  const onInputChange = (event) => {
    const { name, value } = event.target
    setFormData((previous) => ({ ...previous, [name]: value }))
    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }))
    }
  }

  const validate = () => {
    const nextErrors = {}

    if (!formData.username.trim()) {
      nextErrors.username = 'Username is required.'
    } else if (formData.username.trim().length < 3) {
      nextErrors.username = 'Username must be at least 3 characters.'
    }

    if (!emailRegex.test(formData.email.trim())) {
      nextErrors.email = 'Please enter a valid email address.'
    }

    if (mode === 'register') {
      if (!passwordRegex.test(formData.password)) {
        nextErrors.password = 'Must be 8+ chars (upper, lower, num, symbol).'
      }
      if (!formData.firstName.trim()) {
        nextErrors.firstName = 'First name is required.'
      }
      if (!formData.lastName.trim()) {
        nextErrors.lastName = 'Last name is required.'
      }
      if (!formData.countryCode.trim()) {
        nextErrors.phone = 'Country code and number are required.'
      } else if (!phoneRegex.test(formData.phone.trim())) {
        nextErrors.phone = 'Please enter exactly 10 digits.'
      }
      if (!formData.role) {
        nextErrors.role = 'Please select your role.'
      }
      if (!formData.confirmPassword) {
        nextErrors.confirmPassword = 'Please confirm your password.'
      } else if (formData.password !== formData.confirmPassword) {
        nextErrors.confirmPassword = 'Passwords do not match.'
      }
    }

    setErrors(nextErrors)
    return Object.keys(nextErrors).length === 0
  }

  // BUG FIX: Now calls actual backend API for login/register
  // BUG FIX: Uses token and role from backend response
  const onSubmit = async (event) => {
    event.preventDefault()

    if (!validate()) {
      return
    }

    setLoading(true)
    try {
      const authPayload = {
        username: formData.username.trim(),
        email: formData.email.trim(),
        password: formData.password,
      }

      let response
      if (mode === 'login') {
        response = await loginUser(authPayload.email, authPayload.password)
      } else {
        response = await registerUser(authPayload.email, authPayload.username, authPayload.password)
      }

      if (response.user && response.token) {
        const userPayload = {
          username: response.user.name || authPayload.username,
          email: response.user.email || authPayload.email,
          token: response.token,
          uid: response.user.uid,
          role: response.user.role,
        }

        if (mode === 'login') {
          login(userPayload)
        } else {
          register(userPayload)
        }

        navigate(getRouteByRole(userPayload.role))
      } else {
        setErrors({ submit: response.message || 'Authentication failed' })
      }
    } catch (error) {
      setErrors({ submit: error.message || 'An error occurred. Please try again.' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="mx-auto max-w-md px-4 py-10">
      <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <h1 className="text-2xl font-bold text-slate-900">{mode === 'login' ? 'Login' : 'Register'} to SurplusX</h1>
        <p className="mt-2 text-sm text-slate-600">
          {mode === 'register'
            ? 'Role is assigned based on email domain. Email body can contain ngo or admin to set role.'
            : 'Login with your credentials'}
        </p>

        <div className="mt-8 flex space-x-1 rounded-full border border-slate-100 bg-slate-50 p-1">
          <button
            className={`rounded-md px-3 py-2 text-sm font-medium ${
              mode === 'login' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-600'
            }`}
            onClick={() => {
              setMode('login')
              setErrors({})
            }}
            type="button"
            disabled={loading}
          >
            Login
          </button>
          <button
            className={`rounded-md px-3 py-2 text-sm font-medium ${
              mode === 'register' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-600'
            }`}
            onClick={() => {
              setMode('register')
              setErrors({})
            }}
            type="button"
            disabled={loading}
          >
            Register
          </button>
        </div>

        <form className="mt-5 space-y-4" onSubmit={onSubmit}>
          {errors.submit && <div className="rounded-lg bg-red-50 p-3 text-sm text-red-600">{errors.submit}</div>}

          <div>
            <label className="font-instrument mb-1.5 block text-sm font-medium text-slate-700" htmlFor="username">
              Username <span className="text-red-500">*</span>
            </label>
            <input
              className="font-instrument w-full rounded-xl border border-slate-200 px-4 py-2.5 text-[15px] outline-none transition-all focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 placeholder:text-slate-400"
              id="username"
              name="username"
              placeholder="e.g. rahul123"
              onChange={onInputChange}
              type="text"
              value={formData.username}
              disabled={loading}
            />
            {errors.username && <p className="mt-1.5 font-instrument text-xs text-red-500">{errors.username}</p>}
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700" htmlFor="email">
              Email
            </label>
            <input
              className="w-full rounded-lg border border-slate-300 px-3 py-2 outline-none ring-emerald-500 focus:ring"
              id="email"
              name="email"
              onChange={onInputChange}
              type="email"
              value={formData.email}
              disabled={loading}
            />
            {errors.email && <p className="mt-1 text-xs text-red-600">{errors.email}</p>}
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700" htmlFor="password">
              Password
            </label>
            <input
              className="w-full rounded-lg border border-slate-300 px-3 py-2 outline-none ring-emerald-500 focus:ring"
              id="password"
              name="password"
              onChange={onInputChange}
              type="password"
              value={formData.password}
              disabled={loading}
            />
            {errors.password && <p className="mt-1 text-xs text-red-600">{errors.password}</p>}
          </div>

          <button
            className="w-full rounded-lg bg-emerald-600 px-4 py-2 font-medium text-white transition hover:bg-emerald-700 disabled:opacity-50"
            type="submit"
            disabled={loading}
          >
            {loading ? 'Processing...' : mode === 'login' ? 'Login' : 'Create Account'}
          </button>
        </form>
      </section>
    </main>
  )
}

export default AuthPage
