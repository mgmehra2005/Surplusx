import { Link, NavLink } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.js'

function Navbar() {
  const { isAuthenticated, user } = useAuth()

  const navLinks = [
    { name: 'Home', path: '/#home' },
    { name: 'Features', path: '/#features' },
    { name: 'How It Works', path: '/#how-it-works' },
    { name: 'Impact', path: '/#impact' },
  ]

  return (
    <header className="sticky top-0 z-50 w-full bg-white/20 px-6 py-5 backdrop-blur-md md:px-16 lg:px-24">
      <nav className="flex items-center justify-between">
        {/* Left: Logo */}
        <div className="flex flex-1">
          <Link to="/" className="font-instrument text-lg font-medium tracking-tight text-slate-800">
            SurplusX
          </Link>
        </div>

        {/* Center: Links */}
        <div className="hidden flex-initial items-center space-x-10 md:flex">
          {navLinks.map((link) => (
            <NavLink
              key={link.name}
              to={link.path}
              className="font-instrument text-[14px] font-medium text-slate-600 transition-colors hover:text-slate-900"
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
                to="/auth"
                className="font-instrument rounded-full bg-slate-900 px-8 py-2.5 text-[14px] font-medium text-white transition-all hover:bg-slate-800"
              >
                Get Started
              </Link>
              <Link
                to="/auth"
                className="font-instrument text-[14px] font-medium text-slate-600 transition-colors hover:text-slate-900"
              >
                Sign In
              </Link>
            </>
          ) : (
            <Link
              to={user.role === 'donor' ? '/donor' : user.role === 'ngo' ? '/ngo' : '/admin'}
              className="font-instrument rounded-full bg-slate-900 px-8 py-2.5 text-[14px] font-medium text-white transition-all hover:bg-slate-800"
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
