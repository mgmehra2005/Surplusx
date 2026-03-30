import { useEffect, useState } from 'react'
import { getAdminOverview } from '../services/api.js'

function AdminPanel() {
  const [overview, setOverview] = useState({
    totalUsers: 0,
    totalFoodRescuedKg: 0,
    logs: [],
  })

  useEffect(() => {
    const loadOverview = async () => {
      const result = await getAdminOverview()
      setOverview(result)
    }

    loadOverview()
  }, [])

  return (
    <main className="mx-auto max-w-5xl px-4 py-8">
      <h1 className="text-2xl font-bold text-slate-900">Admin Panel</h1>

      <section className="mt-4 grid gap-4 sm:grid-cols-2">
        <article className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-sm text-slate-500">Total Users</p>
          <p className="mt-1 text-3xl font-bold text-emerald-700">{overview.totalUsers}</p>
        </article>

        <article className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-sm text-slate-500">Total Food Rescued</p>
          <p className="mt-1 text-3xl font-bold text-emerald-700">{overview.totalFoodRescuedKg} kg</p>
        </article>
      </section>

      <section className="mt-6 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-slate-900">System Logs</h2>
        <ul className="mt-3 list-inside list-disc space-y-2 text-sm text-slate-700">
          {overview.logs.map((log) => (
            <li key={log}>{log}</li>
          ))}
        </ul>
      </section>
    </main>
  )
}

export default AdminPanel
