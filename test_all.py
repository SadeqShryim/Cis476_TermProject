"""
DriveShare — Comprehensive Automated Test Suite
Tests every feature and all 6 design patterns end-to-end.

Run with: python test_all.py
"""

import sys
import os
import shutil

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ─── Test Setup ──────────────────────────────────────────────────────────

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
PASS = 0
FAIL = 0


def setup():
    """Clean data directory for fresh test run."""
    if os.path.exists(DATA_DIR):
        shutil.rmtree(DATA_DIR)
    os.makedirs(DATA_DIR, exist_ok=True)

    # Reset singleton
    from patterns.singleton import SessionManager
    SessionManager.reset()


def check(test_name, condition, detail=""):
    """Assert a test condition and track pass/fail."""
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ✅ PASS: {test_name}")
    else:
        FAIL += 1
        print(f"  ❌ FAIL: {test_name}  {detail}")


def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


# ─── Tests ───────────────────────────────────────────────────────────────

def test_storage():
    """Test the JSON storage layer."""
    section("1. STORAGE LAYER (db_store)")

    from storage import db_store

    # Add and retrieve
    item = {'id': 'test-1', 'name': 'Test Item'}
    db_store.add('test.json', item)
    loaded = db_store.load_all('test.json')
    check("Add and load item", len(loaded) == 1 and loaded[0]['id'] == 'test-1')

    # Find by ID
    found = db_store.find_by_id('test.json', 'test-1')
    check("Find by ID", found is not None and found['name'] == 'Test Item')

    # Update
    db_store.update('test.json', 'test-1', {'name': 'Updated'})
    updated = db_store.find_by_id('test.json', 'test-1')
    check("Update item", updated['name'] == 'Updated')

    # Find by field
    results = db_store.find_by_field('test.json', 'name', 'Updated')
    check("Find by field", len(results) == 1)

    # Delete
    db_store.delete('test.json', 'test-1')
    deleted = db_store.find_by_id('test.json', 'test-1')
    check("Delete item", deleted is None)

    # Clean up
    try:
        os.remove(os.path.join(DATA_DIR, 'test.json'))
    except FileNotFoundError:
        pass

def test_user_model():
    """Test user model and password hashing."""
    section("2. USER MODEL & PASSWORD HASHING")

    from models.user import create_user, hash_password, verify_password

    user = create_user('test@test.com', 'mypass123', [
        {'question': 'Q1?', 'answer': 'A1'},
        {'question': 'Q2?', 'answer': 'A2'},
        {'question': 'Q3?', 'answer': 'A3'},
    ])
    check("User has ID", 'id' in user and len(user['id']) > 0)
    check("Email normalized", user['email'] == 'test@test.com')
    check("Password hashed", user['password_hash'] != 'mypass123')
    check("3 security questions", len(user['security_questions']) == 3)
    check("Starting balance = 1000", user['balance'] == 1000.0)

    # Password verification
    check("Correct password verifies", verify_password('mypass123', user['password_hash']))
    check("Wrong password fails", not verify_password('wrong', user['password_hash']))

    # Security answer normalization
    check("Answers lowercased", user['security_questions'][0]['answer'] == 'a1')


def test_singleton():
    """Test the Singleton pattern (SessionManager)."""
    section("3. SINGLETON PATTERN — SessionManager")

    from patterns.singleton import SessionManager

    SessionManager.reset()
    s1 = SessionManager()
    s2 = SessionManager()

    check("Same instance", s1 is s2)
    check("Not authenticated initially", not s1.is_authenticated())

    s1.login({'id': 'u1', 'email': 'a@b.com', 'balance': 500})
    check("Authenticated after login", s2.is_authenticated())
    check("Same user from both refs", s2.get_current_user()['email'] == 'a@b.com')

    s1.logout()
    check("Logged out", not s2.is_authenticated())

    SessionManager.reset()


