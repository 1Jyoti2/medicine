import { BrowserRouter, Route, Routes } from 'react-router-dom'

import MainLayout from './layouts/MainLayout.jsx'
import ProtectedRoute from './components/ProtectedRoute.jsx'
import AuthProvider from './context/AuthContext.jsx'
import { LanguageProvider } from './context/LanguageContext.jsx'
import About from './pages/About.jsx'
import ForgotPassword from './pages/ForgotPassword.jsx'
import HistoryPage from './pages/History.jsx'
import Home from './pages/Home.jsx'
import HowItWorks from './pages/HowItWorks.jsx'
import LeafDetection from './pages/LeafDetection.jsx'
import LeafResult from './pages/LeafResult.jsx'
import Login from './pages/Login.jsx'
import MedicineDetails from './pages/MedicineDetails.jsx'
import NotFound from './pages/NotFound.jsx'
import PrescriptionResult from './pages/PrescriptionResult.jsx'
import PrescriptionScanner from './pages/PrescriptionScanner.jsx'
import PlantDetails from './pages/PlantDetails.jsx'
import Profile from './pages/Profile.jsx'
import ResetPassword from './pages/ResetPassword.jsx'
import Signup from './pages/Signup.jsx'
import TabletDetection from './pages/TabletDetection.jsx'
import TabletResult from './pages/TabletResult.jsx'

function Protected({ children }) {
  return <ProtectedRoute>{children}</ProtectedRoute>
}

function App() {
  return (
    <BrowserRouter>
      <LanguageProvider>
        <AuthProvider>
          <Routes>
          <Route element={<MainLayout />}>
            <Route index element={<Home />} />
            <Route
              path="leaf-detection"
              element={
                <Protected>
                  <LeafDetection />
                </Protected>
              }
            />
            <Route path="result/leaf" element={<LeafResult />} />
            <Route
              path="tablet-detection"
              element={
                <Protected>
                  <TabletDetection />
                </Protected>
              }
            />
            <Route path="result/tablet" element={<TabletResult />} />
            <Route
              path="prescription"
              element={
                <Protected>
                  <PrescriptionScanner />
                </Protected>
              }
            />
            <Route path="result/prescription" element={<PrescriptionResult />} />
            <Route path="plant/:name" element={<PlantDetails />} />
            <Route path="medicine/:name" element={<MedicineDetails />} />
            <Route
              path="history"
              element={
                <Protected>
                  <HistoryPage />
                </Protected>
              }
            />
            <Route path="profile" element={<Protected><Profile /></Protected>} />
            <Route path="how-it-works" element={<HowItWorks />} />
            <Route path="about" element={<About />} />
            <Route path="login" element={<Login />} />
            <Route path="signup" element={<Signup />} />
            <Route path="forgot-password" element={<ForgotPassword />} />
            <Route path="reset-password" element={<ResetPassword />} />
            <Route path="*" element={<NotFound />} />
          </Route>
          </Routes>
        </AuthProvider>
      </LanguageProvider>
    </BrowserRouter>
  )
}

export default App