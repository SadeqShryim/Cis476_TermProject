/**
 * WatchedCarsPage — cars the user is watching with unwatch functionality.
 *
 * Mediator Role: ConcreteColleague ("WatchList")
 * Listens for: CAR_WATCHED, CAR_UNWATCHED, CAR_UPDATED, BOOKING_CREATED
 */
import { useState, useEffect, useCallback } from 'react';
import { Eye, EyeOff, Pencil } from 'lucide-react';
import { useColleague } from '../hooks/useColleague';
import { EVENTS } from '../patterns/mediator';
import * as api from '../api/client';
import LoadingSpinner from '../components/shared/LoadingSpinner';

export default function WatchedCarsPage() {
  const [watched, setWatched] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingId, setEditingId] = useState(null);
  const [editPrice, setEditPrice] = useState('');

  const fetchWatched = useCallback(async () => {
    setLoading(true);
    const { ok, data } = await api.get('/user/watched');
    if (ok) setWatched(data);
    setLoading(false);
  }, []);

  const { send } = useColleague('WatchList', (event) => {
    if ([EVENTS.CAR_WATCHED, EVENTS.CAR_UNWATCHED, EVENTS.CAR_UPDATED, EVENTS.BOOKING_CREATED].includes(event)) {
      fetchWatched();
    }
  });

  useEffect(() => { fetchWatched(); }, [fetchWatched]);

  async function handleUnwatch(carId) {
    await api.post(`/user/unwatch/${carId}`);
    send(EVENTS.CAR_UNWATCHED, { carId });
    fetchWatched();
  }

  async function handleUpdatePrice(carId) {
    if (!editPrice) return;
    await api.post(`/user/unwatch/${carId}`);
    await api.post('/user/watch', { car_id: carId, target_price: parseFloat(editPrice) });
    setEditingId(null);
    setEditPrice('');
    fetchWatched();
  }

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-4">Watched Cars</h1>
      {watched.length === 0 ? (
        <p className="text-gray-500 text-center py-12">You&apos;re not watching any cars.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {watched.map(w => {
            const car = w.car || w;
            const criteria = w.criteria || w;
            return (
              <div key={car.id} className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
                <div className="flex items-center gap-2 mb-2">
                  <Eye size={16} className="text-purple-600" />
                  <span className="font-semibold text-gray-900">
                    {car.year} {car.make} {car.model}
                  </span>
                </div>
                <div className="text-sm text-gray-600 space-y-1 mb-3">
                  <p>Price: ${car.daily_price}/day</p>
                  {car.location && <p>Location: {car.location}</p>}
                  {editingId === car.id ? (
                    <div className="flex items-center gap-1 mt-1">
                      <span className="text-xs text-gray-500">Target $</span>
                      <input type="number" value={editPrice}
                        onChange={e => setEditPrice(e.target.value)}
                        className="w-20 px-2 py-1 text-xs border border-gray-300 rounded" />
                      <button onClick={() => handleUpdatePrice(car.id)}
                        className="px-2 py-1 text-xs bg-purple-600 text-white rounded hover:bg-purple-700">Save</button>
                      <button onClick={() => { setEditingId(null); setEditPrice(''); }}
                        className="px-2 py-1 text-xs text-gray-500 hover:text-gray-700">Cancel</button>
                    </div>
                  ) : (
                    criteria.max_price && (
                      <p className="flex items-center gap-1">
                        Target Price: ${criteria.max_price}/day
                        <button onClick={() => { setEditingId(car.id); setEditPrice(String(criteria.max_price)); }}
                          className="text-purple-600 hover:text-purple-800">
                          <Pencil size={12} />
                        </button>
                      </p>
                    )
                  )}
                </div>
                <div className="flex gap-2">
                  <button onClick={() => handleUnwatch(car.id)}
                    className="flex items-center gap-1 px-3 py-1.5 text-xs font-medium border border-red-300 text-red-600 rounded-lg hover:bg-red-50">
                    <EyeOff size={12} /> Unwatch
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
