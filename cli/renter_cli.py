"""
CLI Renter Screens — Search cars, book, watch, view bookings.

Uses:
  - Observer pattern (watching cars)
  - Booking conflict detection
"""

from cli.menus import print_header, pause
from patterns.singleton import SessionManager
from services import car_service, booking_service, watch_service


def renter_menu():
    """Renter sub-menu for searching, booking, and watching cars."""
    while True:
        print_header("Renter — Find & Book Cars")
        print()
        print("  1. 🔍 Search Cars")
        print("  2. 📋 Browse All Available Cars")
        print("  3. 📅 My Bookings")
        print("  4. 👀 My Watched Cars")
        print("  0. ⬅  Back to Dashboard")
        print()

        choice = input("  Select an option: ").strip()

        if choice == '1':
            search_cars_screen()
        elif choice == '2':
            browse_all_cars()
        elif choice == '3':
            my_bookings_screen()
        elif choice == '4':
            watched_cars_screen()
        elif choice == '0':
            break
        else:
            print("\n  ❌ Invalid option.")
            pause()


def _display_cars(cars, show_index=True):
    """Helper to display a list of cars."""
    session = SessionManager()
    current_user_id = session.get_current_user()['id']

    for i, car in enumerate(cars, 1):
        prefix = f"  [{i}]" if show_index else "  •"
        own = " (YOUR CAR)" if car['owner_id'] == current_user_id else ""
        print(f"{prefix} {car['make']} {car['model']} ({car['year']}){own}")
        print(f"      💲 ${car['daily_price']:.2f}/day  |  📍 {car['location']}")
        print(f"      🛣️  {car['mileage']:,} miles")
        if car.get('features'):
            print(f"      ⭐ {', '.join(car['features'])}")
        if car.get('availability'):
            windows = [f"{a['start']} → {a['end']}" for a in car['availability']]
            print(f"      📅 {' | '.join(windows)}")
        print()


def search_cars_screen():
    """Search for cars with filters."""
    print_header("Search Cars")
    print("\n  Enter filters (leave blank to skip):\n")

    location = input("  Location: ").strip() or None
    make = input("  Make (e.g., Toyota): ").strip() or None

    max_price_str = input("  Max daily price ($): ").strip()
    max_price = None
    if max_price_str:
        try:
            max_price = float(max_price_str)
        except ValueError:
            pass

    start_date = input("  Start date (YYYY-MM-DD): ").strip() or None
    end_date = None
    if start_date:
        end_date = input("  End date (YYYY-MM-DD): ").strip() or None

    results = booking_service.search_cars(
        location=location,
        start_date=start_date,
        end_date=end_date,
        max_price=max_price,
        make=make
    )

    print_header("Search Results")
    if not results:
        print("\n  No cars found matching your criteria.")
        pause()
        return

    print(f"\n  Found {len(results)} car(s):\n")
    _display_cars(results)

    _car_action_menu(results)


def browse_all_cars():
    """Browse all active car listings."""
    print_header("All Available Cars")
    cars = car_service.get_active_listings()

    if not cars:
        print("\n  No cars listed yet.")
        pause()
        return

    print(f"\n  {len(cars)} car(s) available:\n")
    _display_cars(cars)

    _car_action_menu(cars)


def _car_action_menu(cars):
    """After viewing a car list, let the user book or watch."""
    session = SessionManager()
    user = session.get_current_user()

    print("-" * 60)
    print("  Actions:")
    print("  B <#>  — Book a car (e.g., B 1)")
    print("  W <#>  — Watch a car (e.g., W 2)")
    print("  0      — Go back")
    print()

    while True:
        action = input("  Action: ").strip().upper()

        if action == '0':
            break

        parts = action.split()
        if len(parts) != 2:
            print("  ❌ Format: B <number> or W <number>")
            continue

        cmd, num_str = parts
        try:
            idx = int(num_str) - 1
            if idx < 0 or idx >= len(cars):
                raise ValueError
        except ValueError:
            print("  ❌ Invalid car number.")
            continue

        car = cars[idx]

        if cmd == 'B':
            _book_car(car, user)
            break
        elif cmd == 'W':
            _watch_car(car, user)
        else:
            print("  ❌ Unknown command. Use B or W.")


