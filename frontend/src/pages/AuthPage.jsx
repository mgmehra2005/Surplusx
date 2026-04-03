import { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.js'

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d]).{8,}$/

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
  const [formData, setFormData] = useState({ username: '', email: '', password: '' })
  const [errors, setErrors] = useState({})
  const { login, register } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  useEffect(() => {
    const params = new URLSearchParams(location.search)
    const modeParam = params.get('mode')
    if (modeParam === 'login' || modeParam === 'register') {
      setMode(modeParam)
    }
  }, [location.search])

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

    if (!passwordRegex.test(formData.password)) {
      nextErrors.password = 'Password must be 8+ chars with upper, lower, number, and symbol.'
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
    }

    if (mode === 'login') {
      login(authPayload)
    } else {
      register(authPayload)
    }

    const role = authPayload.email.toLowerCase().includes('admin')
      ? 'admin'
      : authPayload.email.toLowerCase().includes('ngo')
        ? 'ngo'
        : 'donor'

    navigate(getRouteByRole(role))
  }

  return (
    <main className="flex min-h-[calc(100vh-100px)] items-center justify-center px-4 py-12">
      <section className="w-full max-w-md rounded-[2rem] border border-slate-200/60 bg-white p-8 shadow-2xl shadow-slate-200/50">
        <h1 className="font-instrument text-3xl font-medium tracking-tight text-slate-900">
          {mode === 'login' ? 'Welcome Back' : 'Join SurplusX'}
        </h1>
        <p className="mt-3 font-instrument text-[15px] text-slate-500">
          {mode === 'login' 
            ? 'Enter your details to access your dashboard.' 
            : 'Start reducing food waste with the AI network.'}
        </p>

        <div className="mt-8 flex space-x-1 rounded-full border border-slate-100 bg-slate-50 p-1">
          <button
            className={`font-instrument flex-1 rounded-full px-4 py-2 text-[14px] font-medium transition-all ${
              mode === 'login' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-emerald-600'
            }`}
            onClick={() => setMode('login')}
            type="button"
          >
            Login
          </button>
          <button
            className={`font-instrument flex-1 rounded-full px-4 py-2 text-[14px] font-medium transition-all ${
              mode === 'register' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-emerald-600'
            }`}
            onClick={() => setMode('register')}
            type="button"
          >
            Register
          </button>
        </div>

        <form className="mt-5 space-y-4" onSubmit={onSubmit}>
          <div>
            <label className="font-instrument mb-1.5 block text-sm font-medium text-slate-700" htmlFor="username">
              Username
            </label>
            <input
              className="font-instrument w-full rounded-xl border border-slate-200 px-4 py-2.5 text-[15px] outline-none transition-all focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 placeholder:text-slate-400"
              id="username"
              name="username"
              placeholder="Enter your username"
              onChange={onInputChange}
              type="text"
              value={formData.username}
            />
            {errors.username && <p className="mt-1.5 font-instrument text-xs text-red-500">{errors.username}</p>}
          </div>

          <div>
            <label className="font-instrument mb-1.5 block text-sm font-medium text-slate-700" htmlFor="email">
              Email Address
            </label>
            <input
              className="font-instrument w-full rounded-xl border border-slate-200 px-4 py-2.5 text-[15px] outline-none transition-all focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 placeholder:text-slate-400"
              id="email"
              name="email"
              placeholder="e.g. name@example.com"
              onChange={onInputChange}
              type="email"
              value={formData.email}
            />
            {errors.email && <p className="mt-1.5 font-instrument text-xs text-red-500">{errors.email}</p>}
          </div>

          <div>
            <label className="font-instrument mb-1.5 block text-sm font-medium text-slate-700" htmlFor="password">
              Password
            </label>
            <input
              className="font-instrument w-full rounded-xl border border-slate-200 px-4 py-2.5 text-[15px] outline-none transition-all focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 placeholder:text-slate-400"
              id="password"
              name="password"
              placeholder="Minimum 8 characters"
              onChange={onInputChange}
              type="password"
              value={formData.password}
            />
            {errors.password && <p className="mt-1.5 font-instrument text-xs text-red-500">{errors.password}</p>}
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
