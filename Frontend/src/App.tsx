import { Routes, Route, Navigate } from "react-router-dom"
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import CustomersPage from './pages/CustomersPage'
import EmployeesPage from './pages/EmployeesPage'
import SchedulePage from './pages/SchedulePage'
import MeasuresPage from './pages/MeasuresPage'
import StatisticsPage from './pages/StatisticsPage'

export default function App() {
  return (
    <Routes>
      <Route path='/home' element={<HomePage />} />
      <Route path='/login' element={<LoginPage />} />
      <Route path='/customers' element={<CustomersPage />} />
      <Route path="/employees" element={<EmployeesPage />} />
      <Route path="/schedule" element={<SchedulePage />} />
      <Route path="/measures" element={<MeasuresPage />} />
      <Route path="/statistics" element={<StatisticsPage />} />
      <Route path='*' element={<Navigate to="/home" />} />
    </Routes>
  )
}
