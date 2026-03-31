import { Link, NavLink } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.js'

function Navbar() {
  const { isAuthenticated, user } = useAuth()

  const navLinks = [
    { name: 'Home', path: '/#home' },
    { name: 'How It Works', path: '/#how-it-works' },
    { name: 'Impact', path: '/#impact' },
  ]

  return (
    <header className="sticky top-0 z-50 w-full bg-white/20 px-6 py-5 backdrop-blur-md md:px-16 lg:px-24">
      <nav className="flex items-center justify-between">
        {/* Left: Logo */}
        <div className="flex flex-1">
          <Link to="/" className="flex items-center space-x-2 font-parabolica text-lg font-medium tracking-tight text-slate-800">
            <svg
              className="h-7 w-7 text-emerald-600"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M18 6L6 18M6 6l12 12" />
              <circle cx="12" cy="12" r="3" fill="currentColor" fillOpacity="0.2" />
            </svg>
            <span>SurplusX</span>
          </Link>
        </div>

        {/* Center: Links */}
        <div className="hidden flex-initial items-center space-x-10 md:flex">
          {navLinks.map((link) => (
            <NavLink
              key={link.name}
              to={link.path}
              className="font-parabolica text-[15px] font-medium text-slate-600 transition-colors hover:text-emerald-600"
            >
              {link.name}
            </NavLink>
          ))}
        </div>

        {/* Right: Actions */}
        <div className="flex flex-1 items-center justify-end space-x-8">
          {!isAuthenticated ? (
            <>
              <Link
                to="/auth?mode=login"
                className="font-parabolica rounded-full bg-emerald-600 px-8 py-2.5 text-[15px] font-medium text-white transition-all hover:bg-emerald-700"
              >
                Login
              </Link>
              <Link
                to="/auth?mode=register"
                className="font-parabolica text-[15px] font-medium text-slate-600 transition-colors hover:text-emerald-600"
              >
                Sign Up
              </Link>
            </>
          ) : (
            <Link
              to={user.role === 'donor' ? '/donor' : user.role === 'ngo' ? '/ngo' : '/admin'}
              className="font-parabolica rounded-full bg-emerald-600 px-8 py-2.5 text-[14px] font-medium text-white transition-all hover:bg-emerald-700"
            >
              Dashboard
            </Link>
          )}
        </div>
      </nav>
    </header>
  )
}

export default Navbar
