/**
 * ForgotPasswordPage — 3-step password recovery flow:
 *   Step 1: Enter email
 *   Step 2: Answer security questions
 *   Step 3: Set new password
 *
 * Uses the Chain of Responsibility pattern on the backend
 * (3 security questions verified in sequence).
 */
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import * as api from '../api/client';
import ErrorAlert from '../components/shared/ErrorAlert';

export default function ForgotPasswordPage() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [email, setEmail] = useState('');
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState(['', '', '']);
  const [newPassword, setNewPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Step 1: fetch security questions for the email
  async function handleEmailSubmit(e) {
    e.preventDefault();
    setError('');
    setLoading(true);
    const { ok, data, error: err } = await api.get(`/auth/security-questions/${encodeURIComponent(email)}`);
    setLoading(false);
    if (!ok) return setError(err);
    setQuestions(data.questions);
    setStep(2);
  }

  // Step 2 + 3: submit answers and new password
  async function handleRecoverSubmit(e) {
    e.preventDefault();
    setError('');
    if (!newPassword) return setError('Please enter a new password.');
    setLoading(true);
    const { ok, error: err } = await api.post('/auth/recover-password', {
      email,
      answers,
      new_password: newPassword,
    });
    setLoading(false);
    if (!ok) return setError(err);
    navigate('/login');
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 to-white px-4">
      <div className="w-full max-w-md bg-white rounded-xl shadow-lg p-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-6 text-center">Recover Your Password</h1>
        <ErrorAlert message={error} onDismiss={() => setError('')} />

        {step === 1 && (
          <form onSubmit={handleEmailSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
              <input type="email" required value={email} onChange={e => setEmail(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none" />
            </div>
            <button type="submit" disabled={loading}
              className="w-full py-2 bg-purple-600 text-white font-medium rounded-lg hover:bg-purple-700 disabled:opacity-50">
              {loading ? 'Looking up...' : 'Next'}
            </button>
          </form>
        )}

        {step === 2 && (
          <form onSubmit={handleRecoverSubmit} className="space-y-4">
            {questions.map((q, idx) => (
              <div key={idx}>
                <label className="block text-sm font-medium text-gray-700 mb-1">{q}</label>
                <input type="text" required value={answers[idx]}
                  onChange={e => setAnswers(prev => prev.map((a, i) => i === idx ? e.target.value : a))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none" />
              </div>
            ))}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">New Password</label>
              <input type="password" required value={newPassword} onChange={e => setNewPassword(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none" />
            </div>
            <button type="submit" disabled={loading}
              className="w-full py-2 bg-purple-600 text-white font-medium rounded-lg hover:bg-purple-700 disabled:opacity-50">
              {loading ? 'Resetting...' : 'Reset Password'}
            </button>
          </form>
        )}

        <p className="mt-4 text-center text-sm text-gray-600">
          <Link to="/login" className="text-purple-600 hover:underline">Back to Login</Link>
        </p>
      </div>
    </div>
  );
}
