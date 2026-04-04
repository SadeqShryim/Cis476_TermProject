/**
 * ReviewForm — star rating (1-5) + comment form for completed bookings.
 *
 * Mediator Role: ConcreteColleague ("ReviewForm")
 * Sends: REVIEW_SUBMITTED
 */
import { useState } from 'react';
import { Star } from 'lucide-react';
import { useColleague } from '../../hooks/useColleague';
import { EVENTS } from '../../patterns/mediator';
import * as api from '../../api/client';
import ErrorAlert from '../shared/ErrorAlert';

export default function ReviewForm({ bookingId, onClose }) {
  const [rating, setRating] = useState(0);
  const [hover, setHover] = useState(0);
  const [comment, setComment] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const { send } = useColleague('ReviewForm', () => {});

  async function handleSubmit(e) {
    e.preventDefault();
    if (rating === 0) return setError('Please select a rating.');
    setError('');
    setLoading(true);
    const { ok, error: err } = await api.post('/reviews/', {
      booking_id: bookingId,
      rating,
      comment,
    });
    setLoading(false);
    if (!ok) return setError(err);
    send(EVENTS.REVIEW_SUBMITTED, { bookingId });
    setSuccess(true);
  }

  if (success) {
    return (
      <div className="mt-3 p-3 bg-green-50 rounded-lg text-center">
        <p className="text-green-700 text-sm font-medium">Review submitted!</p>
        <button onClick={onClose} className="mt-2 text-xs text-purple-600 hover:underline">Close</button>
      </div>
    );
  }

  return (
    <div className="mt-3 p-4 bg-gray-50 rounded-lg border border-gray-200">
      <h4 className="text-sm font-semibold text-gray-900 mb-2">Leave a Review</h4>
      <ErrorAlert message={error} onDismiss={() => setError('')} />
      <form onSubmit={handleSubmit} className="space-y-3">
        <div className="flex gap-1">
          {[1, 2, 3, 4, 5].map(star => (
            <button key={star} type="button"
              onMouseEnter={() => setHover(star)}
              onMouseLeave={() => setHover(0)}
              onClick={() => setRating(star)}>
              <Star size={20}
                className={star <= (hover || rating) ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'} />
            </button>
          ))}
        </div>
        <textarea value={comment} onChange={e => setComment(e.target.value)}
          placeholder="Share your experience..."
          className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none resize-none"
          rows={3} />
        <div className="flex gap-2">
          <button type="submit" disabled={loading}
            className="px-4 py-1.5 text-xs bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50">
            {loading ? 'Submitting...' : 'Submit'}
          </button>
          <button type="button" onClick={onClose}
            className="px-4 py-1.5 text-xs text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50">
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
