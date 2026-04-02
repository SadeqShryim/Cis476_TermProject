"""Payment service — simulated payments using the Proxy pattern."""

from patterns.proxy import PaymentProxy

# Single proxy instance for the entire app
_payment_proxy = PaymentProxy()


def process_payment(renter_id, owner_id, amount, booking_id=None):
    """
    Process a payment through the PaymentProxy.
    The proxy validates, logs, delegates, and notifies.
    """
    return _payment_proxy.process_payment(renter_id, owner_id, amount, booking_id)


def get_transaction_log():
    """Return the in-memory transaction log."""
    return _payment_proxy.get_transaction_log()
