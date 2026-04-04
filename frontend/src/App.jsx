/**
 * App — root component that wires together:
 *   MediatorProvider  → singleton DriveShareMediator for the Mediator pattern
 *   AuthProvider      → authentication state (user, token, login, logout)
 *   BrowserRouter     → client-side routing
 */
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { MediatorProvider } from './context/MediatorContext';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/layout/ProtectedRoute';

// Public pages
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ForgotPasswordPage from './pages/ForgotPasswordPage';

// Dashboard (authenticated)
import DashboardPage from './pages/DashboardPage';
import BrowseCarsPage from './pages/BrowseCarsPage';
import MyCarsPage from './pages/MyCarsPage';
import MyBookingsPage from './pages/MyBookingsPage';
import OwnerBookingsPage from './pages/OwnerBookingsPage';
import WatchedCarsPage from './pages/WatchedCarsPage';
import MessagesPage from './pages/MessagesPage';
import NotificationsPage from './pages/NotificationsPage';
import ProfilePage from './pages/ProfilePage';

export default function App() {
  return (
    <MediatorProvider>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            {/* Public routes */}
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/forgot-password" element={<ForgotPasswordPage />} />

            {/* Authenticated routes */}
            <Route element={<ProtectedRoute />}>
              <Route path="/dashboard" element={<DashboardPage />}>
                <Route index element={<BrowseCarsPage />} />
                <Route path="my-cars" element={<MyCarsPage />} />
                <Route path="bookings" element={<MyBookingsPage />} />
                <Route path="owner-bookings" element={<OwnerBookingsPage />} />
                <Route path="watched" element={<WatchedCarsPage />} />
                <Route path="messages" element={<MessagesPage />} />
                <Route path="messages/:userId" element={<MessagesPage />} />
                <Route path="notifications" element={<NotificationsPage />} />
                <Route path="profile" element={<ProfilePage />} />
              </Route>
            </Route>
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </MediatorProvider>
  );
}
