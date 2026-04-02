import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Auth() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  
  // Registration specific
  const [q1, setQ1] = useState('');
  const [a1, setA1] = useState('');
  const [q2, setQ2] = useState('');
  const [a2, setA2] = useState('');
  const [q3, setQ3] = useState('');
  const [a3, setA3] = useState('');

  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const endpoint = isLogin ? '/api/auth/login' : '/api/auth/register';
      const payload = isLogin 
        ? { email, password }
        : {
            email,
            password,
            security_questions: [
              { question: q1, answer: a1 },
              { question: q2, answer: a2 },
              { question: q3, answer: a3 }
            ]
          };

      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      
      if (!res.ok) {
        throw new Error(data.detail || 'Authentication failed');
      }

      if (isLogin) {
        login(data.user, data.token);
        navigate('/dashboard');
      } else {
        // Auto-login after registration is not implemented in backend, switch to login
        setIsLogin(true);
        setError('Registration successful. Please log in.');
      }
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="container" style={{ maxWidth: '500px', marginTop: '4rem' }}>
      <div className="glass-card animate-fade-in">
        <h2 style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
          {isLogin ? 'Welcome Back' : 'Create Account'}
        </h2>
        
        {error && (
          <div style={{ padding: '0.75rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid var(--danger)', borderRadius: 'var(--radius-md)', color: '#fca5a5', marginBottom: '1.5rem', fontSize: '0.9rem' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email Address</label>
            <input 
              type="email" 
              required 
              value={email} 
              onChange={e => setEmail(e.target.value)} 
              placeholder="you@example.com"
            />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input 
              type="password" 
              required 
              value={password} 
              onChange={e => setPassword(e.target.value)} 
              placeholder="••••••••"
            />
          </div>

          {!isLogin && (
            <div style={{ marginTop: '2rem', paddingTop: '1rem', borderTop: '1px solid var(--border-light)' }}>
              <h3>Security Questions</h3>
              <p style={{ fontSize: '0.85rem' }}>Required for password recovery</p>
              
              <div className="form-group">
                <label>Question 1</label>
                <input required value={q1} onChange={e => setQ1(e.target.value)} placeholder="e.g. First pet's name" />
                <input required value={a1} onChange={e => setA1(e.target.value)} placeholder="Answer" style={{ marginTop: '0.5rem' }} />
              </div>

              <div className="form-group">
                <label>Question 2</label>
                <input required value={q2} onChange={e => setQ2(e.target.value)} placeholder="e.g. Mother's maiden name" />
                <input required value={a2} onChange={e => setA2(e.target.value)} placeholder="Answer" style={{ marginTop: '0.5rem' }} />
              </div>

              <div className="form-group">
                <label>Question 3</label>
                <input required value={q3} onChange={e => setQ3(e.target.value)} placeholder="e.g. Favorite color" />
                <input required value={a3} onChange={e => setA3(e.target.value)} placeholder="Answer" style={{ marginTop: '0.5rem' }} />
              </div>
            </div>
          )}

          <button type="submit" className="btn btn-primary" style={{ width: '100%', marginTop: '1rem' }}>
            {isLogin ? 'Sign In' : 'Sign Up'}
          </button>
        </form>

        <div style={{ textAlign: 'center', marginTop: '1.5rem', fontSize: '0.9rem' }}>
          <span style={{ color: 'var(--text-muted)' }}>
            {isLogin ? "Don't have an account? " : "Already have an account? "}
          </span>
          <button 
            type="button" 
            onClick={() => setIsLogin(!isLogin)} 
            style={{ background: 'none', border: 'none', color: 'var(--primary)', cursor: 'pointer', fontWeight: '500' }}
          >
            {isLogin ? 'Register' : 'Login'}
          </button>
        </div>
      </div>
    </div>
  );
}
