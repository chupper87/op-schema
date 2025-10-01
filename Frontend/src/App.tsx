import { Routes, Route, Navigate } from "react-router-dom"
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'

export default function App() {
  return (
    <Routes>
      <Route path='/home' element={<HomePage />} />
      <Route path='/login' element={<LoginPage />} />
      <Route path='*' element={<Navigate to="/home" />} />
    </Routes>
  )
}