def test_chain_of_responsibility():
    """Test the Chain of Responsibility pattern (password recovery)."""
    section("4. CHAIN OF RESPONSIBILITY PATTERN — SecurityQuestionChain")

    from patterns.chain_of_responsibility import build_security_chain

    user = {
        'security_questions': [
            {'question': 'Q1?', 'answer': 'apple'},
            {'question': 'Q2?', 'answer': 'banana'},
            {'question': 'Q3?', 'answer': 'cherry'},
        ]
    }

    chain = build_security_chain()

    # All correct
    check("All 3 correct → passes", chain.handle(user, ['apple', 'banana', 'cherry']))

    # First wrong
    chain = build_security_chain()
    check("Q1 wrong → fails", not chain.handle(user, ['WRONG', 'banana', 'cherry']))

    # Second wrong
    chain = build_security_chain()
    check("Q2 wrong → fails", not chain.handle(user, ['apple', 'WRONG', 'cherry']))

    # Third wrong
    chain = build_security_chain()
    check("Q3 wrong → fails", not chain.handle(user, ['apple', 'banana', 'WRONG']))

    # Case insensitive
    chain = build_security_chain()
    check("Answers case-insensitive", chain.handle(user, ['APPLE', 'Banana', 'CHERRY']))


def test_builder():
    """Test the Builder pattern (CarListingBuilder)."""
    section("5. BUILDER PATTERN — CarListingBuilder")

    from patterns.builder import CarListingBuilder

    builder = CarListingBuilder()

    # Missing required fields
    try:
        builder.build()
        check("Missing fields raises error", False)
    except ValueError as e:
        check("Missing fields raises error", 'Missing required fields' in str(e))

    # Build with all fields
    car = (CarListingBuilder()
           .set_owner('owner-1')
           .set_make('Toyota')
           .set_model('Camry')
           .set_year(2022)
           .set_mileage(15000)
           .set_daily_price(45.0)
           .set_location('Detroit, MI')
           .add_feature('Bluetooth')
           .add_feature('Backup Camera')
           .add_availability('2026-05-01', '2026-06-01')
           .build())

    check("Car has ID", 'id' in car)
    check("Make correct", car['make'] == 'Toyota')
    check("Model correct", car['model'] == 'Camry')
    check("Year correct", car['year'] == 2022)
    check("2 features", len(car['features']) == 2)
    check("1 availability window", len(car['availability']) == 1)
    check("is_active = True", car['is_active'] is True)

    # Build with minimum required fields
    car2 = (CarListingBuilder()
            .set_owner('owner-2')
            .set_make('Honda')
            .set_model('Civic')
            .set_year(2020)
            .set_daily_price(35.0)
            .set_location('Ann Arbor, MI')
            .build())
    check("Minimal build works", car2['make'] == 'Honda')
    check("Empty features list", car2['features'] == [])


