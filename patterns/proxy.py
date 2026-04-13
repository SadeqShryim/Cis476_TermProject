"""
Proxy Pattern — PaymentProxy

The proxy validates, logs, and delegates to the real payment service.
It also sends notifications to both renter and owner after a transaction.
"""

from models.notification import create_notification
from storage import db_store
from datetime import datetime


class RealPaymentService:
    """The actual payment processing service (simulated)."""

    def process(self, renter_id, owner_id, amount):
        """Deduct from renter, credit to owner."""
        renter = db_store.find_by_id('users.json', renter_id)
        owner = db_store.find_by_id('users.json', owner_id)

        if not renter or not owner:
            return {'success': False, 'message': 'User not found'}

        new_renter_balance = round(renter['balance'] - amount, 2)
        new_owner_balance = round(owner['balance'] + amount, 2)

        db_store.update('users.json', renter_id, {'balance': new_renter_balance})
        db_store.update('users.json', owner_id, {'balance': new_owner_balance})

        return {
            'success': True,
            'message': f'Payment of ${amount:.2f} processed successfully',
            'renter_balance': new_renter_balance,
            'owner_balance': new_owner_balance
        }


class PaymentProxy:
    """
    Proxy pattern — sits between the client and the real payment service.
    It is tasked with:
      1. Validating that the renter has sufficient balance
      2. Validate payment amount
      3. Log the transaction
      4. Delegate to the real service
      5. Send notifications to both parties
    """

    def __init__(self):
        self._real_service = RealPaymentService()
        self._transaction_log = []

    def process_payment(self, renter_id, owner_id, amount, booking_id=None):
        """Process a payment through the proxy."""

        # Step 1: Validate amount
        if amount <= 0:
            return {'success': False, 'message': 'Payment amount must be positive'}

        # Step 2: Validate renter balance
        renter = db_store.find_by_id('users.json', renter_id)
        if not renter:
            return {'success': False, 'message': 'Renter not found'}

        if renter['balance'] < amount:
            self._log_transaction(renter_id, owner_id, amount, 'FAILED',
                                  'Insufficient balance')
            return {
                'success': False,
                'message': (f'Insufficient balance. '
                            f'Current: ${renter["balance"]:.2f}, '
                            f'Required: ${amount:.2f}')
            }

        # Step 3: Delegate to real service
        result = self._real_service.process(renter_id, owner_id, amount)

        # Step 4: Log transaction
        status = 'SUCCESS' if result['success'] else 'FAILED'
        self._log_transaction(renter_id, owner_id, amount, status)

        #Adam.Said: (3/22 Fixed notifications failing to send)
        # Step 5: Send notifications
        if result['success']:
            renter_notif = create_notification(
                renter_id,
                f"💳 Payment of ${amount:.2f} sent. New balance: ${result['renter_balance']:.2f}",
                'payment'
            )
            owner_notif = create_notification(
                owner_id,
                f"💰 Payment of ${amount:.2f} received. New balance: ${result['owner_balance']:.2f}",
                'payment'
            )
            db_store.add('notifications.json', renter_notif)
            db_store.add('notifications.json', owner_notif)

            # Mark booking as paid if booking_id provided
            if booking_id:
                db_store.update('bookings.json', booking_id, {'paid': True})

        return result

    def _log_transaction(self, renter_id, owner_id, amount, status, reason=''):
        """Record transaction in the in-memory log."""
        self._transaction_log.append({
            'renter_id': renter_id,
            'owner_id': owner_id,
            'amount': amount,
            'status': status,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        })

    def get_transaction_log(self):
        """Return the full transaction log."""
        return self._transaction_log
