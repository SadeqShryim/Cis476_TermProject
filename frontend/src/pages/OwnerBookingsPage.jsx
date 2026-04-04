/**
 * OwnerBookingsPage — bookings on the owner's cars.
 */
import { useState, useEffect, useCallback } from 'react';
import * as api from '../api/client';
import BookingCard from '../components/bookings/BookingCard';
import LoadingSpinner from '../components/shared/LoadingSpinner';

export default function OwnerBookingsPage() {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchBookings = useCallback(async () => {
    setLoading(true);
    const { ok, data } = await api.get('/bookings/as-owner');
    if (ok) setBookings(data);
    setLoading(false);
  }, []);

  useEffect(() => { fetchBookings(); }, [fetchBookings]);

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-4">Owner Bookings</h1>
      {bookings.length === 0 ? (
        <p className="text-gray-500 text-center py-12">No bookings on your cars yet.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {bookings.map(b => (
            <BookingCard key={b.id} booking={b} role="owner" onCancelled={() => fetchBookings()} />
          ))}
        </div>
      )}
    </div>
  );
}
