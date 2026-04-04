/**
 * BookingCard — displays a single booking with status, Cancel, Pay, and Review actions.
 */
import { useState } from 'react';
import { Calendar, DollarSign, XCircle } from 'lucide-react';
import PaymentButton from '../payments/PaymentButton';
import ReviewForm from '../reviews/ReviewForm';

export default function BookingCard({ booking, role, onCancelled }) {
  const [showReview, setShowReview] = useState(false);

  const isPast = new Date(booking.end_date) < new Date();
  const canPay = role === 'renter' && booking.status === 'confirmed' && !booking.paid;
  const canCancel = booking.status === 'confirmed' && !booking.paid;
  const canReview = booking.status === 'confirmed' && booking.paid && isPast;

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
      <div className="flex items-start justify-between mb-2">
        <h3 className="font-semibold text-gray-900">Booking</h3>
        <span className={`px-2 py-0.5 text-xs font-medium rounded-full
          ${booking.status === 'confirmed' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
          {booking.status}
        </span>
      </div>

      <div className="space-y-1 text-sm text-gray-600 mb-3">
        <div className="flex items-center gap-2">
          <Calendar size={14} />
          {booking.start_date} to {booking.end_date}
        </div>
        <div className="flex items-center gap-2">
          <DollarSign size={14} />
          Total: ${booking.total_price?.toFixed(2)}
          {booking.paid && <span className="text-green-600 font-medium ml-2">Paid</span>}
        </div>
        <div className="text-xs text-gray-400">Car: {booking.car_id}</div>
      </div>

      <div className="flex flex-wrap gap-2 pt-3 border-t border-gray-100">
        {canPay && (
          <PaymentButton
            bookingId={booking.id}
            ownerId={booking.owner_id}
            amount={booking.total_price}
            onPaid={onCancelled}
          />
        )}
        {canCancel && (
          <button onClick={() => onCancelled(booking.id)}
            className="flex items-center gap-1 px-3 py-1.5 text-xs font-medium border border-red-300 text-red-600 rounded-lg hover:bg-red-50">
            <XCircle size={12} /> Cancel
          </button>
        )}
        {canReview && (
          <button onClick={() => setShowReview(true)}
            className="px-3 py-1.5 text-xs font-medium border border-purple-300 text-purple-700 rounded-lg hover:bg-purple-50">
            Leave Review
          </button>
        )}
      </div>

      {showReview && (
        <ReviewForm bookingId={booking.id} onClose={() => setShowReview(false)} />
      )}
    </div>
  );
}
