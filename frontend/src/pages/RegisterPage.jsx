/**
 * RegisterPage — registration form with email, password, and 3 security questions.
 * On success, auto-logs in and navigates to /dashboard.
 */
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import * as api from '../api/client';
import ErrorAlert from '../components/shared/ErrorAlert';

const QUESTION_OPTIONS = [
  "What is your mother's maiden name?",
  'What was the name of your first pet?',
  'What city were you born in?',
  'What is your favorite movie?',
  'What was the name of your elementary school?',
  'What is your favorite food?',
];

export default function RegisterPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [questions, setQuestions] = useState([
    { question: QUESTION_OPTIONS[0], answer: '' },
    { question: QUESTION_OPTIONS[1], answer: '' },
    { question: QUESTION_OPTIONS[2], answer: '' },
  ]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  function updateQuestion(idx, field, value) {
    setQuestions(prev => prev.map((q, i) => i === idx ? { ...q, [field]: value } : q));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    if (password !== confirmPassword) return setError('Passwords do not match.');
    if (questions.some(q => !q.answer.trim())) return setError('Please answer all security questions.');

    setLoading(true);
    const { ok, data, error: err } = await api.post('/auth/register', {
      email,
      password,
      security_questions: questions,
    });
    setLoading(false);
    if (!ok) return setError(err);

    // Auto-login after registration
    const loginRes = await api.post('/auth/login', { email, password });
    if (loginRes.ok) {
      login(loginRes.data.user, loginRes.data.token);
      navigate('/dashboard');
    } else {
      navigate('/login');
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 to-white px-4 py-8">
      <div className="w-full max-w-lg bg-white rounded-xl shadow-lg p-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-6 text-center">Create Your Account</h1>
        <ErrorAlert message={error} onDismiss={() => setError('')} />
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input type="email" required value={email} onChange={e => setEmail(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input type="password" required value={password} onChange={e => setPassword(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label>
            <input type="password" required value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none" />
          </div>

          <hr className="my-4" />
          <h2 className="text-lg font-semibold text-gray-900">Security Questions</h2>
          <p className="text-sm text-gray-500 mb-2">These are used to recover your password if you forget it.</p>

          {questions.map((q, idx) => (
            <div key={idx} className="space-y-2 p-3 bg-gray-50 rounded-lg">
              <label className="block text-sm font-medium text-gray-700">Question {idx + 1}</label>
              <select value={q.question} onChange={e => updateQuestion(idx, 'question', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-purple-500 outline-none">
                {QUESTION_OPTIONS.map(opt => (
                  <option key={opt} value={opt}>{opt}</option>
                ))}
              </select>
              <input type="text" required placeholder="Your answer" value={q.answer}
                onChange={e => updateQuestion(idx, 'answer', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none" />
            </div>
          ))}

          <button type="submit" disabled={loading}
            className="w-full py-2 bg-purple-600 text-white font-medium rounded-lg hover:bg-purple-700 disabled:opacity-50">
            {loading ? 'Creating Account...' : 'Sign Up'}
          </button>
        </form>
        <p className="mt-4 text-center text-sm text-gray-600">
          Already have an account?{' '}
          <Link to="/login" className="text-purple-600 hover:underline">Log In</Link>
        </p>
      </div>
    </div>
  );
}
