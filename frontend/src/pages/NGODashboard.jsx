import { useEffect, useState } from 'react'
import { claimFoodItem, getAvailableFoodItems } from '../services/api.js'

function NGODashboard() {
  const [foodFeed, setFoodFeed] = useState([])

  useEffect(() => {
    const loadFoodFeed = async () => {
      const items = await getAvailableFoodItems()
      setFoodFeed(items)
    }

    loadFoodFeed()
  }, [])

  const onClaim = async (itemId) => {
    await claimFoodItem(itemId)
    setFoodFeed((previous) => previous.filter((item) => item.id !== itemId))
  }

  return (
    <main className="mx-auto max-w-7xl px-6 py-12 md:px-16 lg:px-24">
      <section className="rounded-[2.5rem] border border-slate-200/60 bg-white p-10 shadow-2xl shadow-slate-200/40">
        <h1 className="font-instrument text-4xl font-medium tracking-tight text-slate-900 md:text-5xl">Available Food Feed</h1>
        <p className="mt-4 font-instrument text-[16px] text-slate-500">Real-time rescue opportunities in your area.</p>
        
        <div className="mt-12 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {foodFeed.map((item) => (
            <article 
              className="group flex flex-col justify-between rounded-[2rem] border border-slate-100 bg-slate-50/30 p-6 transition-all duration-300 hover:-translate-y-1 hover:border-emerald-200 hover:bg-white hover:shadow-xl hover:shadow-emerald-600/5" 
              key={item.id}
            >
              <div>
                <div className="mb-4 flex items-center justify-between">
                  <span className="font-instrument text-[12px] font-semibold uppercase tracking-wider text-emerald-600 bg-emerald-50 px-3 py-1 rounded-full">
                    {item.type}
                  </span>
                  <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
                </div>
                <h2 className="font-instrument text-2xl font-medium text-slate-900">{item.name}</h2>
                <div className="mt-4 space-y-2">
                  <p className="flex items-center text-[14px] text-slate-500">
                    <svg className="mr-2 h-4 w-4 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" /></svg>
                    {item.donorName}
                  </p>
                  <p className="flex items-center text-[14px] text-slate-500">
                    <svg className="mr-2 h-4 w-4 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" /></svg>
                    Prepared: {new Date(item.preparationTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
              </div>
              <button
                className="mt-8 font-instrument w-full rounded-full bg-emerald-600 py-3 text-[15px] font-medium text-white transition-all hover:bg-emerald-700 hover:shadow-lg hover:shadow-emerald-600/20 active:scale-[0.98]"
                onClick={() => onClaim(item.id)}
                type="button"
              >
                Claim Donation
              </button>
            </article>
          ))}
        </div>

        {foodFeed.length === 0 && (
          <div className="py-20 text-center">
            <p className="font-instrument text-lg text-slate-400">The feed is currently empty. Check back soon for fresh donations.</p>
          </div>
        )}
      </section>
    </main>
  )
}

export default NGODashboard
