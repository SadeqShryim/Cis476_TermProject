/**
 * Navbar — top navigation bar shown on all dashboard pages.
 * Contains logo, BalanceDisplay (Mediator Colleague), NotificationBell
 * (Mediator Colleague), and logout button.
 */
import { Link, useNavigate } from 'react-router-dom';
import { LogOut, Menu, X } from 'lucide-react';
import { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import BalanceDisplay from '../payments/BalanceDisplay';
import NotificationBell from '../notifications/NotificationBell';

export default function Navbar({ onToggleSidebar, sidebarOpen }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  async function handleLogout() {
    await logout();
    navigate('/');
  }

  return (
    <nav className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-4 lg:px-8 sticky top-0 z-30">
      <div className="flex items-center gap-3">
        <button onClick={onToggleSidebar} className="lg:hidden p-1 rounded hover:bg-gray-100">
          {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
        <Link to="/dashboard" className="text-xl font-bold text-purple-700">DriveShare</Link>
      </div>

      <div className="flex items-center gap-4">
        <BalanceDisplay />
        <NotificationBell />
        <span className="hidden sm:inline text-sm text-gray-600">{user?.email}</span>
        <button onClick={handleLogout}
          className="flex items-center gap-1 text-sm text-gray-500 hover:text-red-600 transition-colors">
          <LogOut size={16} /> <span className="hidden sm:inline">Logout</span>
        </button>
      </div>
    </nav>
  );
}
