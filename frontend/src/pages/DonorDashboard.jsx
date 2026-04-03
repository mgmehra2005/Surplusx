import { useEffect, useState } from 'react'
import { addFoodItem, getDonorDonations } from '../services/api.js'

function DonorDashboard() {
  const [formData, setFormData] = useState({
    name: '',
    type: '',
    preparationTime: '',
    description: '',
    quantity: '',
    unit: 'kg',
    expiryTime: '',
  })
  const [locationData, setLocationData] = useState({
    address: '',
    country: 'India',
    city: '',
    state: '',
    zip: '',
  })
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [donations, setDonations] = useState([])
  const [statusMessage, setStatusMessage] = useState('')
  const [statusType, setStatusType] = useState('success') // 'success' or 'error'

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

  const onLocationInputChange = (event) => {
    const { name, value } = event.target
    setLocationData((previous) => ({ ...previous, [name]: value }))
  }

  const onAddFoodRequest = (event) => {
    event.preventDefault()

    if (
      !formData.name.trim() ||
      !formData.type.trim() ||
      !formData.preparationTime ||
      !formData.description.trim() ||
      !formData.quantity ||
      !formData.expiryTime
    ) {
      setStatusMessage('Please complete all fields before listing food.')
      setStatusType('error')
      return
    }

    const now = new Date()
    const prepDate = new Date(formData.preparationTime)
    const expiryDate = new Date(formData.expiryTime)

    if (prepDate > now) {
      setStatusMessage('Preparation date cannot be in the future.')
      setStatusType('error')
      return
    }

    if (expiryDate <= prepDate) {
      setStatusMessage('Expiry date must be after the preparation date.')
      setStatusType('error')
      return
    }

    setIsModalOpen(true)
  }

  const onFinalSubmit = async (event) => {
    event.preventDefault()

    if (!locationData.address.trim() || !locationData.city.trim() || !locationData.state.trim() || !locationData.zip.trim()) {
      return // HTML5 validation will typically handle this, but being safe
    }

    const payload = {
      title: formData.name.trim(),
      description: formData.description.trim(),
      foodType: formData.type.trim(),
      quantity: Number(formData.quantity),
      quantityUnit: formData.unit,
      preparationDate: formData.preparationTime,
      expiryDate: formData.expiryTime,
      location: {
        address: locationData.address.trim(),
        country: locationData.country,
        city: locationData.city.trim(),
        state: locationData.state.trim(),
        zipCode: locationData.zip.trim(),
      }
    }

    const createdItem = await addFoodItem(payload)

    setDonations((previous) => [createdItem, ...previous])
    setFormData({
      name: '',
      type: '',
      preparationTime: '',
      description: '',
      quantity: '',
      unit: 'kg',
      expiryTime: ''
    })
    setLocationData({
      address: '',
      country: 'India',
      city: '',
      state: '',
      zip: '',
    })
    setIsModalOpen(false)
    setStatusMessage('Food item listed successfully with location.')
    setStatusType('success')

    // Clear message after 5 seconds
    setTimeout(() => setStatusMessage(''), 5000)
  }

  return (
    <main className="mx-auto grid max-w-7xl gap-8 px-6 py-12 md:grid-cols-12 md:px-16 lg:px-24">
      {/* Step 1: Form Section */}
      <section className="md:col-span-5 rounded-[2rem] border border-slate-200/60 bg-white p-8 shadow-2xl shadow-slate-200/40 h-fit">
        <h1 className="font-instrument text-3xl font-medium tracking-tight text-slate-900 md:text-4xl">Add Food</h1>
        <p className="mt-3 font-instrument text-[15px] text-slate-500">Step 1: Item Details</p>

        <form className="mt-8 space-y-6" onSubmit={onAddFoodRequest}>
          <div className="space-y-2">
            <label className="font-instrument block text-[15px] font-medium text-slate-700" htmlFor="name">
              Food Item Name <span className="text-red-500">*</span>
            </label>
            <input
              className="font-instrument w-full rounded-xl border border-slate-200 px-4 py-2.5 text-[15px] outline-none transition-all focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 placeholder:text-slate-400"
              id="name"
              name="name"
              placeholder="e.g. Fresh Paneer Tikka"
              onChange={onInputChange}
              type="text"
              value={formData.name}
              required
            />
          </div>

          <div className="space-y-2">
            <label className="font-instrument block text-[15px] font-medium text-slate-700" htmlFor="type">
              Preparation / Food Type <span className="text-red-500">*</span>
            </label>
            <input
              className="font-instrument w-full rounded-xl border border-slate-200 px-4 py-2.5 text-[15px] outline-none transition-all focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 placeholder:text-slate-400"
              id="type"
              name="type"
              placeholder="Veg / Non-Veg / Bakery"
              onChange={onInputChange}
              type="text"
              value={formData.type}
              required
            />
          </div>

          <div className="space-y-2">
            <label className="font-instrument block text-[15px] font-medium text-slate-700" htmlFor="preparationTime">
              Preparation Time & Date <span className="text-red-500">*</span>
            </label>
            <input
              className="font-instrument w-full rounded-xl border border-slate-200 px-4 py-2.5 text-[15px] outline-none transition-all focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10"
              id="preparationTime"
              name="preparationTime"
              onChange={onInputChange}
              type="datetime-local"
              value={formData.preparationTime}
              max={new Date().toISOString().slice(0, 16)}
              required
            />
          </div>

          <div className="space-y-2">
            <label className="font-instrument block text-[15px] font-medium text-slate-700" htmlFor="expiryTime">
              Expiry Time & Date <span className="text-red-500">*</span>
            </label>
            <input
              className="font-instrument w-full rounded-xl border border-slate-200 px-4 py-2.5 text-[15px] outline-none transition-all focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10"
              id="expiryTime"
              name="expiryTime"
              onChange={onInputChange}
              type="datetime-local"
              value={formData.expiryTime}
              min={formData.preparationTime || new Date().toISOString().slice(0, 16)}
              required
            />
          </div>

          <div className="space-y-2">
            <label className="font-instrument block text-[15px] font-medium text-slate-700" htmlFor="quantity">
              Quantity <span className="text-red-500">*</span>
            </label>
            <div className="flex space-x-2">
              <input
                className="font-instrument flex-1 rounded-xl border border-slate-200 px-4 py-2.5 text-[15px] outline-none transition-all focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10"
                id="quantity"
                name="quantity"
                placeholder="2"
                onChange={onInputChange}
                type="number"
                value={formData.quantity}
                required
              />
              <select
                className="font-instrument w-[100px] rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-[14px] outline-none transition-all focus:border-emerald-500 select-none cursor-pointer"
                name="unit"
                onChange={onInputChange}
                value={formData.unit}
                required
              >
                <option value="kg">KG</option>
                <option value="grams">Grams</option>
                <option value="servings">Servings</option>
                <option value="packets">Packets</option>
              </select>
            </div>
          </div>

          <div className="space-y-2">
            <label className="font-instrument block text-[15px] font-medium text-slate-700" htmlFor="description">
              Food Description / Extra Notes <span className="text-red-500">*</span>
            </label>
            <textarea
              className="font-instrument min-h-[100px] w-full rounded-xl border border-slate-200 px-4 py-3 text-[15px] outline-none transition-all focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 placeholder:text-slate-400"
              id="description"
              name="description"
              placeholder="e.g. Freshly cooked, contains spice, properly packed."
              onChange={onInputChange}
              value={formData.description}
              required
            />
          </div>

          <button
            className="font-instrument w-full rounded-full bg-emerald-600 py-3 text-[15px] font-medium text-white shadow-lg shadow-emerald-600/10 transition-all hover:bg-emerald-700 hover:shadow-emerald-600/20 active:scale-[0.98]"
            type="submit"
          >
            List for Donation
          </button>

          {statusMessage && (
            <p className={`mt-4 text-center font-instrument text-[14px] font-medium py-2 rounded-lg ${statusType === 'error' ? 'text-red-600 bg-red-50' : 'text-emerald-600 bg-emerald-50'
              }`}>
              {statusMessage}
            </p>
          )}
        </form>
      </section>

      {/* Right Col: Active Feed */}
      <section className="md:col-span-7 rounded-[2rem] border border-slate-200/60 bg-white p-8 shadow-2xl shadow-slate-200/40">
        <h2 className="font-instrument text-3xl font-medium tracking-tight text-slate-900 md:text-3xl">Active Donations</h2>
        <p className="mt-3 font-instrument text-[15px] text-slate-500">Live feed of your contributions.</p>

        <div className="mt-8 space-y-4">
          {donations.length === 0 ? (
            <div className="py-12 text-center">
              <p className="font-instrument text-slate-400">No active donations yet. Start by adding one!</p>
            </div>
          ) : (
            donations.map((item) => (
              <div
                className="group flex items-center justify-between rounded-2xl border border-slate-100 p-5 transition-all hover:bg-slate-50/50 hover:border-emerald-200"
                key={item.id}
              >
                <div>
                  <h3 className="font-instrument text-lg font-medium text-slate-900">{item.name}</h3>
                  <div className="mt-1 flex items-center space-x-3 text-[13px] text-slate-500">
                    <span className="flex items-center"><span className="mr-1.5 h-1.5 w-1.5 rounded-full bg-emerald-500"></span>{item.type}</span>
                    <span>•</span>
                    <span>{new Date(item.preparationTime).toLocaleString([], { hour: '2-digit', minute: '2-digit', day: 'numeric', month: 'short' })}</span>
                  </div>
                </div>
                <div className="text-right">
                  <span className="font-instrument text-[12px] font-semibold uppercase tracking-wider text-amber-600 bg-amber-50 px-3 py-1 rounded-full">
                    Processing
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      </section>

      {/* Step 2: Location Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-slate-900/40 backdrop-blur-sm px-6">
          <div className="w-full max-w-xl rounded-3xl bg-white p-10 shadow-3xl">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="font-instrument text-3xl font-medium text-slate-900">Pickup Location</h2>
                <p className="mt-2 font-instrument text-slate-500">Where should the NGO collect the food?</p>
              </div>
              <button
                onClick={() => setIsModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 transition-colors"
              >
                <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" /></svg>
              </button>
            </div>

            <form className="mt-10 space-y-5" onSubmit={onFinalSubmit}>
              <div className="space-y-2">
                <label className="font-instrument block text-[15px] font-medium text-slate-700">
                  Street Address <span className="text-red-500">*</span>
                </label>
                <input
                  className="font-instrument w-full rounded-xl border border-slate-200 px-4 py-3 text-[15px] outline-none transition-all focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 placeholder:text-slate-400"
                  name="address"
                  placeholder="Street name, landmark..."
                  onChange={onLocationInputChange}
                  value={locationData.address}
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="font-instrument block text-[15px] font-medium text-slate-700">
                    City <span className="text-red-500">*</span>
                  </label>
                  <input
                    className="font-instrument w-full rounded-xl border border-slate-200 px-4 py-3 text-[15px] outline-none transition-all focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10"
                    name="city"
                    placeholder="e.g. New Delhi"
                    onChange={onLocationInputChange}
                    value={locationData.city}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <label className="font-instrument block text-[15px] font-medium text-slate-700">
                    State <span className="text-red-500">*</span>
                  </label>
                  <input
                    className="font-instrument w-full rounded-xl border border-slate-200 px-4 py-3 text-[15px] outline-none transition-all focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10"
                    name="state"
                    placeholder="e.g. Delhi"
                    onChange={onLocationInputChange}
                    value={locationData.state}
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="font-instrument block text-[15px] font-medium text-slate-700">
                    Country <span className="text-red-500">*</span>
                  </label>
                  <select
                    className="font-instrument w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-[15px] outline-none transition-all focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 cursor-pointer"
                    name="country"
                    onChange={onLocationInputChange}
                    value={locationData.country}
                    required
                  >
                    <option value="India">India</option>
                    <option value="USA">USA</option>
                    <option value="UK">UK</option>
                    <option value="Canada">Canada</option>
                    <option value="Australia">Australia</option>
                  </select>
                </div>
                <div className="space-y-2">
                  <label className="font-instrument block text-[15px] font-medium text-slate-700">
                    ZIP Code/Postal Code <span className="text-red-500">*</span>
                  </label>
                  <input
                    className="font-instrument w-full rounded-xl border border-slate-200 px-4 py-3 text-[15px] outline-none transition-all focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10"
                    name="zip"
                    placeholder="e.g. 110001"
                    onChange={onLocationInputChange}
                    value={locationData.zip}
                    type="number"
                    required
                  />
                </div>
              </div>

              <div className="pt-4">
                <button
                  className="font-instrument w-full rounded-full bg-emerald-600 py-4 text-[16px] font-semibold text-white shadow-xl shadow-emerald-600/20 transition-all hover:bg-emerald-700 active:scale-[0.98]"
                  type="submit"
                >
                  Finalize & List Donation
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </main>
  )
}

export default DonorDashboard
