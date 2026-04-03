import React from 'react'
import { Link } from 'react-router-dom'
import footerImg from '../assets/footer.png'
import logo from '../assets/transparent_logo.png'

const Footer = () => {
  return (
    <footer className="w-full bg-white pt-24">
      <div className="mx-auto max-w-7xl px-6 md:px-16 lg:px-24">
        {/* Simplified Footer Grid */}
        <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-12 pb-20">
          {/* Brand & Mission */}
          <div className="space-y-6 max-w-sm">
            <Link to="/" className="flex items-center space-x-3 font-instrument text-2xl font-medium tracking-tight text-slate-900 group">
              <img 
                src={logo} 
                alt="SurplusX Logo" 
                className="h-10 w-10 object-contain transition-transform group-hover:scale-110" 
              />
              <span>SurplusX</span>
            </Link>
            <p className="font-instrument text-[16px] leading-relaxed text-slate-500">
              AI infrastructure for zero food waste. Connecting surplus food to those who need it most, in real-time.
            </p>
          </div>

          {/* Minimal Links */}
          <div className="flex space-x-16">
            <div className="space-y-4">
              <h4 className="font-instrument text-[14px] font-semibold uppercase tracking-widest text-slate-900">Platform</h4>
              <ul className="space-y-3 font-instrument text-[15px] text-slate-500">
                <li><button onClick={() => window.dispatchEvent(new CustomEvent('scrollToSection', { detail: 'how-it-works' }))} className="transition-colors hover:text-emerald-600">How it works</button></li>
                <li><button onClick={() => window.dispatchEvent(new CustomEvent('scrollToSection', { detail: 'impact' }))} className="transition-colors hover:text-emerald-600">Impact</button></li>
              </ul>
            </div>
            <div className="space-y-4">
              <h4 className="font-instrument text-[14px] font-semibold uppercase tracking-widest text-slate-900">Company</h4>
              <ul className="space-y-3 font-instrument text-[15px] text-slate-500">
                <li><Link to="/" className="transition-colors hover:text-emerald-600">About us</Link></li>
                <li><Link to="/" className="transition-colors hover:text-emerald-600">Contact</Link></li>
              </ul>
            </div>
          </div>
        </div>

        {/* Lower Legal Bar */}
        <div className="flex flex-col border-t border-slate-100 py-10 md:flex-row md:items-center md:justify-between gap-6">
          <p className="font-instrument text-[14px] text-slate-400">
            © {new Date().getFullYear()} SurplusX. All rights reserved.
          </p>
          <div className="flex space-x-8 font-instrument text-[14px] text-slate-400">
            <Link to="/" className="hover:text-emerald-600">Privacy Policy</Link>
            <Link to="/" className="hover:text-emerald-600">Terms</Link>
          </div>
        </div>
      </div>

      {/* Seamless Artistic Image Footer */}
      <div className="w-full leading-[0] overflow-hidden">
        <img
          src={footerImg}
          alt="SurplusX Landscape Integration"
          className="w-full h-auto object-cover"
        />
      </div>
    </footer>
  )
}

export default Footer
