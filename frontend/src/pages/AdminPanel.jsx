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
    <main className="mx-auto max-w-7xl px-6 py-12 md:px-16 lg:px-24">
      <h1 className="font-instrument text-4xl font-medium tracking-tight text-slate-900 md:text-5xl">Admin Overview</h1>
      <p className="mt-4 font-instrument text-[16px] text-slate-500">Global food rescue metrics and system activity.</p>

      <section className="mt-12 grid gap-8 sm:grid-cols-2">
        <article className="group rounded-[2.5rem] border border-slate-200/60 bg-white p-10 shadow-2xl shadow-slate-200/30 transition-all hover:-translate-y-1">
          <p className="font-instrument text-[14px] font-semibold uppercase tracking-widest text-slate-400">Total Network Users</p>
          <div className="mt-4 flex items-baseline space-x-2">
            <p className="font-instrument text-6xl font-medium text-emerald-600">{overview.totalUsers}</p>
            <span className="text-[15px] font-medium text-slate-400">Members</span>
          </div>
        </article>

        <article className="group rounded-[2.5rem] border border-slate-200/60 bg-white p-10 shadow-2xl shadow-slate-200/30 transition-all hover:-translate-y-1">
          <p className="font-instrument text-[14px] font-semibold uppercase tracking-widest text-slate-400">Environment Impact</p>
          <div className="mt-4 flex items-baseline space-x-2">
            <p className="font-instrument text-6xl font-medium text-emerald-600">{overview.totalFoodRescuedKg}</p>
            <span className="text-[15px] font-medium text-slate-400">KG Rescued</span>
          </div>
        </article>
      </section>

      <section className="mt-12 rounded-[2.5rem] border border-slate-200/60 bg-white p-10 shadow-2xl shadow-slate-200/30">
        <h2 className="font-instrument text-3xl font-medium text-slate-900">System Logs</h2>
        <div className="mt-8 space-y-3">
          {overview.logs.length === 0 ? (
            <p className="py-10 text-center font-instrument text-slate-400">No system events logged today.</p>
          ) : (
            overview.logs.map((log, index) => (
              <div key={`log-${index}`} className="flex items-center space-x-4 rounded-xl bg-slate-50 px-6 py-4 transition-all hover:bg-slate-100/50">
                <span className="h-2 w-2 rounded-full bg-emerald-500"></span>
                <p className="font-instrument text-[15px] text-slate-700">{log}</p>
              </div>
            ))
          )}
        </div>
      </section>
    </main>
  )
}

export default AdminPanel