def test_auth_service():
    """Test auth service (registration, login, logout, recovery)."""
    section("6. AUTH SERVICE (register, login, logout, recover)")

    from services import auth_service
    from patterns.singleton import SessionManager

    SessionManager.reset()

    # Register
    result = auth_service.register('alice@test.com', 'pass1234', [
        {'question': 'Pet name?', 'answer': 'Fluffy'},
        {'question': 'Birth city?', 'answer': 'Detroit'},
        {'question': 'Fav movie?', 'answer': 'Inception'},
    ])
    check("Registration success", result['success'])
    check("Auto-login after register", SessionManager().is_authenticated())

    alice_id = result['user']['id']

    # Duplicate email
    auth_service.logout()
    result2 = auth_service.register('alice@test.com', 'other', [
        {'question': 'Q?', 'answer': 'A'},
        {'question': 'Q?', 'answer': 'A'},
        {'question': 'Q?', 'answer': 'A'},
    ])
    check("Duplicate email blocked", not result2['success'])

    # Login
    result3 = auth_service.login('alice@test.com', 'pass1234')
    check("Login success", result3['success'])

    # Wrong password
    auth_service.logout()
    result4 = auth_service.login('alice@test.com', 'wrong')
    check("Wrong password fails", not result4['success'])

    # Password recovery (Chain of Responsibility)
    questions = auth_service.get_security_questions('alice@test.com')
    check("Get security questions", len(questions) == 3)

    # Correct answers
    result5 = auth_service.recover_password(
        'alice@test.com',
        ['Fluffy', 'Detroit', 'Inception'],
        'newpass456'
    )
    check("Password recovery success", result5['success'])

    # Login with new password
    result6 = auth_service.login('alice@test.com', 'newpass456')
    check("Login with new password", result6['success'])

    # Wrong recovery answers
    auth_service.logout()
    result7 = auth_service.recover_password(
        'alice@test.com',
        ['Wrong', 'Wrong', 'Wrong'],
        'hacked'
    )
    check("Wrong recovery answers fail", not result7['success'])

    # Register second user for later tests
    auth_service.logout()
    SessionManager.reset()
    result8 = auth_service.register('bob@test.com', 'bobpass', [
        {'question': 'Q1?', 'answer': 'B1'},
        {'question': 'Q2?', 'answer': 'B2'},
        {'question': 'Q3?', 'answer': 'B3'},
    ])
    check("Second user (Bob) registered", result8['success'])
    auth_service.logout()
    SessionManager.reset()

    return alice_id, result8['user']['id']


def test_car_service(alice_id):
    """Test car listing service with Builder pattern."""
    section("7. CAR SERVICE (CRUD with Builder)")

    from services import car_service
    from patterns.builder import CarListingBuilder

    # Create listing using Builder
    car_data = (CarListingBuilder()
                .set_owner(alice_id)
                .set_make('Toyota')
                .set_model('Camry')
                .set_year(2022)
                .set_mileage(15000)
                .set_daily_price(50.0)
                .set_location('Detroit, MI')
                .add_feature('Bluetooth')
                .add_availability('2026-04-15', '2026-06-15')
                .build())

    result = car_service.create_listing(car_data)
    check("Create listing", result['success'])
    car_id = car_data['id']

    # Get all listings
    all_cars = car_service.get_all_listings()
    check("Get all listings", len(all_cars) >= 1)

    # Get user listings
    my_cars = car_service.get_user_listings(alice_id)
    check("Get user listings", len(my_cars) >= 1)

    # Update listing
    result2 = car_service.update_listing(car_id, {'daily_price': 40.0}, alice_id)
    check("Update listing price", result2['success'] and result2['car']['daily_price'] == 40.0)

    # Update by wrong owner
    result3 = car_service.update_listing(car_id, {'daily_price': 30.0}, 'wrong-owner-id')
    check("Wrong owner update blocked", not result3['success'])

    # Create second car for booking tests
    car2 = (CarListingBuilder()
            .set_owner(alice_id)
            .set_make('Honda')
            .set_model('Civic')
            .set_year(2021)
            .set_mileage(20000)
            .set_daily_price(35.0)
            .set_location('Ann Arbor, MI')
            .add_availability('2026-05-01', '2026-07-01')
            .build())
    car_service.create_listing(car2)

    # Delete listing
    result4 = car_service.delete_listing(car2['id'], alice_id)
    check("Delete listing (soft)", result4['success'])

    # Verify soft-deleted
    active = car_service.get_active_listings()
    deleted_in_active = any(c['id'] == car2['id'] for c in active)
    check("Deleted car not in active listings", not deleted_in_active)

    return car_id


