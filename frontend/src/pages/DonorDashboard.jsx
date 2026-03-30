import { useEffect, useState } from 'react'
import { addFoodItem, getDonorDonations } from '../services/api.js'

function DonorDashboard() {
  const [formData, setFormData] = useState({
    name: '',
    type: '',
    preparationTime: '',
  })
  const [donations, setDonations] = useState([])
  const [statusMessage, setStatusMessage] = useState('')

  useEffect(() => {
    const loadDonations = async () => {
      const result = await getDonorDonations()
      setDonations(result)
    }

    loadDonations()
  }, [])

  const onInputChange = (event) => {
    const { name, value } = event.target
    setFormData((previous) => ({ ...previous, [name]: value }))
  }

  const onAddFood = async (event) => {
    event.preventDefault()

    if (!formData.name.trim() || !formData.type.trim() || !formData.preparationTime) {
      setStatusMessage('Please complete all fields before adding food.')
      return
    }

    const createdItem = await addFoodItem({
      name: formData.name.trim(),
      type: formData.type.trim(),
      preparationTime: formData.preparationTime,
    })

    setDonations((previous) => [createdItem, ...previous])
    setFormData({ name: '', type: '', preparationTime: '' })
    setStatusMessage('Food item added successfully.')
  }

  return (
    <main className="mx-auto grid max-w-6xl gap-6 px-4 py-8 md:grid-cols-2">
      <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <h1 className="text-2xl font-bold text-slate-900">Add Food</h1>
        <form className="mt-4 space-y-4" onSubmit={onAddFood}>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700" htmlFor="name">
              Food Name
            </label>
            <input
              className="w-full rounded-lg border border-slate-300 px-3 py-2 outline-none ring-emerald-500 focus:ring"
              id="name"
              name="name"
              onChange={onInputChange}
              type="text"
              value={formData.name}
            />
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700" htmlFor="type">
              Food Type
            </label>
            <input
              className="w-full rounded-lg border border-slate-300 px-3 py-2 outline-none ring-emerald-500 focus:ring"
              id="type"
              name="type"
              onChange={onInputChange}
              type="text"
              value={formData.type}
            />
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700" htmlFor="preparationTime">
              Preparation Time
            </label>
            <input
              className="w-full rounded-lg border border-slate-300 px-3 py-2 outline-none ring-emerald-500 focus:ring"
              id="preparationTime"
              name="preparationTime"
              onChange={onInputChange}
              type="datetime-local"
              value={formData.preparationTime}
            />
          </div>

          <button
            className="rounded-lg bg-emerald-600 px-4 py-2 font-medium text-white transition hover:bg-emerald-700"
            type="submit"
          >
            Add Food
          </button>

          {statusMessage && <p className="text-sm text-slate-600">{statusMessage}</p>}
        </form>
      </section>

      <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-slate-900">Active Donations</h2>
        <ul className="mt-4 space-y-3">
          {donations.map((item) => (
            <li className="rounded-lg border border-slate-200 p-3" key={item.id}>
              <p className="font-medium text-slate-900">{item.name}</p>
              <p className="text-sm text-slate-600">Type: {item.type}</p>
              <p className="text-sm text-slate-600">Prepared: {item.preparationTime}</p>
              <p className="text-sm font-medium text-amber-600">Freshness Score: Pending API</p>
            </li>
          ))}
        </ul>
      </section>
    </main>
  )
}

export default DonorDashboard
