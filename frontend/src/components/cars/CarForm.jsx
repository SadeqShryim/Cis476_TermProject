/**
 * CarForm — form for creating or editing a car listing.
 *
 * Mediator Role: ConcreteColleague ("CarForm")
 * Sends: CAR_LISTED (on create), CAR_UPDATED (on edit)
 */
import { useState, useEffect } from 'react';
import { useColleague } from '../../hooks/useColleague';
import { EVENTS } from '../../patterns/mediator';
import * as api from '../../api/client';
import ErrorAlert from '../shared/ErrorAlert';

export default function CarForm({ car, onClose, onSaved }) {
  const isEdit = !!car;
  const [make, setMake] = useState(car?.make || '');
  const [model, setModel] = useState(car?.model || '');
  const [year, setYear] = useState(car?.year || '');
  const [mileage, setMileage] = useState(car?.mileage || '');
  const [dailyPrice, setDailyPrice] = useState(car?.daily_price || '');
  const [location, setLocation] = useState(car?.location || '');
  const [features, setFeatures] = useState(car?.features?.join(', ') || '');
  const [availStart, setAvailStart] = useState(car?.availability?.[0]?.start || '');
  const [availEnd, setAvailEnd] = useState(car?.availability?.[0]?.end || '');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { send } = useColleague('CarForm', () => {});

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setLoading(true);

    const featureList = features.split(',').map(f => f.trim()).filter(Boolean);
    const availability = (availStart && availEnd) ? [{ start: availStart, end: availEnd }] : [];

    if (isEdit) {
      // Update only price and availability
      const { ok, error: err } = await api.put(`/cars/${car.id}`, {
        daily_price: parseFloat(dailyPrice),
        availability,
      });
      setLoading(false);
      if (!ok) return setError(err);
      send(EVENTS.CAR_UPDATED, { carId: car.id });
    } else {
      const { ok, error: err } = await api.post('/cars/', {
        make, model,
        year: parseInt(year),
        mileage: parseInt(mileage),
        daily_price: parseFloat(dailyPrice),
        location,
        features: featureList,
        availability,
      });
      setLoading(false);
      if (!ok) return setError(err);
      send(EVENTS.CAR_LISTED, {});
    }
    onSaved();
  }

  return (
    <div className="fixed inset-0 z-40 flex items-center justify-center bg-black/40">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-lg p-6 max-h-[90vh] overflow-y-auto">
        <h2 className="text-lg font-bold text-gray-900 mb-4">{isEdit ? 'Edit Car Listing' : 'Create New Listing'}</h2>
        <ErrorAlert message={error} onDismiss={() => setError('')} />
        <form onSubmit={handleSubmit} className="space-y-3">
          {!isEdit && (
            <>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Make</label>
                  <input required value={make} onChange={e => setMake(e.target.value)}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Model</label>
                  <input required value={model} onChange={e => setModel(e.target.value)}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none" />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Year</label>
                  <input type="number" required value={year} onChange={e => setYear(e.target.value)}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Mileage</label>
                  <input type="number" required value={mileage} onChange={e => setMileage(e.target.value)}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none" />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
                <input required value={location} onChange={e => setLocation(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Features (comma separated)</label>
                <input value={features} onChange={e => setFeatures(e.target.value)} placeholder="GPS, Bluetooth, Sunroof"
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none" />
              </div>
            </>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Daily Price ($)</label>
            <input type="number" step="0.01" required value={dailyPrice} onChange={e => setDailyPrice(e.target.value)}
              className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none" />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Available From</label>
              <input type="date" value={availStart} onChange={e => setAvailStart(e.target.value)}
                className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Available Until</label>
              <input type="date" value={availEnd} onChange={e => setAvailEnd(e.target.value)}
                className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none" />
            </div>
          </div>

          <div className="flex gap-3 pt-2">
            <button type="submit" disabled={loading}
              className="flex-1 py-2 bg-purple-600 text-white font-medium rounded-lg hover:bg-purple-700 disabled:opacity-50">
              {loading ? 'Saving...' : isEdit ? 'Update' : 'Create Listing'}
            </button>
            <button type="button" onClick={onClose}
              className="flex-1 py-2 border border-gray-300 text-gray-600 rounded-lg hover:bg-gray-50">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
