import { Route, Routes } from 'react-router-dom'
import Navbar from './components/Navbar.jsx'
import ProtectedRoute from './components/ProtectedRoute.jsx'
import AdminPanel from './pages/AdminPanel.jsx'
import AuthPage from './pages/AuthPage.jsx'
import DonorDashboard from './pages/DonorDashboard.jsx'
import LandingPage from './pages/LandingPage.jsx'
import NGODashboard from './pages/NGODashboard.jsx'

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route element={<LandingPage />} path="/" />
        <Route element={<AuthPage />} path="/auth" />

        {/* BUG FIX: Use uppercase role names to match backend values */}
        <Route element={<ProtectedRoute allowedRoles={['DONOR']} />}>
          <Route element={<DonorDashboard />} path="/donor" />
        </Route>

        <Route element={<ProtectedRoute allowedRoles={['NGO']} />}>
          <Route element={<NGODashboard />} path="/ngo" />
        </Route>

        <Route element={<ProtectedRoute allowedRoles={['ADMIN']} />}>
          <Route element={<AdminPanel />} path="/admin" />
        </Route>

        <Route element={<LandingPage />} path="*" />
      </Routes>
    </>
  )
}

export default App