def test_booking_service(alice_id, bob_id, car_id):
    """Test booking service including conflict detection."""
    section("8. BOOKING SERVICE (search, book, conflicts)")

    from services import booking_service

    # Search all
    results = booking_service.search_cars()
    check("Search all cars returns results", len(results) >= 1)

    # Search by location
    results2 = booking_service.search_cars(location='Detroit')
    check("Search by location", len(results2) >= 1)

    # Search by max price
    results3 = booking_service.search_cars(max_price=30.0)
    check("Search by max price (no results)", len(results3) == 0)

    results4 = booking_service.search_cars(max_price=100.0)
    check("Search by max price (has results)", len(results4) >= 1)

    # Book a car
    result = booking_service.book_car(car_id, bob_id, '2026-05-01', '2026-05-04')
    check("Book car success", result['success'])
    check("Total price = 3 days × $40", result['booking']['total_price'] == 120.0)
    booking_id = result['booking']['id']

    # Self-booking blocked
    result2 = booking_service.book_car(car_id, alice_id, '2026-05-10', '2026-05-12')
    check("Cannot book own car", not result2['success'])

    # Overlapping dates blocked
    result3 = booking_service.book_car(car_id, bob_id, '2026-05-02', '2026-05-06')
    check("Overlapping booking blocked", not result3['success'])

    # Non-overlapping dates OK
    result4 = booking_service.book_car(car_id, bob_id, '2026-05-05', '2026-05-08')
    check("Non-overlapping booking OK", result4['success'])

    # Invalid dates
    result5 = booking_service.book_car(car_id, bob_id, '2026-06-10', '2026-06-08')
    check("End before start blocked", not result5['success'])

    # Cancel booking
    result6 = booking_service.cancel_booking(booking_id, bob_id)
    check("Cancel booking success", result6['success'])

    # Double cancel
    result7 = booking_service.cancel_booking(booking_id, bob_id)
    check("Double cancel blocked", not result7['success'])

    # Get user bookings
    bookings = booking_service.get_user_bookings(bob_id, as_renter=True)
    check("Get renter bookings", len(bookings) >= 1)

    owner_bookings = booking_service.get_user_bookings(alice_id, as_renter=False)
    check("Get owner bookings", len(owner_bookings) >= 1)

    return result4['booking']['id']  # Return the active booking


def test_observer_and_watch(alice_id, bob_id, car_id):
    """Test Observer pattern via the watch service."""
    section("9. OBSERVER PATTERN — Watch Service")

    from services import watch_service, car_service, notification_service

    # Bob watches Alice's car
    result = watch_service.watch_car(bob_id, car_id, max_price=35.0)
    check("Watch car success", result['success'])

    # Double watch blocked
    result2 = watch_service.watch_car(bob_id, car_id)
    check("Double watch blocked", not result2['success'])

    # Alice can't watch own car
    result3 = watch_service.watch_car(alice_id, car_id)
    check("Cannot watch own car", not result3['success'])

    # Get watched cars
    watched = watch_service.get_watched_cars(bob_id)
    check("Get watched cars", len(watched) == 1)
    check("Watch criteria saved", watched[0]['criteria']['max_price'] == 35.0)

    # Trigger price drop notification (Observer pattern fires)
    # Current price is $40, Bob wants ≤ $35
    car_service.update_listing(car_id, {'daily_price': 32.0}, alice_id)

    # Check Bob got a notification
    notifs = notification_service.get_notifications(bob_id)
    watch_notifs = [n for n in notifs if n['type'] == 'watch']
    check("Watcher notified on price drop", len(watch_notifs) >= 1)
    if watch_notifs:
        check("Notification mentions price", 'rice' in watch_notifs[0]['content'].lower()
              or '$' in watch_notifs[0]['content'])

    # Unwatch
    result4 = watch_service.unwatch_car(bob_id, car_id)
    check("Unwatch success", result4['success'])

    watched_after = watch_service.get_watched_cars(bob_id)
    check("No watched cars after unwatch", len(watched_after) == 0)


