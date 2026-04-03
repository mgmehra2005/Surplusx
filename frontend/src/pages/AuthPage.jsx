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
  const [loading, setLoading] = useState(false)
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

  const onSubmit = async (event) => {
    event.preventDefault()

    if (!validate()) {
      return
    }

    setLoading(true)
    setErrors({})

    try {
      if (mode === 'login') {
        const userData = await login({
          username: formData.username.trim(),
          password: formData.password,
        })

        // On success, navigate to the specific dashboard
        const role = userData?.role || 'donor'
        navigate(getRouteByRole(role))
      } else {
        const authPayload = {
          username: formData.username.trim(),
          firstName: formData.firstName.trim(),
          lastName: formData.lastName.trim(),
          password: formData.password,
          email: formData.email.trim(),
          phone: `${formData.countryCode}${formData.phone.trim()}`,
          role: formData.role.toUpperCase(),
        }

        const userData = await register(authPayload)

        // On success, navigate to the specific dashboard
        const role = userData?.role || 'donor'
        navigate(getRouteByRole(role))
      }
    } catch (error) {
      const message = error.response?.data?.message || 'Authentication failed. Please check your credentials.'
      setErrors({ form: message })
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

        <form className="mt-8 space-y-5" onSubmit={onSubmit}>
          {errors.form && (
            <div className="rounded-xl border border-red-100 bg-red-50 p-4 font-instrument text-sm text-red-600">
              {errors.form}
            </div>
          )}
          {mode === 'register' && (
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="font-instrument mb-1.5 block text-sm font-medium text-slate-700" htmlFor="firstName">
                  First Name <span className="text-red-500">*</span>
                </label>
                  <input
                    className="font-instrument w-full rounded-xl border border-slate-200 px-4 py-2.5 text-[15px] outline-none transition-all focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 placeholder:text-slate-400"
                    id="firstName"
                    name="firstName"
                    placeholder="Rahul"
                    onChange={onInputChange}
                    type="text"
                    value={formData.firstName}
                    required
                  />
                {errors.firstName && <p className="mt-1.5 font-instrument text-xs text-red-500">{errors.firstName}</p>}
              </div>

              <div>
                <label className="font-instrument mb-1.5 block text-sm font-medium text-slate-700" htmlFor="lastName">
                  Last Name <span className="text-red-500">*</span>
                </label>
                <input
                  className="font-instrument w-full rounded-xl border border-slate-200 px-4 py-2.5 text-[15px] outline-none transition-all focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 placeholder:text-slate-400"
                  id="lastName"
                  name="lastName"
                  placeholder="Sharma"
                  onChange={onInputChange}
                  type="text"
                  value={formData.lastName}
                  required
                />
                {errors.lastName && <p className="mt-1.5 font-instrument text-xs text-red-500">{errors.lastName}</p>}
              </div>
            </div>
          )}

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
            className="font-instrument flex w-full items-center justify-center rounded-full bg-emerald-600 py-3 text-[15px] font-medium text-white transition-all hover:bg-emerald-700 hover:shadow-lg hover:shadow-emerald-600/20 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed"
            type="submit"
            disabled={loading}
          >
            {loading ? (
              <svg className="h-5 w-5 animate-spin text-white" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            ) : (
              mode === 'login' ? 'Login to Dashboard' : 'Create Account'
            )}
          </button>
        </form>
      </section>
    </main>
  )
}

export default AuthPage
