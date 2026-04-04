/**
 * PaymentButton — processes a payment for a booking.
 *
 * Mediator Role: ConcreteColleague ("PaymentButton")
 * Sends: PAYMENT_PROCESSED
 *
 * This component uses the Proxy pattern on the backend, where PaymentProxy
 * validates, logs, and delegates the actual payment processing.
 */
import { useState } from 'react';
import { CreditCard } from 'lucide-react';
import { useColleague } from '../../hooks/useColleague';
import { EVENTS } from '../../patterns/mediator';
import * as api from '../../api/client';

export default function PaymentButton({ bookingId, ownerId, amount, onPaid }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const { send } = useColleague('PaymentButton', () => {});

  async function handlePay() {
    setError('');
    setLoading(true);
    const { ok, error: err } = await api.post('/payments/', {
      booking_id: bookingId,
      owner_id: ownerId,
      amount,
    });
    setLoading(false);
    if (!ok) return setError(err);
    send(EVENTS.PAYMENT_PROCESSED, { bookingId, amount });
    if (onPaid) onPaid();
  }

  return (
    <div>
      <button onClick={handlePay} disabled={loading}
        className="flex items-center gap-1 px-3 py-1.5 text-xs font-medium bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50">
        <CreditCard size={12} />
        {loading ? 'Processing...' : `Pay $${amount?.toFixed(2)}`}
      </button>
      {error && <p className="text-xs text-red-500 mt-1">{error}</p>}
    </div>
  );
}
