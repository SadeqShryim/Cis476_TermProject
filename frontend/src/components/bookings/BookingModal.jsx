/**
 * BookingModal — modal for booking a car with date selection.
 *
 * Mediator Role: ConcreteColleague ("BookingModal")
 * Sends: BOOKING_CREATED
 */
import { useState } from 'react';
import { useColleague } from '../../hooks/useColleague';
import { EVENTS } from '../../patterns/mediator';
import * as api from '../../api/client';
import ErrorAlert from '../shared/ErrorAlert';

export default function BookingModal({ car, onClose }) {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const { send } = useColleague('BookingModal', () => {});

  // Calculate total price based on date range
  function getDays() {
    if (!startDate || !endDate) return 0;
    const diff = (new Date(endDate) - new Date(startDate)) / (1000 * 60 * 60 * 24);
    return Math.max(0, diff);
  }
  const days = getDays();
  const total = days * car.daily_price;

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    if (days <= 0) return setError('End date must be after start date.');
    setLoading(true);
    const { ok, error: err } = await api.post('/bookings/', {
      car_id: car.id,
      start_date: startDate,
      end_date: endDate,
    });
    setLoading(false);
    if (!ok) return setError(err);
    send(EVENTS.BOOKING_CREATED, { carId: car.id });
    setSuccess(true);
  }

  return (
    <div className="fixed inset-0 z-40 flex items-center justify-center bg-black/40">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-md p-6">
        <h2 className="text-lg font-bold text-gray-900 mb-2">
          Book {car.year} {car.make} {car.model}
        </h2>
        <p className="text-sm text-gray-500 mb-4">${car.daily_price}/day &middot; {car.location}</p>

        {success ? (
          <div className="text-center py-6">
            <p className="text-green-600 font-semibold mb-4">Booking confirmed!</p>
            <button onClick={onClose}
              className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700">Close</button>
          </div>
        ) : (
          <>
            <ErrorAlert message={error} onDismiss={() => setError('')} />
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
                  <input type="date" required value={startDate} onChange={e => setStartDate(e.target.value)}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
                  <input type="date" required value={endDate} onChange={e => setEndDate(e.target.value)}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none" />
                </div>
              </div>
              {days > 0 && (
                <div className="p-3 bg-gray-50 rounded-lg text-sm">
                  <span className="text-gray-600">{days} day{days !== 1 ? 's' : ''} &times; ${car.daily_price}/day = </span>
                  <span className="font-bold text-gray-900">${total.toFixed(2)}</span>
                </div>
              )}
              <div className="flex gap-3">
                <button type="submit" disabled={loading}
                  className="flex-1 py-2 bg-purple-600 text-white font-medium rounded-lg hover:bg-purple-700 disabled:opacity-50">
                  {loading ? 'Booking...' : 'Confirm Booking'}
                </button>
                <button type="button" onClick={onClose}
                  className="flex-1 py-2 border border-gray-300 text-gray-600 rounded-lg hover:bg-gray-50">Cancel</button>
              </div>
            </form>
          </>
        )}
      </div>
    </div>
  );
}
