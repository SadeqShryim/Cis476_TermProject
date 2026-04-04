/**
 * NotificationsPage — full notification history.
 */
import { useState, useEffect } from 'react';
import { Bell, Check } from 'lucide-react';
import * as api from '../api/client';
import LoadingSpinner from '../components/shared/LoadingSpinner';

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);

  async function fetchNotifications() {
    setLoading(true);
    const { ok, data } = await api.get('/user/notifications');
    if (ok) setNotifications(data);
    setLoading(false);
  }

  useEffect(() => { fetchNotifications(); }, []);

  async function handleMarkAllRead() {
    await api.post('/user/notifications/mark-read');
    fetchNotifications();
  }

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-bold text-gray-900">Notifications</h1>
        <button onClick={handleMarkAllRead}
          className="flex items-center gap-1 px-3 py-1.5 text-sm text-purple-600 border border-purple-300 rounded-lg hover:bg-purple-50">
          <Check size={14} /> Mark All Read
        </button>
      </div>

      {notifications.length === 0 ? (
        <p className="text-gray-500 text-center py-12">No notifications.</p>
      ) : (
        <div className="space-y-2">
          {notifications.map(n => (
            <div key={n.id}
              className={`flex items-start gap-3 p-4 bg-white border border-gray-200 rounded-lg ${n.read ? '' : 'border-l-4 border-l-purple-500'}`}>
              <Bell size={16} className="text-gray-400 mt-0.5 flex-shrink-0" />
              <div className="flex-1">
                <p className="text-sm text-gray-700">{n.content}</p>
                <div className="flex items-center gap-3 mt-1">
                  <span className="text-xs text-gray-400">{new Date(n.timestamp).toLocaleString()}</span>
                  <span className="text-xs px-1.5 py-0.5 bg-gray-100 text-gray-500 rounded">{n.type}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
