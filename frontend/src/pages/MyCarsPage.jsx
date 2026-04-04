/**
 * MyCarsPage — owner's car listings with create, edit, and delete.
 */
import { useState, useEffect, useCallback } from 'react';
import { Plus } from 'lucide-react';
import { useColleague } from '../hooks/useColleague';
import { EVENTS } from '../patterns/mediator';
import * as api from '../api/client';
import CarCard from '../components/cars/CarCard';
import CarForm from '../components/cars/CarForm';
import LoadingSpinner from '../components/shared/LoadingSpinner';

export default function MyCarsPage() {
  const [cars, setCars] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editCar, setEditCar] = useState(null);

  const fetchCars = useCallback(async () => {
    setLoading(true);
    const { ok, data } = await api.get('/cars/my-cars');
    if (ok) setCars(data);
    setLoading(false);
  }, []);

  useColleague('MyCarsOwnerList', (event) => {
    if ([EVENTS.CAR_LISTED, EVENTS.CAR_UPDATED, EVENTS.CAR_DELETED].includes(event)) {
      fetchCars();
    }
  });

  useEffect(() => { fetchCars(); }, [fetchCars]);

  async function handleDelete(carId) {
    await api.del(`/cars/${carId}`);
    fetchCars();
  }

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-bold text-gray-900">My Cars</h1>
        <button onClick={() => { setEditCar(null); setShowForm(true); }}
          className="flex items-center gap-1 px-4 py-2 text-sm font-medium bg-purple-600 text-white rounded-lg hover:bg-purple-700">
          <Plus size={16} /> New Listing
        </button>
      </div>

      {cars.length === 0 ? (
        <p className="text-gray-500 text-center py-12">You haven&apos;t listed any cars yet.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {cars.map(car => (
            <CarCard key={car.id} car={car}
              onEdit={(c) => { setEditCar(c); setShowForm(true); }}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}

      {showForm && (
        <CarForm car={editCar}
          onClose={() => setShowForm(false)}
          onSaved={() => { setShowForm(false); fetchCars(); }}
        />
      )}
    </div>
  );
}
