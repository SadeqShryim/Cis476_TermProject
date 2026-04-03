import { useState } from 'react';
import { useAuth } from '../context/AuthContext';

export default function CreateCar({ onCarCreated }) {
  const { user } = useAuth();
  const [make, setMake] = useState('');
  const [model, setModel] = useState('');
  const [year, setYear] = useState('');
  const [price, setPrice] = useState('');
  const [location, setLocation] = useState('');
  const [mileage, setMileage] = useState('');
  const [features, setFeatures] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const res = await fetch('/api/cars/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Auth-Token': localStorage.getItem('token'),
        },
        body: JSON.stringify({
          make,
          model,
          year: parseInt(year),
          daily_price: parseFloat(price),
          location,
          mileage: parseInt(mileage),
          features: features.split(',').map(f => f.trim()),
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || 'Failed to create car');
      }

      setSuccess('Car listed successfully!');
      // Reset form
      setMake('');
      setModel('');
      setYear('');
      setPrice('');
      setLocation('');
      setMileage('');
      setFeatures('');

      if (onCarCreated) {
        onCarCreated();
      }
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="glass-card" style={{ marginTop: '2rem' }}>
      <h3>List a New Car</h3>
      {error && <div className="alert alert-danger">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Make</label>
          <input type="text" required value={make} onChange={(e) => setMake(e.target.value)} />
        </div>
        <div className="form-group">
          <label>Model</label>
          <input type="text" required value={model} onChange={(e) => setModel(e.target.value)} />
        </div>
        <div className="form-group">
          <label>Year</label>
          <input type="number" required value={year} onChange={(e) => setYear(e.target.value)} />
        </div>
        <div className="form-group">
          <label>Daily Price</label>
          <input type="number" required value={price} onChange={(e) => setPrice(e.target.value)} />
        </div>
        <div className="form-group">
          <label>Location</label>
          <input type="text" required value={location} onChange={(e) => setLocation(e.target.value)} />
        </div>
        <div className="form-group">
          <label>Mileage</label>
          <input type="number" required value={mileage} onChange={(e) => setMileage(e.target.value)} />
        </div>
        <div className="form-group">
          <label>Features (comma-separated)</label>
          <input type="text" value={features} onChange={(e) => setFeatures(e.target.value)} />
        </div>
        <button type="submit" className="btn btn-primary" style={{ marginTop: '1rem' }}>
          List Car
        </button>
      </form>
    </div>
  );
}
