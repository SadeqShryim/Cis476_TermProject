import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div className="container animate-fade-in" style={{ textAlign: 'center', paddingTop: '4rem' }}>
      <h1 style={{ fontSize: '4rem', marginBottom: '1.5rem', lineHeight: '1.1' }}>
        Rent the perfect car, <br />
        <span className="text-gradient">directly from local owners.</span>
      </h1>
      <p style={{ fontSize: '1.2rem', maxWidth: '600px', margin: '0 auto 3rem auto' }}>
        DriveShare is the premier peer-to-peer car sharing platform. Skip the rental counter and choose from hundreds of unique vehicles.
      </p>
      
      <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
        <Link to="/auth" className="btn btn-primary" style={{ padding: '1rem 2rem', fontSize: '1.1rem' }}>
          Find a Car
        </Link>
        <Link to="/auth" className="btn btn-secondary" style={{ padding: '1rem 2rem', fontSize: '1.1rem' }}>
          List Your Car
        </Link>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '2rem', marginTop: '6rem' }}>
        <div className="glass-card delay-100">
          <h3>Wide Selection</h3>
          <p>Find the perfect vehicle for any occasion, from luxury sedans to rugged SUVs.</p>
        </div>
        <div className="glass-card delay-200">
          <h3>Lower Prices</h3>
          <p>Rent directly from owners and save up to 30% compared to traditional rental companies.</p>
        </div>
        <div className="glass-card delay-300">
          <h3>Fully Insured</h3>
          <p>Every trip is covered by our comprehensive insurance policy and 24/7 roadside assistance.</p>
        </div>
      </div>
    </div>
  );
}
