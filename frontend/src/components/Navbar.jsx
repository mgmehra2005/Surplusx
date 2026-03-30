import { Link, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.js'

function navClassName({ isActive }) {
  return `rounded-md px-3 py-2 text-sm font-medium transition ${
    isActive ? 'bg-emerald-100 text-emerald-800' : 'text-slate-700 hover:bg-slate-100'
  }`
}

function Navbar() {
  const { user, isAuthenticated, logout } = useAuth()
  const navigate = useNavigate()

  const onLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <header className="sticky top-0 z-20 border-b border-slate-200 bg-white/95 backdrop-blur">
      <nav className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-3 px-4 py-3">
        <Link className="text-xl font-bold text-emerald-700" to="/">
          SurplusX
        </Link>

        <div className="flex flex-wrap items-center gap-2">
          <NavLink className={navClassName} to="/">
            Home
          </NavLink>

          {!isAuthenticated && (
            <NavLink className={navClassName} to="/auth">
              Login / Register
            </NavLink>
          )}

          {isAuthenticated && user.role === 'donor' && (
            <NavLink className={navClassName} to="/donor">
              Donor Dashboard
            </NavLink>
          )}

          {isAuthenticated && user.role === 'ngo' && (
            <NavLink className={navClassName} to="/ngo">
              NGO Dashboard
            </NavLink>
          )}

          {isAuthenticated && user.role === 'admin' && (
            <NavLink className={navClassName} to="/admin">
              Admin Panel
            </NavLink>
          )}

          {isAuthenticated && (
            <button
              className="rounded-md bg-slate-800 px-3 py-2 text-sm font-medium text-white hover:bg-slate-700"
              onClick={onLogout}
              type="button"
            >
              Logout
            </button>
          )}
        </div>
      </nav>
    </header>
  )
}

export default Navbar
