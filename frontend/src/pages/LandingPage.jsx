function LandingPage() {
  return (
    <main className="mx-auto max-w-6xl px-4 py-8">
      <section className="rounded-2xl bg-gradient-to-r from-emerald-600 to-teal-600 p-8 text-white md:p-12">
        <p className="text-sm uppercase tracking-widest text-emerald-100">Food Redistribution System</p>
        <h1 className="mt-3 text-3xl font-bold md:text-5xl">Redistribute Surplus Food. Nourish More Lives.</h1>
        <p className="mt-4 max-w-2xl text-emerald-50">
          SurplusX connects donors and NGOs in real-time to reduce food waste and improve community impact.
        </p>
      </section>

      <section className="mt-10 grid gap-6 md:grid-cols-2">
        <article className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-slate-900">How it Works for Donors</h2>
          <ol className="mt-4 list-inside list-decimal space-y-2 text-slate-700">
            <li>Add available food with preparation details.</li>
            <li>Get visibility into active donations.</li>
            <li>Track rescue impact over time.</li>
          </ol>
        </article>

        <article className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-slate-900">How it Works for NGOs</h2>
          <ol className="mt-4 list-inside list-decimal space-y-2 text-slate-700">
            <li>Browse available food feed instantly.</li>
            <li>Claim suitable donations with one click.</li>
            <li>Coordinate pickup and deliver faster.</li>
          </ol>
        </article>
      </section>

      <section className="mt-10 grid gap-4 sm:grid-cols-3">
        <div className="rounded-xl bg-white p-6 text-center shadow-sm ring-1 ring-slate-200">
          <p className="text-3xl font-bold text-emerald-700">1,240+</p>
          <p className="mt-1 text-sm text-slate-600">Meals Redistributed</p>
        </div>
        <div className="rounded-xl bg-white p-6 text-center shadow-sm ring-1 ring-slate-200">
          <p className="text-3xl font-bold text-emerald-700">320+</p>
          <p className="mt-1 text-sm text-slate-600">Active Donors & NGOs</p>
        </div>
        <div className="rounded-xl bg-white p-6 text-center shadow-sm ring-1 ring-slate-200">
          <p className="text-3xl font-bold text-emerald-700">3.8 Tons</p>
          <p className="mt-1 text-sm text-slate-600">Food Waste Prevented</p>
        </div>
      </section>
    </main>
  )
}

export default LandingPage
