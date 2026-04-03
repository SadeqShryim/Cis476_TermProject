import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Clock, DollarSign, MapPin, Tag, PlusCircle } from 'lucide-react';
import CreateCar from '../components/CreateCar';

export default function Dashboard() {
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [cars, setCars] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [activeTab, setActiveTab] = useState('browse'); // browse, my-cars, bookings
  const [loading, setLoading] = useState(true);
  const [showCreateCar, setShowCreateCar] = useState(false);

  // For booking/payment
  const [message, setMessage] = useState('');

  useEffect(() => {
    setLoading(true);
    fetchProfile();
    if (activeTab === 'browse') {
      fetchAllCars();
    } else if (activeTab === 'my-cars') {
      fetchMyCars();
    } else if (activeTab === 'bookings') {
      fetchMyBookings();
    }
  }, [activeTab]);

  const fetchProfile = async () => {
    const res = await fetch('/api/user/profile', {
      headers: { 'X-Auth-Token': localStorage.getItem('token') }
    });
    if (res.ok) setProfile(await res.json());
  };

  const fetchAllCars = async () => {
    const res = await fetch('/api/cars/');
    if (res.ok) setCars(await res.json());
    setLoading(false);
  };

  const fetchMyCars = async () => {
    const res = await fetch('/api/cars/my-cars', {
      headers: { 'X-Auth-Token': localStorage.getItem('token') }
    });
    if (res.ok) setCars(await res.json());
    setLoading(false);
  };
  
  const fetchMyBookings = async () => {
    const res = await fetch('/api/bookings/as-renter', {
      headers: { 'X-Auth-Token': localStorage.getItem('token') }
    });
    if (res.ok) setBookings(await res.json());
    setLoading(false);
  };

  const handleBook = async (carId, ownerId) => {
    // Simple 3-day booking from today for demo purposes
    const start = new Date().toISOString().split('T')[0];
    const end = new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
    
    try {
      const res = await fetch('/api/bookings/', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'X-Auth-Token': localStorage.getItem('token')
        },
        body: JSON.stringify({ car_id: carId, owner_id: ownerId, start_date: start, end_date: end })
      });
      
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail);
      
      setMessage(`Successfully booked car for 3 days! Finalizing payment...`);
      
      const paymentRes = await fetch('/api/payments/', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'X-Auth-Token': localStorage.getItem('token')
        },
        body: JSON.stringify({ booking_id: data.booking.id })
      });

      if (!paymentRes.ok) throw new Error('Payment failed');

      setMessage(`Successfully booked and paid for car!`);
      fetchProfile(); // update balance
      setActiveTab('bookings'); // Switch to bookings tab

    } catch (err) {
      alert(err.message);
    }
  };

  const handleCarCreated = () => {
    setShowCreateCar(false);
    fetchMyCars();
  }

  const renderCars = () => (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1.5rem' }}>
      {cars.map((car, idx) => (
        <div key={car.id} className={`glass-card delay-${(idx % 3 + 1) * 100}`}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
            <h3 style={{ margin: 0 }}>{car.year} {car.make} {car.model}</h3>
            <span className="badge badge-primary">${car.daily_price}/day</span>
          </div>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '1.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><MapPin size={16}/> {car.location}</div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><Clock size={16}/> {car.mileage} miles</div>
          </div>

          {car.features && car.features.length > 0 && (
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '1.5rem' }}>
              {car.features.map((f, i) => <span key={i} className="badge badge-warning"><Tag size={12} style={{ display: 'inline', marginRight: '4px' }}/> {f}</span>)}
            </div>
          )}

          {activeTab === 'browse' && car.owner_id !== user.id && (
            <button className="btn btn-primary" style={{ width: '100%' }} onClick={() => handleBook(car.id, car.owner_id)}>
              <DollarSign size={16}/> Book Now
            </button>
          )}
        </div>
      ))}
      {cars.length === 0 && (
        <div style={{ gridColumn: '1 / -1', textAlign: 'center', color: 'var(--text-muted)', padding: '3rem' }}>
          {activeTab === 'my-cars' ? 'You have no listings. Click "List New Car" to get started.' : 'No cars available for these criteria.'}
        </div>
      )}
    </div>
  );

  const renderBookings = () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {bookings.map(booking => (
        <div key={booking.id} className="glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <h4 style={{ margin: '0 0 0.5rem 0' }}>Booking #{booking.id}</h4>
              <p style={{ margin: 0, color: 'var(--text-muted)' }}>
                {new Date(booking.start_date).toLocaleDateString()} - {new Date(booking.end_date).toLocaleDateString()}
              </p>
            </div>
            <div style={{ textAlign: 'right' }}>
              <div className={`badge badge-${booking.status === 'confirmed' ? 'success' : 'warning'}`} style={{ marginBottom: '0.5rem' }}>
                {booking.status}
              </div>
              <div>Total: ${booking.total_price.toFixed(2)}</div>
            </div>
          </div>
        </div>
      ))}
      {bookings.length === 0 && (
        <div style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '3rem' }}>
          You have no bookings.
        </div>
      )}
    </div>
  );

  return (
    <div className="container animate-fade-in">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h2>Dashboard</h2>
        {profile && (
          <div className="badge badge-success" style={{ fontSize: '1.1rem', padding: '0.5rem 1rem' }}>
            Balance: ${profile.balance.toFixed(2)}
          </div>
        )}
      </div>

      {message && (
        <div style={{ padding: '1rem', background: 'rgba(16, 185, 129, 0.1)', border: '1px solid var(--success)', borderRadius: 'var(--radius-md)', color: '#34d399', marginBottom: '2rem' }}>
          {message}
          <button style={{ float: 'right', background: 'none', border: 'none', color: '#34d399', cursor: 'pointer' }} onClick={() => setMessage('')}>✕</button>
        </div>
      )}

      <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', borderBottom: '1px solid var(--border-light)', paddingBottom: '1rem' }}>
        <button className={`btn ${activeTab === 'browse' ? 'btn-primary' : 'btn-secondary'}`} onClick={() => setActiveTab('browse')}>Find Cars</button>
        <button className={`btn ${activeTab === 'my-cars' ? 'btn-primary' : 'btn-secondary'}`} onClick={() => setActiveTab('my-cars')}>My Listings</button>
        <button className={`btn ${activeTab === 'bookings' ? 'btn-primary' : 'btn-secondary'}`} onClick={() => setActiveTab('bookings')}>My Bookings</button>
      </div>

      {activeTab === 'my-cars' && (
        <div style={{ marginBottom: '2rem' }}>
          <button className="btn btn-primary" onClick={() => setShowCreateCar(!showCreateCar)}>
            <PlusCircle size={16} style={{ marginRight: '0.5rem' }} />
            {showCreateCar ? 'Cancel' : 'List New Car'}
          </button>
          {showCreateCar && <CreateCar onCarCreated={handleCarCreated} />}
        </div>
      )}

      {loading ? (
        <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>Loading...</div>
      ) : (
        <>
          {(activeTab === 'browse' || activeTab === 'my-cars') && renderCars()}
          {activeTab === 'bookings' && renderBookings()}
        </>
      )}
    </div>
  );
}
