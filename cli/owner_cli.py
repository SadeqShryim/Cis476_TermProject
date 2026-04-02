"""
CLI Owner Screens — List cars, manage listings, update pricing/availability.

Uses:
  - Builder pattern (CarListingBuilder) for car creation
  - Observer pattern triggers when price/availability changes
"""

from cli.menus import print_header, pause
from patterns.singleton import SessionManager
from patterns.builder import CarListingBuilder
from services import car_service


def owner_menu():
    """Owner sub-menu for managing car listings."""
    while True:
        print_header("Owner — My Cars")
        print()
        print("  1. ➕ List a New Car")
        print("  2. 📋 View My Listings")
        print("  3. ✏️  Update a Listing")
        print("  4. 🗑️  Remove a Listing")
        print("  0. ⬅  Back to Dashboard")
        print()

        choice = input("  Select an option: ").strip()

        if choice == '1':
            list_car_screen()
        elif choice == '2':
            view_my_listings()
        elif choice == '3':
            update_listing_screen()
        elif choice == '4':
            delete_listing_screen()
        elif choice == '0':
            break
        else:
            print("\n  ❌ Invalid option.")
            pause()


def list_car_screen():
    """
    Create a new car listing using the Builder pattern.
    Walks the user through setting required and optional fields.
    """
    session = SessionManager()
    user = session.get_current_user()

    print_header("List a New Car")
    print("\n  Fill in the details below (Builder Pattern):\n")

    builder = CarListingBuilder()
    builder.set_owner(user['id'])

    # Required fields
    make = input("  Make (e.g., Toyota): ").strip()
    if not make:
        print("\n  ❌ Make is required.")
        pause()
        return
    builder.set_make(make)

    model = input("  Model (e.g., Camry): ").strip()
    if not model:
        print("\n  ❌ Model is required.")
        pause()
        return
    builder.set_model(model)

    try:
        year = input("  Year (e.g., 2022): ").strip()
        builder.set_year(year)
    except ValueError:
        print("\n  ❌ Invalid year.")
        pause()
        return

    try:
        mileage = input("  Mileage (e.g., 15000): ").strip()
        builder.set_mileage(mileage if mileage else '0')
    except ValueError:
        print("\n  ❌ Invalid mileage.")
        pause()
        return

    try:
        price = input("  Daily rental price ($): ").strip()
        builder.set_daily_price(price)
    except ValueError:
        print("\n  ❌ Invalid price.")
        pause()
        return

    location = input("  Pick-up location (e.g., Detroit, MI): ").strip()
    if not location:
        print("\n  ❌ Location is required.")
        pause()
        return
    builder.set_location(location)

    # Optional features
    print("\n  Add features (type each one and press Enter, empty to finish):")
    while True:
        feature = input("    Feature: ").strip()
        if not feature:
            break
        builder.add_feature(feature)

    # Optional availability windows
    print("\n  Add availability windows (YYYY-MM-DD format, empty to skip):")
    while True:
        start = input("    Start date (or empty to finish): ").strip()
        if not start:
            break
        end = input("    End date: ").strip()
        if not end:
            break
        builder.add_availability(start, end)

    # Build and save
    try:
        car = builder.build()
        result = car_service.create_listing(car)
        print(f"\n  ✅ {result['message']}")
        print(f"     {make} {model} ({year}) — ${float(price):.2f}/day")
    except ValueError as e:
        print(f"\n  ❌ {e}")

    pause()


def view_my_listings():
    """View all of the current user's car listings."""
    session = SessionManager()
    user = session.get_current_user()

    print_header("My Car Listings")
    listings = car_service.get_user_listings(user['id'])

    if not listings:
        print("\n  You don't have any car listings yet.")
        pause()
        return

    for i, car in enumerate(listings, 1):
        status = "🟢 Active" if car.get('is_active', True) else "🔴 Inactive"
        print(f"\n  [{i}] {car['make']} {car['model']} ({car['year']}) — {status}")
        print(f"      💲 ${car['daily_price']:.2f}/day  |  📍 {car['location']}")
        print(f"      🛣️  {car['mileage']:,} miles")
        if car.get('features'):
            print(f"      ⭐ Features: {', '.join(car['features'])}")
        if car.get('availability'):
            windows = [f"{a['start']} to {a['end']}" for a in car['availability']]
            print(f"      📅 Available: {' | '.join(windows)}")
        watcher_count = len(car.get('watchers', []))
        if watcher_count:
            print(f"      👀 {watcher_count} watcher(s)")
        print(f"      🆔 {car['id'][:8]}...")

    print()
    pause()


def update_listing_screen():
    """Update price or availability of an existing listing."""
    session = SessionManager()
    user = session.get_current_user()

    print_header("Update Listing")
    listings = car_service.get_user_listings(user['id'])
    active = [c for c in listings if c.get('is_active', True)]

    if not active:
        print("\n  No active listings to update.")
        pause()
        return

    for i, car in enumerate(active, 1):
        print(f"  [{i}] {car['make']} {car['model']} ({car['year']}) — ${car['daily_price']:.2f}/day")

    print()
    try:
        idx = int(input("  Select a car to update (number): ").strip()) - 1
        if idx < 0 or idx >= len(active):
            raise ValueError
    except ValueError:
        print("\n  ❌ Invalid selection.")
        pause()
        return

    car = active[idx]
    print(f"\n  Updating: {car['make']} {car['model']}")
    print()
    print("  1. Update daily price")
    print("  2. Update availability")
    print("  3. Update both")
    print()

    choice = input("  Select: ").strip()
    updates = {}

    if choice in ('1', '3'):
        try:
            new_price = float(input(f"  New daily price (current: ${car['daily_price']:.2f}): $").strip())
            updates['daily_price'] = new_price
        except ValueError:
            print("\n  ❌ Invalid price.")
            pause()
            return

    if choice in ('2', '3'):
        print("  Enter new availability windows (empty start to finish):")
        new_avail = []
        while True:
            start = input("    Start date (YYYY-MM-DD): ").strip()
            if not start:
                break
            end = input("    End date (YYYY-MM-DD): ").strip()
            if not end:
                break
            new_avail.append({'start': start, 'end': end})
        if new_avail:
            updates['availability'] = new_avail

    if not updates:
        print("\n  No changes made.")
        pause()
        return

    result = car_service.update_listing(car['id'], updates, user['id'])
    print(f"\n  {'✅' if result['success'] else '❌'} {result['message']}")

    if 'daily_price' in updates and updates['daily_price'] < car['daily_price']:
        print("  📢 Watchers have been notified of the price drop!")

    pause()


def delete_listing_screen():
    """Remove (deactivate) a car listing."""
    session = SessionManager()
    user = session.get_current_user()

    print_header("Remove Listing")
    listings = car_service.get_user_listings(user['id'])
    active = [c for c in listings if c.get('is_active', True)]

    if not active:
        print("\n  No active listings to remove.")
        pause()
        return

    for i, car in enumerate(active, 1):
        print(f"  [{i}] {car['make']} {car['model']} ({car['year']})")

    print()
    try:
        idx = int(input("  Select a car to remove (number): ").strip()) - 1
        if idx < 0 or idx >= len(active):
            raise ValueError
    except ValueError:
        print("\n  ❌ Invalid selection.")
        pause()
        return

    car = active[idx]
    confirm = input(f"  Remove {car['make']} {car['model']}? (y/n): ").strip().lower()
    if confirm == 'y':
        result = car_service.delete_listing(car['id'], user['id'])
        print(f"\n  {'✅' if result['success'] else '❌'} {result['message']}")
    else:
        print("\n  Cancelled.")

    pause()
