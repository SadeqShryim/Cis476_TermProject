/**
 * NotificationPanel — dropdown showing recent notifications with a "mark all read" button.
 */
import * as api from '../../api/client';
import { Check } from 'lucide-react';

export default function NotificationPanel({ notifications, onClose, onMarkRead }) {
  async function handleMarkAllRead() {
    await api.post('/user/notifications/mark-read');
    onMarkRead();
  }

  const recent = notifications.slice(0, 10);

  return (
    <div className="absolute right-0 top-12 w-80 bg-white border border-gray-200 rounded-xl shadow-lg z-50 overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-100">
        <h3 className="font-semibold text-sm text-gray-900">Notifications</h3>
        <button onClick={handleMarkAllRead}
          className="flex items-center gap-1 text-xs text-purple-600 hover:underline">
          <Check size={12} /> Mark all read
        </button>
      </div>
      <div className="max-h-72 overflow-y-auto">
        {recent.length === 0 ? (
          <p className="p-4 text-sm text-gray-500 text-center">No notifications yet.</p>
        ) : (
          recent.map(n => (
            <div key={n.id} className={`px-4 py-3 border-b border-gray-50 ${n.read ? '' : 'bg-purple-50'}`}>
              <p className="text-sm text-gray-700">{n.content}</p>
              <p className="text-xs text-gray-400 mt-1">{new Date(n.timestamp).toLocaleString()}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
