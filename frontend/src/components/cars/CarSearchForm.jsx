/**
 * CarSearchForm — search filters for browsing cars.
 * Calls POST /api/bookings/search on the backend.
 */
import { useState } from 'react';
import { Search } from 'lucide-react';

export default function CarSearchForm({ onSearch, onClear }) {
  const [location, setLocation] = useState('');
  const [make, setMake] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  function handleSubmit(e) {
    e.preventDefault();
    const filters = {};
    if (location) filters.location = location;
    if (make) filters.make = make;
    if (maxPrice) filters.max_price = parseFloat(maxPrice);
    if (startDate) filters.start_date = startDate;
    if (endDate) filters.end_date = endDate;
    onSearch(filters);
  }

  function handleClear() {
    setLocation(''); setMake(''); setMaxPrice(''); setStartDate(''); setEndDate('');
    onClear();
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white border border-gray-200 rounded-xl p-4 mb-6">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
        <input type="text" placeholder="Location" value={location} onChange={e => setLocation(e.target.value)}
          className="px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none" />
        <input type="text" placeholder="Make" value={make} onChange={e => setMake(e.target.value)}
          className="px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none" />
        <input type="number" placeholder="Max $/day" value={maxPrice} onChange={e => setMaxPrice(e.target.value)}
          className="px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none" />
        <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)}
          className="px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none" />
        <input type="date" value={endDate} onChange={e => setEndDate(e.target.value)}
          className="px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none" />
      </div>
      <div className="flex gap-2 mt-3">
        <button type="submit"
          className="flex items-center gap-1 px-4 py-2 text-sm font-medium bg-purple-600 text-white rounded-lg hover:bg-purple-700">
          <Search size={14} /> Search
        </button>
        <button type="button" onClick={handleClear}
          className="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50">
          Clear
        </button>
      </div>
    </form>
  );
}
