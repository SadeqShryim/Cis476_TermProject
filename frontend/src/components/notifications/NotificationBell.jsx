/**
 * NotificationBell — bell icon in the Navbar with an unread-count badge.
 *
 * Mediator Role: ConcreteColleague ("NotificationBell")
 * Listens for: most events (BOOKING_CREATED, PAYMENT_PROCESSED, MESSAGE_SENT, etc.)
 * Action:      Re-fetches notifications to update the unread count.
 */
import { useState, useEffect, useCallback, useRef } from 'react';
import { Bell } from 'lucide-react';
import { useColleague } from '../../hooks/useColleague';
import { EVENTS } from '../../patterns/mediator';
import { useAuth } from '../../context/AuthContext';
import * as api from '../../api/client';
import NotificationPanel from './NotificationPanel';

export default function NotificationBell() {
  const { user } = useAuth();
  const [notifications, setNotifications] = useState([]);
  const [showPanel, setShowPanel] = useState(false);
  const panelRef = useRef(null);

  const fetchNotifications = useCallback(async () => {
    if (!user) return;
    const { ok, data } = await api.get('/user/notifications');
    if (ok) setNotifications(data);
  }, [user]);

  // Colleague: refresh notifications on any relevant event
  const { send } = useColleague('NotificationBell', (event) => {
    if (event === EVENTS.USER_LOGGED_OUT) {
      setNotifications([]);
      return;
    }
    fetchNotifications();
  });

  useEffect(() => { fetchNotifications(); }, [fetchNotifications]);

  // Close panel on outside click
  useEffect(() => {
    function handleClick(e) {
      if (panelRef.current && !panelRef.current.contains(e.target)) {
        setShowPanel(false);
      }
    }
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  const unreadCount = notifications.filter(n => !n.read).length;

  return (
    <div className="relative" ref={panelRef}>
      <button onClick={() => setShowPanel(v => !v)} className="relative p-2 rounded-lg hover:bg-gray-100">
        <Bell size={20} className="text-gray-600" />
        {unreadCount > 0 && (
          <span className="absolute -top-0.5 -right-0.5 bg-red-500 text-white text-xs w-5 h-5 flex items-center justify-center rounded-full">
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </button>
      {showPanel && (
        <NotificationPanel
          notifications={notifications}
          onClose={() => setShowPanel(false)}
          onMarkRead={() => { send(EVENTS.NOTIFICATIONS_READ); fetchNotifications(); }}
        />
      )}
    </div>
  );
}
