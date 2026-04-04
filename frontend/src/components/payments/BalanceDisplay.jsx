/**
 * BalanceDisplay — shows the current user balance in the Navbar.
 *
 * Mediator Role: ConcreteColleague ("BalanceDisplay")
 * Listens for: PAYMENT_PROCESSED, USER_LOGGED_IN, BOOKING_CREATED
 * Action:      Re-fetches the user profile to update the displayed balance.
 */
import { useState, useEffect, useCallback } from 'react';
import { Wallet } from 'lucide-react';
import { useColleague } from '../../hooks/useColleague';
import { EVENTS } from '../../patterns/mediator';
import { useAuth } from '../../context/AuthContext';
import * as api from '../../api/client';

export default function BalanceDisplay() {
  const { user } = useAuth();
  const [balance, setBalance] = useState(null);

  const fetchBalance = useCallback(async () => {
    if (!user) return;
    const { ok, data } = await api.get('/user/profile');
    if (ok) setBalance(data.balance);
  }, [user]);

  // Colleague receive handler — refresh balance on relevant events
  useColleague('BalanceDisplay', (event) => {
    if ([EVENTS.PAYMENT_PROCESSED, EVENTS.USER_LOGGED_IN, EVENTS.BOOKING_CREATED, EVENTS.USER_LOGGED_OUT].includes(event)) {
      if (event === EVENTS.USER_LOGGED_OUT) {
        setBalance(null);
        return;
      }
      fetchBalance();
    }
  });

  useEffect(() => { fetchBalance(); }, [fetchBalance]);

  if (balance === null) return null;
  return (
    <div className="flex items-center gap-1 text-sm font-medium text-gray-700 bg-gray-100 px-3 py-1.5 rounded-lg">
      <Wallet size={16} className="text-green-600" />
      ${balance.toFixed(2)}
    </div>
  );
}
