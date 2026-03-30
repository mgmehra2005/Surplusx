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
    <main className="mx-auto max-w-5xl px-4 py-8">
      <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <h1 className="text-2xl font-bold text-slate-900">Available Food Feed</h1>
        <div className="mt-4 grid gap-4 md:grid-cols-2">
          {foodFeed.map((item) => (
            <article className="rounded-lg border border-slate-200 p-4" key={item.id}>
              <h2 className="text-lg font-semibold text-slate-900">{item.name}</h2>
              <p className="text-sm text-slate-600">Donor: {item.donorName}</p>
              <p className="text-sm text-slate-600">Type: {item.type}</p>
              <p className="text-sm text-slate-600">Prepared: {item.preparationTime}</p>
              <button
                className="mt-3 rounded-lg bg-emerald-600 px-3 py-2 text-sm font-medium text-white hover:bg-emerald-700"
                onClick={() => onClaim(item.id)}
                type="button"
              >
                Claim
              </button>
            </article>
          ))}
        </div>

        {foodFeed.length === 0 && <p className="mt-3 text-sm text-slate-600">No available food items right now.</p>}
      </section>
    </main>
  )
}

export default NGODashboard
