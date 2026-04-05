/**
 * CarCard — displays a single car listing with action buttons.
 * Actions shown depend on context (browse, my-cars, watched).
 */
import { useState } from 'react';
import { Car, MapPin, Calendar, DollarSign, Eye, MessageSquare } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export default function CarCard({ car, isWatched, onBook, onWatch, onMessage, onEdit, onDelete }) {
  const { user } = useAuth();
  const isOwner = user?.id === car.owner_id;
  const [showWatchForm, setShowWatchForm] = useState(false);
  const [maxPrice, setMaxPrice] = useState('');

  function handleWatch() {
    if (!maxPrice) return;
    onWatch(car.id, parseFloat(maxPrice));
    setShowWatchForm(false);
    setMaxPrice('');
  }

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <Car size={20} className="text-purple-600" />
          <h3 className="font-semibold text-gray-900">
            {car.year} {car.make} {car.model}
          </h3>
        </div>
        <span className="text-lg font-bold text-green-600">${car.daily_price}/day</span>
      </div>

      <div className="space-y-1.5 text-sm text-gray-600 mb-3">
        <div className="flex items-center gap-2">
          <MapPin size={14} /> {car.location}
        </div>
        <div className="flex items-center gap-2">
          <Calendar size={14} /> {car.mileage?.toLocaleString()} miles
        </div>
      </div>

      {car.features && car.features.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mb-3">
          {car.features.map(f => (
            <span key={f} className="px-2 py-0.5 text-xs bg-purple-50 text-purple-700 rounded-full">{f}</span>
          ))}
        </div>
      )}

      {car.availability && car.availability.length > 0 && (
        <div className="text-xs text-gray-500 mb-3">
          Available: {car.availability.map(a => `${a.start} to ${a.end}`).join(', ')}
        </div>
      )}

      {/* Action buttons */}
      <div className="flex flex-wrap gap-2 pt-3 border-t border-gray-100">
        {!isOwner && onBook && (
          <button onClick={() => onBook(car)}
            className="px-3 py-1.5 text-xs font-medium bg-purple-600 text-white rounded-lg hover:bg-purple-700">
            Book
          </button>
        )}
        {!isOwner && onWatch && (
          isWatched ? (
            <span className="flex items-center gap-1 px-3 py-1.5 text-xs font-medium text-green-700 bg-green-50 border border-green-200 rounded-lg">
              <Eye size={12} /> Watching
            </span>
          ) : (
            <>
              {!showWatchForm ? (
                <button onClick={() => setShowWatchForm(true)}
                  className="flex items-center gap-1 px-3 py-1.5 text-xs font-medium border border-purple-300 text-purple-700 rounded-lg hover:bg-purple-50">
                  <Eye size={12} /> Watch
                </button>
              ) : (
                <div className="flex items-center gap-1">
                  <input type="number" placeholder="Target price" value={maxPrice} required
                    onChange={e => setMaxPrice(e.target.value)}
                    className="w-24 px-2 py-1 text-xs border border-gray-300 rounded" />
                  <button onClick={handleWatch}
                    className="px-2 py-1 text-xs bg-purple-600 text-white rounded hover:bg-purple-700">OK</button>
                  <button onClick={() => setShowWatchForm(false)}
                    className="px-2 py-1 text-xs text-gray-500 hover:text-gray-700">Cancel</button>
                </div>
              )}
            </>
          )
        )}
        {!isOwner && onMessage && (
          <button onClick={() => onMessage(car.owner_id)}
            className="flex items-center gap-1 px-3 py-1.5 text-xs font-medium border border-gray-300 text-gray-600 rounded-lg hover:bg-gray-50">
            <MessageSquare size={12} /> Message Owner
          </button>
        )}
        {isOwner && onEdit && (
          <button onClick={() => onEdit(car)}
            className="px-3 py-1.5 text-xs font-medium border border-blue-300 text-blue-600 rounded-lg hover:bg-blue-50">
            Edit
          </button>
        )}
        {isOwner && onDelete && (
          <button onClick={() => onDelete(car.id)}
            className="px-3 py-1.5 text-xs font-medium border border-red-300 text-red-600 rounded-lg hover:bg-red-50">
            Delete
          </button>
        )}
      </div>
    </div>
  );
}
