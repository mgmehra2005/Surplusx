import { Link, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.js'
import logo from '../assets/transparent_logo.png'

function Navbar() {
  const { isAuthenticated, user, logout } = useAuth()
  const navigate = useNavigate()

  const navLinks = [
    { name: 'Home', target: 'home' },
    { name: 'How It Works', target: 'how-it-works' },
    { name: 'Impact', target: 'impact' },
  ]

  const handleNav = (target) => {
    if (window.location.pathname !== '/') {
      navigate('/', { state: { scrollTo: target } })
    } else {
      window.dispatchEvent(new CustomEvent('scrollToSection', { detail: target }))
    }
  }

  return (
    <header className="sticky top-0 z-50 w-full bg-white/20 px-6 py-5 backdrop-blur-md md:px-16 lg:px-24">
      <nav className="flex items-center justify-between">
        {/* Left: Logo */}
        <div className="flex flex-1">
          <Link to="/" className="flex items-center space-x-2 font-instrument text-lg font-medium tracking-tight text-slate-800">
            <img
              src={logo}
              alt="SurplusX Logo"
              className="h-10 w-10 object-contain"
            />
            <span className="text-2xl">SurplusX</span>
          </Link>
        </div>

        {/* Center: Links */}
        <div className="hidden flex-initial items-center space-x-10 md:flex">
          {navLinks.map((link) => (
            <button
              key={link.name}
              onClick={() => handleNav(link.target)}
              className="font-instrument text-[19px] font-medium text-slate-600 transition-colors hover:text-emerald-600"
            >
              {link.name}
            </button>
          ))}
        </div>

        {/* Right: Actions */}
        <div className="flex flex-1 items-center justify-end space-x-8">
          {isAuthenticated ? (
            <div className="flex items-center space-x-6">
              <Link
                to={['/donor', '/ngo', '/admin'].includes(window.location.pathname) ? '/' : (user.role === 'donor' ? '/donor' : user.role === 'ngo' ? '/ngo' : '/admin')}
                className="font-instrument rounded-full bg-emerald-600 px-8 py-2 text-[17px] font-medium text-white transition-all hover:bg-emerald-700 hover:shadow-lg hover:shadow-emerald-600/10"
              >
                {['/donor', '/ngo', '/admin'].includes(window.location.pathname) ? 'Back To Home' : 'Dashboard'}
              </Link>
              <button
                onClick={() => {
                  logout()
                  navigate('/')
                }}
                className="font-instrument text-[17px] font-medium text-slate-600 transition-colors hover:text-red-500"
              >
                Logout
              </button>
            </div>
          ) : (
            <div className="flex items-center space-x-6">
              <Link
                to="/auth"
                state={{ mode: 'login' }}
                className="font-instrument rounded-full bg-emerald-600 px-8 py-2 text-[17px] font-medium text-white transition-all hover:bg-emerald-700"
              >
                Login
              </Link>
              <Link
                to="/auth"
                state={{ mode: 'register' }}
                className="font-instrument text-[17px] font-medium text-slate-600 transition-colors hover:text-emerald-600"
              >
                Sign Up
              </Link>
            </div>
          )}
        </div>
      </nav>
    </header>
  )
}

export default Navbar
