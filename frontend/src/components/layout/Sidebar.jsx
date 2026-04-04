/**
 * Sidebar — dashboard navigation links.
 */
import { NavLink } from 'react-router-dom';
import { Search, Car, CalendarDays, ClipboardList, Eye, MessageSquare, Bell, User } from 'lucide-react';

const links = [
  { to: '/dashboard',             icon: Search,         label: 'Browse Cars', end: true },
  { to: '/dashboard/my-cars',     icon: Car,            label: 'My Cars' },
  { to: '/dashboard/bookings',    icon: CalendarDays,   label: 'My Bookings' },
  { to: '/dashboard/owner-bookings', icon: ClipboardList, label: 'Owner Bookings' },
  { to: '/dashboard/watched',     icon: Eye,            label: 'Watched Cars' },
  { to: '/dashboard/messages',    icon: MessageSquare,  label: 'Messages' },
  { to: '/dashboard/notifications', icon: Bell,         label: 'Notifications' },
  { to: '/dashboard/profile',     icon: User,           label: 'Profile' },
];

export default function Sidebar({ open, onClose }) {
  return (
    <>
      {/* Overlay for mobile */}
      {open && (
        <div className="fixed inset-0 bg-black/30 z-20 lg:hidden" onClick={onClose} />
      )}
      <aside className={`
        fixed lg:static inset-y-0 left-0 z-20 w-60 bg-white border-r border-gray-200
        transform transition-transform lg:translate-x-0
        ${open ? 'translate-x-0' : '-translate-x-full'}
        pt-16 lg:pt-0
      `}>
        <nav className="flex flex-col gap-1 p-4">
          {links.map(({ to, icon: Icon, label, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              onClick={onClose}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors
                ${isActive ? 'bg-purple-100 text-purple-700' : 'text-gray-600 hover:bg-gray-100'}`
              }
            >
              <Icon size={18} />
              {label}
            </NavLink>
          ))}
        </nav>
      </aside>
    </>
  );
}
