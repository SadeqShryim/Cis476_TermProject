/**
 * WatchedCarsPage — cars the user is watching with unwatch functionality.
 *
 * Mediator Role: ConcreteColleague ("WatchList")
 * Listens for: CAR_WATCHED, CAR_UNWATCHED, CAR_UPDATED, BOOKING_CREATED
 */
import { useState, useEffect, useCallback } from 'react';
import { Eye, EyeOff } from 'lucide-react';
import { useColleague } from '../hooks/useColleague';
import { EVENTS } from '../patterns/mediator';
import * as api from '../api/client';
import LoadingSpinner from '../components/shared/LoadingSpinner';

export default function WatchedCarsPage() {
  const [watched, setWatched] = useState([]);
  const [loading, setLoading] = useState(true);

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

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-4">Watched Cars</h1>
      {watched.length === 0 ? (
        <p className="text-gray-500 text-center py-12">You&apos;re not watching any cars.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {watched.map(w => (
            <div key={w.car_id || w.id} className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
              <div className="flex items-center gap-2 mb-2">
                <Eye size={16} className="text-purple-600" />
                <span className="font-semibold text-gray-900">
                  {w.year} {w.make} {w.model}
                </span>
              </div>
              <div className="text-sm text-gray-600 space-y-1 mb-3">
                <p>Price: ${w.daily_price}/day</p>
                {w.location && <p>Location: {w.location}</p>}
                {w.max_price && <p>Target Price: ${w.max_price}/day</p>}
              </div>
              <button onClick={() => handleUnwatch(w.car_id || w.id)}
                className="flex items-center gap-1 px-3 py-1.5 text-xs font-medium border border-red-300 text-red-600 rounded-lg hover:bg-red-50">
                <EyeOff size={12} /> Unwatch
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
