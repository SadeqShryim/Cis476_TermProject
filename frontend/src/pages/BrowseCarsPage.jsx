/**
 * BrowseCarsPage — search and browse all active car listings.
 *
 * Mediator Role: ConcreteColleague ("CarList")
 * Listens for: CAR_LISTED, CAR_UPDATED, CAR_DELETED, BOOKING_CREATED, CAR_UNWATCHED
 * Action:      Re-fetches car listings to show up-to-date data.
 */
import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useColleague } from '../hooks/useColleague';
import { EVENTS } from '../patterns/mediator';
import * as api from '../api/client';
import CarCard from '../components/cars/CarCard';
import CarSearchForm from '../components/cars/CarSearchForm';
import BookingModal from '../components/bookings/BookingModal';
import LoadingSpinner from '../components/shared/LoadingSpinner';

export default function BrowseCarsPage() {
  const navigate = useNavigate();
  const [cars, setCars] = useState([]);
  const [watchedIds, setWatchedIds] = useState(new Set());
  const [loading, setLoading] = useState(true);
  const [bookingCar, setBookingCar] = useState(null);

  const fetchWatched = useCallback(async () => {
    const { ok, data } = await api.get('/user/watched');
    if (ok) setWatchedIds(new Set(data.map(w => (w.car || w).id)));
  }, []);

  const fetchCars = useCallback(async () => {
    setLoading(true);
    const { ok, data } = await api.get('/cars/');
    if (ok) setCars(data);
    await fetchWatched();
    setLoading(false);
  }, [fetchWatched]);

  // Register as CarList colleague to receive refresh events
  useColleague('CarList', (event) => {
    if ([EVENTS.CAR_LISTED, EVENTS.CAR_UPDATED, EVENTS.CAR_DELETED,
         EVENTS.BOOKING_CREATED, EVENTS.CAR_UNWATCHED].includes(event)) {
      fetchCars();
    }
  });

  useEffect(() => { fetchCars(); }, [fetchCars]);

  async function handleSearch(filters) {
    setLoading(true);
    const { ok, data } = await api.post('/bookings/search', filters);
    if (ok) setCars(Array.isArray(data) ? data : data.results ?? []);
    setLoading(false);
  }

  async function handleWatch(carId, targetPrice) {
    const { ok } = await api.post('/user/watch', { car_id: carId, target_price: targetPrice });
    if (ok) setWatchedIds(prev => new Set(prev).add(carId));
  }

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-4">Browse Cars</h1>
      <CarSearchForm onSearch={handleSearch} onClear={fetchCars} />
      {cars.length === 0 ? (
        <p className="text-gray-500 text-center py-12">No cars found.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {cars.map(car => (
            <CarCard key={car.id} car={car}
              isWatched={watchedIds.has(car.id)}
              onBook={setBookingCar}
              onWatch={handleWatch}
              onMessage={(ownerId) => navigate(`/dashboard/messages/${ownerId}`)}
            />
          ))}
        </div>
      )}
      {bookingCar && <BookingModal car={bookingCar} onClose={() => setBookingCar(null)} />}
    </div>
  );
}
