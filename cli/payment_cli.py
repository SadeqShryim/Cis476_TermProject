"""
CLI Payment & Booking Management Screens.

Uses:
  - Proxy pattern (PaymentProxy) for simulated payment processing
"""

from cli.menus import print_header, pause
from patterns.singleton import SessionManager
from services import booking_service, car_service, payment_service


def bookings_and_payments_menu():
    """Bookings & payments sub-menu."""
    while True:
        print_header("Bookings & Payments")
        print()
        print("  1. 📅 My Bookings (as Renter)")
        print("  2. 📋 Bookings for My Cars (as Owner)")
        print("  3. 💳 Pay for a Booking")
        print("  4. 💰 Transaction History")
        print("  0. ⬅  Back to Dashboard")
        print()

        choice = input("  Select an option: ").strip()

        if choice == '1':
            renter_bookings_screen()
        elif choice == '2':
            owner_bookings_screen()
        elif choice == '3':
            pay_for_booking_screen()
        elif choice == '4':
            transaction_history_screen()
        elif choice == '0':
            break
        else:
            print("\n  ❌ Invalid option.")
            pause()


def renter_bookings_screen():
    """View the current user's bookings as a renter."""
    session = SessionManager()
    user = session.get_current_user()

    print_header("My Bookings (Renter)")
    bookings = booking_service.get_user_bookings(user['id'], as_renter=True)

    if not bookings:
        print("\n  No bookings found.")
        pause()
        return

    _display_bookings(bookings)
    pause()


def owner_bookings_screen():
    """View bookings for the current user's cars (as owner)."""
    session = SessionManager()
    user = session.get_current_user()

    print_header("Bookings for My Cars (Owner)")
    bookings = booking_service.get_user_bookings(user['id'], as_renter=False)

    if not bookings:
        print("\n  No one has booked your cars yet.")
        pause()
        return

    _display_bookings(bookings, show_renter=True)
    pause()


def _display_bookings(bookings, show_renter=False):
    """Helper to display a list of bookings."""
    from services.auth_service import get_user_by_id

    for i, b in enumerate(bookings, 1):
        car = car_service.get_car_by_id(b['car_id'])
        car_name = f"{car['make']} {car['model']}" if car else "Unknown car"
        status_emoji = {
            'confirmed': '🟢',
            'cancelled': '🔴',
            'completed': '✅'
        }.get(b['status'], '⚪')
        paid_tag = " 💳 PAID" if b.get('paid') else " ⏳ UNPAID"

        print(f"\n  [{i}] {car_name}")
        print(f"      📅 {b['start_date']} → {b['end_date']}")
        print(f"      💲 ${b['total_price']:.2f}  |  {status_emoji} {b['status'].upper()}{paid_tag}")

        if show_renter:
            renter = get_user_by_id(b['renter_id'])
            renter_email = renter['email'] if renter else 'Unknown'
            print(f"      👤 Renter: {renter_email}")

        print(f"      🆔 {b['id'][:8]}...")


def pay_for_booking_screen():
    """
    Pay for an unpaid booking using the Proxy pattern.
    The PaymentProxy validates balance, processes payment, logs it, and notifies both parties.
    """
    session = SessionManager()
    session.refresh()
    user = session.get_current_user()

    print_header("Pay for a Booking")
    bookings = booking_service.get_user_bookings(user['id'], as_renter=True)

    # Filter to unpaid, confirmed bookings only
    unpaid = [b for b in bookings if not b.get('paid') and b['status'] == 'confirmed']

    if not unpaid:
        print("\n  No unpaid bookings to pay for.")
        pause()
        return

    print(f"\n  Your balance: ${user['balance']:.2f}\n")

    for i, b in enumerate(unpaid, 1):
        car = car_service.get_car_by_id(b['car_id'])
        car_name = f"{car['make']} {car['model']}" if car else "Unknown car"
        print(f"  [{i}] {car_name} — ${b['total_price']:.2f}")
        print(f"      📅 {b['start_date']} → {b['end_date']}")

    print()

    try:
        idx = int(input("  Select booking to pay (number): ").strip()) - 1
        if idx < 0 or idx >= len(unpaid):
            raise ValueError
    except ValueError:
        print("\n  ❌ Invalid selection.")
        pause()
        return

    booking = unpaid[idx]
    car = car_service.get_car_by_id(booking['car_id'])
    car_name = f"{car['make']} {car['model']}" if car else "Unknown car"

    print(f"\n  📋 Paying ${booking['total_price']:.2f} for {car_name}")
    print(f"  Current balance: ${user['balance']:.2f}")

    confirm = input("\n  Confirm payment? (y/n): ").strip().lower()
    if confirm != 'y':
        print("\n  Payment cancelled.")
        pause()
        return

    # Use PaymentProxy (Proxy pattern)
    result = payment_service.process_payment(
        renter_id=user['id'],
        owner_id=booking['owner_id'],
        amount=booking['total_price'],
        booking_id=booking['id']
    )

    print(f"\n  {'✅' if result['success'] else '❌'} {result['message']}")

    if result['success']:
        session.refresh()
        print(f"  New balance: ${session.get_current_user()['balance']:.2f}")

    pause()


def transaction_history_screen():
    """View the in-memory transaction log from the PaymentProxy."""
    print_header("Transaction History")
    log = payment_service.get_transaction_log()

    if not log:
        print("\n  No transactions yet.")
        pause()
        return

    from services.auth_service import get_user_by_id

    for i, t in enumerate(log, 1):
        renter = get_user_by_id(t['renter_id'])
        owner = get_user_by_id(t['owner_id'])
        renter_email = renter['email'] if renter else 'Unknown'
        owner_email = owner['email'] if owner else 'Unknown'

        status_emoji = '✅' if t['status'] == 'SUCCESS' else '❌'
        print(f"\n  {status_emoji} Transaction #{i}")
        print(f"      From: {renter_email} → To: {owner_email}")
        print(f"      Amount: ${t['amount']:.2f}  |  Status: {t['status']}")
        if t.get('reason'):
            print(f"      Reason: {t['reason']}")
        print(f"      Time: {t['timestamp'][:16].replace('T', ' ')}")

    print()
    pause()