def _book_car(car, user):
    """Book a specific car."""
    print(f"\n  Booking: {car['make']} {car['model']} ({car['year']})")
    print(f"  Price: ${car['daily_price']:.2f}/day\n")

    start = input("  Start date (YYYY-MM-DD): ").strip()
    end = input("  End date (YYYY-MM-DD): ").strip()

    if not start or not end:
        print("\n  ❌ Both dates are required.")
        pause()
        return

    result = booking_service.book_car(car['id'], user['id'], start, end)
    print(f"\n  {'✅' if result['success'] else '❌'} {result['message']}")
    pause()


def _watch_car(car, user):
    """Watch a car with optional criteria."""
    print(f"\n  Watch: {car['make']} {car['model']} ({car['year']})")
    print("  Set watch criteria (leave blank to skip):\n")

    max_price_str = input("  Notify me if price drops to ($): ").strip()
    max_price = float(max_price_str) if max_price_str else None

    desired_start = input("  Desired start date (YYYY-MM-DD): ").strip() or None
    desired_end = input("  Desired end date (YYYY-MM-DD): ").strip() or None

    result = watch_service.watch_car(
        user['id'], car['id'],
        max_price=max_price,
        desired_start=desired_start,
        desired_end=desired_end
    )
    print(f"\n  {'✅' if result['success'] else '❌'} {result['message']}")
    pause()


def my_bookings_screen():
    """View the renter's bookings."""
    session = SessionManager()
    user = session.get_current_user()

    print_header("My Bookings")
    bookings = booking_service.get_user_bookings(user['id'], as_renter=True)

    if not bookings:
        print("\n  You don't have any bookings yet.")
        pause()
        return

    for i, b in enumerate(bookings, 1):
        car = car_service.get_car_by_id(b['car_id'])
        car_name = f"{car['make']} {car['model']}" if car else "Unknown"
        status_emoji = {'confirmed': '🟢', 'cancelled': '🔴', 'completed': '✅'}.get(b['status'], '⚪')
        paid_tag = " 💳 PAID" if b.get('paid') else " ⏳ UNPAID"

        print(f"\n  [{i}] {car_name}")
        print(f"      📅 {b['start_date']} → {b['end_date']}")
        print(f"      💲 ${b['total_price']:.2f}  |  {status_emoji} {b['status'].upper()}{paid_tag}")
        print(f"      🆔 {b['id'][:8]}...")

    print()
    print("  C <#> — Cancel a booking (e.g., C 1)")
    print("  0     — Back")
    print()

    action = input("  Action: ").strip().upper()
    if action == '0':
        return

    parts = action.split()
    if len(parts) == 2 and parts[0] == 'C':
        try:
            idx = int(parts[1]) - 1
            if idx < 0 or idx >= len(bookings):
                raise ValueError
            result = booking_service.cancel_booking(bookings[idx]['id'], user['id'])
            print(f"\n  {'✅' if result['success'] else '❌'} {result['message']}")
        except ValueError:
            print("\n  ❌ Invalid booking number.")
    pause()


def watched_cars_screen():
    """View and manage watched cars."""
    session = SessionManager()
    user = session.get_current_user()

    print_header("My Watched Cars")
    watched = watch_service.get_watched_cars(user['id'])

    if not watched:
        print("\n  You're not watching any cars.")
        pause()
        return

    for i, entry in enumerate(watched, 1):
        car = entry['car']
        criteria = entry['criteria']
        print(f"\n  [{i}] {car['make']} {car['model']} ({car['year']})")
        print(f"      💲 ${car['daily_price']:.2f}/day  |  📍 {car['location']}")
        if criteria.get('max_price'):
            print(f"      🎯 Alert when ≤ ${criteria['max_price']:.2f}/day")
        if criteria.get('desired_start') and criteria.get('desired_end'):
            print(f"      📅 Desired: {criteria['desired_start']} → {criteria['desired_end']}")

    print()
    print("  U <#> — Unwatch (e.g., U 1)")
    print("  0     — Back")
    print()

    action = input("  Action: ").strip().upper()
    if action == '0':
        return

    parts = action.split()
    if len(parts) == 2 and parts[0] == 'U':
        try:
            idx = int(parts[1]) - 1
            if idx < 0 or idx >= len(watched):
                raise ValueError
            car_id = watched[idx]['car']['id']
            result = watch_service.unwatch_car(user['id'], car_id)
            print(f"\n  {'✅' if result['success'] else '❌'} {result['message']}")
        except ValueError:
            print("\n  ❌ Invalid number.")
    pause()
