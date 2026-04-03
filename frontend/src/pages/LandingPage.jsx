import { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { gsap } from 'gsap'
import { ScrollToPlugin } from 'gsap/ScrollToPlugin'
import heroImg from '../../assets/hero_img.png'
import donorImg from '../../assets/donor_img.png'
import ngoImg from '../../assets/ngo_img.png'
import Footer from '../components/Footer.jsx'

gsap.registerPlugin(ScrollToPlugin)

/* Reusable CountUp Animation Component */
function CountUp({ end, duration = 2000, decimals = 0, suffix = '' }) {
  const [count, setCount] = useState(0)

  useEffect(() => {
    let startTimestamp = null
    const step = (timestamp) => {
      if (!startTimestamp) startTimestamp = timestamp
      const progress = Math.min((timestamp - startTimestamp) / duration, 1)
      const currentCount = progress * end
      setCount(currentCount)
      if (progress < 1) {
        window.requestAnimationFrame(step)
      }
    }
    window.requestAnimationFrame(step)
  }, [end, duration])

  return (
    <span>
      {count.toLocaleString(undefined, {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals,
      })}
      {suffix}
    </span>
  )
}

function LandingPage() {
  const [activeRole, setActiveRole] = useState('donors') // 'donors' or 'ngos'
  const { hash } = useLocation()

  const location = useLocation()

  useEffect(() => {
    const scrollToId = (id) => {
      const isHome = id === 'home' || id === 'top'
      gsap.to(window, {
        duration: 1.2,
        scrollTo: { 
          y: isHome ? 0 : `#${id}`, 
          autoKill: false, 
          offsetY: isHome ? 0 : 100 
        },
        ease: 'power4.inOut',
        overwrite: 'all',
      })
    }

    // 1. Handle navigation from of state (cross-page)
    if (location.state?.scrollTo) {
      scrollToId(location.state.scrollTo)
      // Clear state to avoid scrolling again on back nav
      window.history.replaceState({}, document.title)
    }

    // 2. Handle same-page internal clicking
    const handleEvent = (e) => scrollToId(e.detail)
    window.addEventListener('scrollToSection', handleEvent)

    return () => window.removeEventListener('scrollToSection', handleEvent)
  }, [location])

  const content = {
    donors: {
      title: 'How it Works for Donors',
      steps: [
        { title: 'Add food details', desc: 'Add available food with preparation details quickly.' },
        { title: 'Real-time visibility', desc: 'Get instant visibility into active donations and claims.' },
        { title: 'Track impact', desc: 'Track rescue impact and food waste reduction over time.' },
      ],
    },
    ngos: {
      title: 'How it Works for NGOs',
      steps: [
        { title: 'Browse feed', desc: 'Browse available food feed instantly in your local area.' },
        { title: 'Instant claim', desc: 'Claim suitable donations with one click to avoid waste.' },
        { title: 'Fast coordination', desc: 'Coordinate pickup and deliver faster with integrated maps.' },
      ],
    },
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <main id="home" className="px-6 py-12 md:px-16 md:py-20 lg:px-24">
        <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-12 md:flex-row">
          {/* Left Section: Content */}
          <div className="flex flex-col items-center text-center md:w-[50%] md:items-start md:text-left">
            <h1 className="font-instrument text-4xl leading-[0.95] tracking-tight text-slate-900 md:text-6xl lg:text-7xl">
              AI Infrastructure For <br /> Zero Food Waste
            </h1>
            <p className="mt-6 max-w-sm text-lg text-slate-600 md:mt-4 md:text-xl">
              An AI-driven network that routes excess food to where it’s needed
            </p>
            <div className="mt-8 flex flex-col items-center gap-4 sm:flex-row md:items-start">
              <Link
                to="/auth"
                className="font-instrument rounded-full bg-emerald-600 px-10 py-2 text-[15px] font-medium text-white transition-all hover:bg-emerald-700"
              >
                Join the Network
              </Link>
              <Link
                to="/#how-it-works"
                className="font-instrument rounded-full border border-slate-200 bg-white px-10 py-2 text-[15px] font-medium text-slate-900 transition-all hover:bg-slate-50"
              >
                See the Flow
              </Link>
            </div>
          </div>

          {/* Right Section: Image */}
          <div className="flex justify-center md:w-[50%] md:justify-end">
            <div className="relative max-w-[500px] transform transition-transform duration-700 hover:scale-[1.02] md:max-w-[600px] md:rotate-[-1deg]">
              <img
                src={heroImg}
                alt="SurplusX AI Infrastructure Illustration"
                className="h-auto w-full"
              />
            </div>
          </div>
        </div>
      </main>

      {/* How it Works Section */}
      <section id="how-it-works" className="mt-12 px-6 py-16 md:px-16 lg:px-24">
        <div className="mx-auto max-w-6xl">
          <div className="mb-12 flex flex-col items-center text-center">
            <h2 className="font-instrument text-3xl tracking-tight text-slate-900 md:text-4xl">
              How SurplusX Works
            </h2>
            <p className="mt-3 max-w-md text-[15px] text-slate-600">
              How surplus becomes impact, step by step
            </p>

            {/* Role Toggle */}
            <div className="mt-8 flex space-x-1 rounded-full border border-slate-100 bg-slate-50 p-1">
              <button
                onClick={() => setActiveRole('donors')}
                className={`font-instrument rounded-full px-6 py-1.5 text-[13px] transition-all ${activeRole === 'donors'
                  ? 'bg-emerald-600 text-white shadow-sm'
                  : 'text-slate-500 hover:text-emerald-600'
                  }`}
              >
                For Donors
              </button>
              <button
                onClick={() => setActiveRole('ngos')}
                className={`font-instrument rounded-full px-6 py-1.5 text-[13px] transition-all ${activeRole === 'ngos'
                  ? 'bg-emerald-600 text-white shadow-sm'
                  : 'text-slate-500 hover:text-emerald-600'
                  }`}
              >
                For NGOs
              </button>
            </div>
          </div>

          {/* Interactive Flow Layout with Dynamic Order */}
          <div
            key={activeRole}
            className={`flex flex-col animate-in fade-in duration-700 items-center gap-10 lg:flex-row lg:items-stretch ${activeRole === 'ngos' ? 'lg:flex-row-reverse slide-in-from-right-8' : 'slide-in-from-left-8'
              }`}
          >
            {/* Illustration Mockup */}
            <div className="w-full lg:w-[40%] flex">
              <div className="relative flex w-full flex-col overflow-hidden rounded-[2rem] bg-transparent p-6 ring-1 ring-slate-200/60 lg:h-full">
                <div className="flex items-center justify-between px-4 pb-6">
                  <div className="h-2 w-2 rounded-full bg-slate-200"></div>
                  <div className="h-1.5 w-12 rounded-full bg-slate-200"></div>
                  <div className="h-2 w-2 rounded-full bg-slate-200"></div>
                </div>
                <div className="flex-1 transform overflow-hidden transition-all duration-700 hover:scale-105">
                  <img
                    src={activeRole === 'donors' ? donorImg : ngoImg}
                    alt={`${activeRole === 'donors' ? 'Donor' : 'NGO'} Illustration`}
                    className={`h-full w-full object-contain ${activeRole === 'ngos' ? 'rotate-3 scale-110' : '-rotate-1'
                      } transition-transform duration-1000`}
                  />
                </div>
              </div>
            </div>

            {/* Steps Cards */}
            <div className="flex w-full flex-col space-y-4 lg:w-[60%]">
              {content[activeRole].steps.map((step, idx) => (
                <div
                  key={idx}
                  className="group rounded-[1.5rem] border border-slate-200 bg-white p-6 transition-all duration-300 hover:border-slate-400"
                >
                  <div className="mb-3 flex h-6 w-6 items-center justify-center rounded-full bg-emerald-600 text-[10px] font-medium text-white ring-4 ring-emerald-50">
                    {idx + 1}
                  </div>
                  <h3 className="font-instrument mb-2 text-xl tracking-tight text-slate-900">
                    {step.title}
                  </h3>
                  <p className="text-[14px] leading-relaxed text-slate-600">
                    {step.desc}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Real-World Impact Section */}
      <section id="impact" className="px-6 py-24 md:px-16 lg:px-24">
        <div className="mx-auto max-w-6xl">
          <div className="mb-20 flex flex-col items-center text-center">
            <h2 className="font-instrument text-3xl tracking-tight text-slate-900 md:text-5xl">
              Real-World Impact
            </h2>
            <p className="mt-4 max-w-xl text-slate-600">
              Turning surplus into measurable outcomes
            </p>
          </div>

          {/* Impact Cards Grid */}
          <div className="flex flex-col items-center justify-center gap-8 md:flex-row md:gap-12">
            {/* Meals Card */}
            <div className="group relative w-full min-h-[240px] max-w-[320px] rounded-[2.5rem] border-2 border-slate-100 bg-white p-10 text-center transition-all duration-300 hover:-translate-y-1 hover:border-emerald-600/20 hover:shadow-lg hover:shadow-emerald-600/5">
              <span className="font-instrument block text-5xl tracking-tight text-emerald-600 md:text-6xl">
                <CountUp end={1240} suffix="+" />
              </span>
              <div className="mt-6">
                <p className="font-instrument text-xl font-medium text-slate-900">Meals</p>
                <p className="font-instrument text-[15px] text-slate-500">Redistributed</p>
              </div>
            </div>

            {/* Network Card */}
            <div className="group relative w-full min-h-[240px] max-w-[320px] rounded-[2.5rem] border-2 border-slate-100 bg-white p-10 text-center transition-all duration-300 hover:-translate-y-1 hover:border-emerald-600/20 hover:shadow-lg hover:shadow-emerald-600/5">
              <span className="font-instrument block text-5xl tracking-tight text-emerald-600 md:text-6xl">
                <CountUp end={320} suffix="+" />
              </span>
              <div className="mt-6">
                <p className="font-instrument text-xl font-medium text-slate-900">Active</p>
                <p className="font-instrument text-[15px] text-slate-500">Network</p>
              </div>
            </div>

            {/* Waste Card */}
            <div className="group relative w-full min-h-[240px] max-w-[320px] rounded-[2.5rem] border-2 border-slate-100 bg-white p-10 text-center transition-all duration-300 hover:-translate-y-1 hover:border-emerald-600/20 hover:shadow-lg hover:shadow-emerald-600/5">
              <span className="font-instrument block text-5xl tracking-tight text-emerald-600 md:text-6xl">
                <CountUp end={3.8} decimals={1} suffix=" Tons" />
              </span>
              <div className="mt-6">
                <p className="font-instrument text-xl font-medium text-slate-900">Waste</p>
                <p className="font-instrument text-[15px] text-slate-500">Prevented</p>
              </div>
            </div>
          </div>
        </div>
      </section>
      <Footer />
    </div>
  )
}

export default LandingPage