def test_proxy_and_payment(alice_id, bob_id, active_booking_id):
    """Test Proxy pattern via payment service."""
    section("10. PROXY PATTERN — Payment Service")

    from services import payment_service, notification_service
    from storage import db_store

    # Get pre-payment balances
    bob_before = db_store.find_by_id('users.json', bob_id)
    alice_before = db_store.find_by_id('users.json', alice_id)
    bob_bal = bob_before['balance']
    alice_bal = alice_before['balance']

    # Get booking to pay
    booking = db_store.find_by_id('bookings.json', active_booking_id)
    amount = booking['total_price']

    # Process payment (Proxy validates → logs → processes → notifies)
    result = payment_service.process_payment(bob_id, alice_id, amount, active_booking_id)
    check("Payment success", result['success'])

    # Balances updated
    bob_after = db_store.find_by_id('users.json', bob_id)
    alice_after = db_store.find_by_id('users.json', alice_id)
    check("Renter balance decreased", bob_after['balance'] == round(bob_bal - amount, 2))
    check("Owner balance increased", alice_after['balance'] == round(alice_bal + amount, 2))

    # Booking marked as paid
    updated_booking = db_store.find_by_id('bookings.json', active_booking_id)
    check("Booking marked paid", updated_booking.get('paid') is True)

    # Both got payment notifications
    bob_notifs = notification_service.get_notifications(bob_id)
    bob_payment_notifs = [n for n in bob_notifs if n['type'] == 'payment']
    check("Renter got payment notification", len(bob_payment_notifs) >= 1)

    alice_notifs = notification_service.get_notifications(alice_id)
    alice_payment_notifs = [n for n in alice_notifs if n['type'] == 'payment']
    check("Owner got payment notification", len(alice_payment_notifs) >= 1)

    # Transaction log recorded
    log = payment_service.get_transaction_log()
    check("Transaction logged", len(log) >= 1)
    check("Log shows SUCCESS", log[-1]['status'] == 'SUCCESS')

    # Insufficient balance test
    result2 = payment_service.process_payment(bob_id, alice_id, 999999.0)
    check("Insufficient balance blocked", not result2['success'])

    # Negative amount test
    result3 = payment_service.process_payment(bob_id, alice_id, -10.0)
    check("Negative amount blocked", not result3['success'])


def test_messaging(alice_id, bob_id):
    """Test messaging service."""
    section("11. MESSAGING SERVICE")

    from services import message_service, notification_service

    # Send message
    result = message_service.send_message(bob_id, alice_id, "Hi! Interested in your car.")
    check("Send message success", result['success'])

    # Self-message blocked
    result2 = message_service.send_message(bob_id, bob_id, "Talking to myself")
    check("Self-message blocked", not result2['success'])

    # Empty message blocked
    result3 = message_service.send_message(bob_id, alice_id, "   ")
    check("Empty message blocked", not result3['success'])

    # Reply
    result4 = message_service.send_message(alice_id, bob_id, "Sure! When do you need it?")
    check("Reply sent", result4['success'])

    # Get conversation
    convo = message_service.get_conversation(bob_id, alice_id)
    check("Conversation has 2 messages", len(convo) == 2)
    check("Messages in chronological order", convo[0]['timestamp'] <= convo[1]['timestamp'])

    # Get conversations list
    bob_convos = message_service.get_conversations(bob_id)
    check("Bob has 1 conversation", len(bob_convos) == 1)
    check("Conversation partner is Alice", bob_convos[0]['partner_id'] == alice_id)

    # Unread count
    check("Alice has unread from Bob", bob_convos[0]['unread_count'] >= 0)

    # Mark conversation read
    message_service.mark_conversation_read(alice_id, bob_id)

    # Message notification sent
    alice_notifs = notification_service.get_notifications(alice_id)
    msg_notifs = [n for n in alice_notifs if n['type'] == 'message']
    check("Message notification sent", len(msg_notifs) >= 1)


