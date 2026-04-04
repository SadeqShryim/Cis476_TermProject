/**
 * MyBookingsPage — renter's bookings with pay, cancel, and review actions.
 *
 * Mediator Role: ConcreteColleague ("BookingList")
 * Listens for: BOOKING_CREATED, BOOKING_CANCELLED, PAYMENT_PROCESSED, REVIEW_SUBMITTED
 */
import { useState, useEffect, useCallback } from 'react';
import { useColleague } from '../hooks/useColleague';
import { EVENTS } from '../patterns/mediator';
import * as api from '../api/client';
import BookingCard from '../components/bookings/BookingCard';
import LoadingSpinner from '../components/shared/LoadingSpinner';

export default function MyBookingsPage() {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchBookings = useCallback(async () => {
    setLoading(true);
    const { ok, data } = await api.get('/bookings/as-renter');
    if (ok) setBookings(data);
    setLoading(false);
  }, []);

  useColleague('BookingList', (event) => {
    if ([EVENTS.BOOKING_CREATED, EVENTS.BOOKING_CANCELLED,
         EVENTS.PAYMENT_PROCESSED, EVENTS.REVIEW_SUBMITTED].includes(event)) {
      fetchBookings();
    }
  });

  useEffect(() => { fetchBookings(); }, [fetchBookings]);

  async function handleCancel(bookingId) {
    await api.post(`/bookings/${bookingId}/cancel`);
    fetchBookings();
  }

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-4">My Bookings</h1>
      {bookings.length === 0 ? (
        <p className="text-gray-500 text-center py-12">No bookings yet.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {bookings.map(b => (
            <BookingCard key={b.id} booking={b} role="renter" onCancelled={handleCancel} />
          ))}
        </div>
      )}
    </div>
  );
}
