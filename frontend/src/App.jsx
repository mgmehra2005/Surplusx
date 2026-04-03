import { useEffect } from 'react'
import { Route, Routes, useLocation } from 'react-router-dom'
import Navbar from './components/Navbar.jsx'
import ProtectedRoute from './components/ProtectedRoute.jsx'
import AdminPanel from './pages/AdminPanel.jsx'
import AuthPage from './pages/AuthPage.jsx'
import DonorDashboard from './pages/DonorDashboard.jsx'
import LandingPage from './pages/LandingPage.jsx'
import NGODashboard from './pages/NGODashboard.jsx'

function ScrollToTop() {
  const { pathname } = useLocation()

  useEffect(() => {
    window.scrollTo(0, 0)
  }, [pathname])

  return null
}

function App() {
  return (
    <>
      <ScrollToTop />
      <Navbar />
      <Routes>
        <Route element={<LandingPage />} path="/" />
        <Route element={<AuthPage />} path="/auth" />

        <Route element={<ProtectedRoute allowedRoles={['donor']} />}>
          <Route element={<DonorDashboard />} path="/donor" />
        </Route>

        <Route element={<ProtectedRoute allowedRoles={['ngo']} />}>
          <Route element={<NGODashboard />} path="/ngo" />
        </Route>

        <Route element={<ProtectedRoute allowedRoles={['admin']} />}>
          <Route element={<AdminPanel />} path="/admin" />
        </Route>

        <Route element={<LandingPage />} path="*" />
      </Routes>
    </>
  )
}

export default App