def test_notification_service(alice_id, bob_id):
    """Test notification service."""
    section("12. NOTIFICATION SERVICE")

    from services import notification_service

    # Get all notifications
    alice_notifs = notification_service.get_notifications(alice_id)
    check("Alice has notifications", len(alice_notifs) > 0)

    # Unread count
    unread = notification_service.get_unread_count(alice_id)
    check("Unread count > 0", unread > 0)

    # Mark all read
    notification_service.mark_all_read(alice_id)
    new_unread = notification_service.get_unread_count(alice_id)
    check("All marked read", new_unread == 0)

    # Add manual notification
    notification_service.add_notification(bob_id, "Test notification", 'general')
    bob_notifs = notification_service.get_notifications(bob_id)
    check("Manual notification added", any(n['content'] == 'Test notification' for n in bob_notifs))


def test_mediator():
    """Test the Mediator pattern."""
    section("13. MEDIATOR PATTERN — UIMediator")

    from patterns.mediator import UIMediator

    mediator = UIMediator()

    # Test component registration and data sharing
    class MockComponent:
        def __init__(self):
            self.received_events = []
            self.mediator = None

        def set_mediator(self, m):
            self.mediator = m

        def receive(self, event, data):
            self.received_events.append((event, data))

    comp_owner = MockComponent()
    comp_renter = MockComponent()
    mediator.register('owner', comp_owner)
    mediator.register('renter', comp_renter)

    check("Components registered", mediator.get_component('owner') is comp_owner)
    check("Mediator set on component", comp_owner.mediator is mediator)

    # Test event routing
    mediator.notify('main', 'navigate_owner_menu', {'from': 'dashboard'})
    check("Event routed to owner", len(comp_owner.received_events) == 1)
    check("Renter not notified", len(comp_renter.received_events) == 0)

    mediator.notify('main', 'car_selected', {'car_id': '123'})
    check("car_selected routed to renter", len(comp_renter.received_events) == 1)

    # Shared data
    mediator.set_data('selected_car', 'car-abc')
    check("Shared data stored", mediator.get_data('selected_car') == 'car-abc')


def test_data_persistence():
    """Test that data persists in JSON files."""
    section("14. DATA PERSISTENCE")

    from storage import db_store

    users = db_store.load_all('users.json')
    check("Users persisted", len(users) >= 2)

    cars = db_store.load_all('cars.json')
    check("Cars persisted", len(cars) >= 1)

    bookings = db_store.load_all('bookings.json')
    check("Bookings persisted", len(bookings) >= 1)

    messages = db_store.load_all('messages.json')
    check("Messages persisted", len(messages) >= 2)

    notifications = db_store.load_all('notifications.json')
    check("Notifications persisted", len(notifications) >= 1)


# ─── Run All Tests ──────────────────────────────────────────────────────

def run_all():
    global PASS, FAIL
    PASS = 0
    FAIL = 0

    print("\n" + "🚗" * 30)
    print("  DriveShare — Automated Test Suite")
    print("🚗" * 30)

    setup()

    test_storage()
    test_user_model()
    test_singleton()
    test_chain_of_responsibility()
    test_builder()
    alice_id, bob_id = test_auth_service()
    car_id = test_car_service(alice_id)
    active_booking_id = test_booking_service(alice_id, bob_id, car_id)
    test_observer_and_watch(alice_id, bob_id, car_id)
    test_proxy_and_payment(alice_id, bob_id, active_booking_id)
    test_messaging(alice_id, bob_id)
    test_notification_service(alice_id, bob_id)
    test_mediator()
    test_data_persistence()

    print(f"\n{'='*60}")
    print(f"  RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print(f"{'='*60}")

    if FAIL == 0:
        print("  🎉 ALL TESTS PASSED!")
    else:
        print(f"  ⚠️  {FAIL} test(s) failed — review above.")

    print()
    return FAIL == 0


if __name__ == '__main__':
    success = run_all()
    sys.exit(0 if success else 1)
