import { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.js'

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d]).{8,}$/
const phoneRegex = /^\d{10}$/

function getRouteByRole(role) {
  if (role === 'ngo') {
    return '/ngo'
  }

  if (role === 'admin') {
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

  const onSubmit = (event) => {
    event.preventDefault()

    if (!validate()) {
      return
    }

    const authPayload = {
      username: formData.username.trim(),
      email: formData.email.trim(),
      password: formData.password,
      firstName: formData.firstName.trim(),
      lastName: formData.lastName.trim(),
      phone: `${formData.countryCode} ${formData.phone.trim()}`,
      role: formData.role,
    }

    if (mode === 'login') {
      login(authPayload)
    } else {
      register(authPayload)
    }

    const finalRole = mode === 'login'
      ? (authPayload.email.toLowerCase().includes('admin')
        ? 'admin'
        : authPayload.email.toLowerCase().includes('ngo')
          ? 'ngo'
          : 'donor')
      : authPayload.role

    navigate(getRouteByRole(finalRole))
  }

  return (
    <main className="flex min-h-[calc(100vh-100px)] items-center justify-center px-4 py-12">
      <section className="w-full max-w-md rounded-[2rem] border border-slate-200/60 bg-white p-8 shadow-2xl shadow-slate-200/50">
        <h1 className="font-instrument text-3xl font-medium text-slate-900">
          {mode === 'login' ? 'Welcome Back' : 'Join SurplusX'}
        </h1>
        <p className="mt-3 font-instrument text-[15px] text-slate-500">
          {mode === 'login'
            ? 'Enter your details to access your dashboard.'
            : 'Start reducing food waste with the AI network.'}
        </p>

        <div className="mt-8 flex space-x-1 rounded-full border border-slate-100 bg-slate-50 p-1">
          <button
            className={`font-instrument flex-1 rounded-full px-4 py-2 text-[14px] font-medium transition-all ${mode === 'login' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-emerald-600'
              }`}
            onClick={() => setMode('login')}
            type="button"
          >
            Login
          </button>
          <button
            className={`font-instrument flex-1 rounded-full px-4 py-2 text-[14px] font-medium transition-all ${mode === 'register' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-emerald-600'
              }`}
            onClick={() => setMode('register')}
            type="button"
          >
            Register
          </button>
        </div>

        <form className="mt-8 space-y-5" onSubmit={onSubmit}>
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
              required
            />
            {errors.username && <p className="mt-1.5 font-instrument text-xs text-red-500">{errors.username}</p>}
          </div>

          <div className="space-y-5">
            <div>
              <label className="font-instrument mb-1.5 block text-sm font-medium text-slate-700" htmlFor="email">
                Email Address <span className="text-red-500">*</span>
              </label>
              <input
                className="font-instrument w-full rounded-xl border border-slate-200 px-4 py-2.5 text-[15px] outline-none transition-all focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 placeholder:text-slate-400"
                id="email"
                name="email"
                placeholder="rahul@example.com"
                onChange={onInputChange}
                type="email"
                value={formData.email}
                required
              />
              {errors.email && <p className="mt-1.5 font-instrument text-xs text-red-500">{errors.email}</p>}
            </div>

            {mode === 'register' && (
              <div>
                <label className="font-instrument mb-1.5 block text-sm font-medium text-slate-700" htmlFor="phone">
                  Phone Number <span className="text-red-500">*</span>
                </label>
                <div className="flex space-x-2">
                  <div className="w-[85px]">
                    <input
                      className="font-instrument w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-[15px] text-slate-500 outline-none cursor-not-allowed"
                      id="countryCode"
                      name="countryCode"
                      readOnly
                      type="text"
                      value="+91"
                      required
                    />
                  </div>
                  <div className="flex-1">
                    <input
                      className="font-instrument w-full rounded-xl border border-slate-200 px-4 py-2.5 text-[15px] outline-none transition-all focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 placeholder:text-slate-400"
                      id="phone"
                      name="phone"
                      placeholder="98765 00000"
                      onChange={onInputChange}
                      onKeyPress={(e) => {
                        if (!/[0-9]/.test(e.key)) {
                          e.preventDefault()
                        }
                      }}
                      type="tel"
                      maxLength="10"
                      value={formData.phone}
                      required
                    />
                  </div>
                </div>
                {errors.phone && <p className="mt-1.5 font-instrument text-xs text-red-500">{errors.phone}</p>}
              </div>
            )}
          </div>

          {mode === 'register' && (
            <div>
              <label className="font-instrument mb-1.5 block text-sm font-medium text-slate-700" htmlFor="role">
                You are a... <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <select
                  className="font-instrument w-full appearance-none rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-[15px] outline-none transition-all focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10"
                  id="role"
                  name="role"
                  onChange={onInputChange}
                  value={formData.role}
                  required
                >
                  <option value="" disabled>Select your role</option>
                  <option value="donor">Food Donor (Restaurant, Hotel, Individual)</option>
                  <option value="ngo">NGO / Relief Organization</option>
                </select>
                <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-4 text-slate-400">
                  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path d="M19 9l-7 7-7-7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
                  </svg>
                </div>
              </div>
              {errors.role && <p className="mt-1.5 font-instrument text-xs text-red-500">{errors.role}</p>}
            </div>
          )}

          <div className="space-y-5">
            <div>
              <label className="font-instrument mb-1.5 block text-sm font-medium text-slate-700" htmlFor="password">
                {mode === 'register' ? 'Create Password' : 'Password'} <span className="text-red-500">*</span>
              </label>
              <input
                className="font-instrument w-full rounded-xl border border-slate-200 px-4 py-2.5 text-[15px] outline-none transition-all focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 placeholder:text-slate-400"
                id="password"
                name="password"
                placeholder="••••••••"
                onChange={onInputChange}
                type="password"
                value={formData.password}
                required
              />
              {errors.password && <p className="mt-1.5 font-instrument text-xs text-red-500">{errors.password}</p>}
            </div>

            {mode === 'register' && (
              <div>
                <label className="font-instrument mb-1.5 block text-sm font-medium text-slate-700" htmlFor="confirmPassword">
                  Confirm Password <span className="text-red-500">*</span>
                </label>
                <input
                  className="font-instrument w-full rounded-xl border border-slate-200 px-4 py-2.5 text-[15px] outline-none transition-all focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 placeholder:text-slate-400"
                  id="confirmPassword"
                  name="confirmPassword"
                  placeholder="••••••••"
                  onChange={onInputChange}
                  type="password"
                  value={formData.confirmPassword}
                  required
                />
                {errors.confirmPassword && (
                  <p className="mt-1.5 font-instrument text-xs text-red-500">{errors.confirmPassword}</p>
                )}
              </div>
            )}
          </div>

          <button
            className="font-instrument w-full rounded-full bg-emerald-600 py-3 text-[15px] font-medium text-white transition-all hover:bg-emerald-700 hover:shadow-lg hover:shadow-emerald-600/20 active:scale-[0.98]"
            type="submit"
          >
            {mode === 'login' ? 'Login to Dashboard' : 'Create Account'}
          </button>
        </form>
      </section>
    </main>
  )
}

export default AuthPage
