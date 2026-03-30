import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
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
    <main className="mx-auto max-w-md px-4 py-10">
      <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <h1 className="text-2xl font-bold text-slate-900">{mode === 'login' ? 'Login' : 'Register'} to SurplusX</h1>
        <p className="mt-2 text-sm text-slate-600">
          Use <span className="font-semibold">ngo</span> or <span className="font-semibold">admin</span> in email to
          simulate role login.
        </p>

        <div className="mt-4 grid grid-cols-2 rounded-lg bg-slate-100 p-1">
          <button
            className={`rounded-md px-3 py-2 text-sm font-medium ${
              mode === 'login' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-600'
            }`}
            onClick={() => setMode('login')}
            type="button"
          >
            Login
          </button>
          <button
            className={`rounded-md px-3 py-2 text-sm font-medium ${
              mode === 'register' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-600'
            }`}
            onClick={() => setMode('register')}
            type="button"
          >
            Register
          </button>
        </div>

        <form className="mt-5 space-y-4" onSubmit={onSubmit}>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700" htmlFor="username">
              Username
            </label>
            <input
              className="w-full rounded-lg border border-slate-300 px-3 py-2 outline-none ring-emerald-500 focus:ring"
              id="username"
              name="username"
              onChange={onInputChange}
              type="text"
              value={formData.username}
            />
            {errors.username && <p className="mt-1 text-xs text-red-600">{errors.username}</p>}
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
            />
            {errors.password && <p className="mt-1 text-xs text-red-600">{errors.password}</p>}
          </div>

          <button
            className="w-full rounded-lg bg-emerald-600 px-4 py-2 font-medium text-white transition hover:bg-emerald-700"
            type="submit"
          >
            {mode === 'login' ? 'Login' : 'Create Account'}
          </button>
        </form>
      </section>
    </main>
  )
}

export default AuthPage
