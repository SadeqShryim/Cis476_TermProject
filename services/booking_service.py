"""Booking service — search, book, conflict detection."""

from datetime import datetime
from storage import db_store
from models.booking import create_booking
from models.notification import create_notification


def search_cars(location=None, start_date=None, end_date=None,
                max_price=None, make=None):
    """
    Search for available cars with optional filters.
    Returns a list of matching car dicts.
    """
    cars = db_store.load_all('cars.json')
    results = []

    for car in cars:
        if not car.get('is_active', True):
            continue

        # Filter by location (substring match, case-insensitive)
        if location and location.lower() not in car.get('location', '').lower():
            continue

        # Filter by max daily price
        if max_price is not None and car['daily_price'] > max_price:
            continue

        # Filter by make (substring match)
        if make and make.lower() not in car.get('make', '').lower():
            continue

        # Filter by date availability
        if start_date and end_date:
            if not _is_available(car, start_date, end_date):
                continue

        results.append(car)

    return results


def _is_available(car, start_date, end_date):
    """Check if a car is available for the given date range."""
    # If the car has explicit availability windows, check them
    if car.get('availability'):
        has_window = False
        for window in car['availability']:
            if window['start'] <= start_date and window['end'] >= end_date:
                has_window = True
                break
        if not has_window:
            return False

    # Check for conflicting bookings
    return not _has_conflict(car['id'], start_date, end_date)


def _has_conflict(car_id, start_date, end_date):
    """Check for overlapping confirmed bookings on this car."""
    bookings = db_store.load_all('bookings.json')
    for booking in bookings:
        if booking['car_id'] != car_id:
            continue
        if booking['status'] == 'cancelled':
            continue
        # Overlap check: new_start < existing_end AND new_end > existing_start
        if start_date < booking['end_date'] and end_date > booking['start_date']:
            return True
    return False


def book_car(car_id, renter_id, start_date, end_date):
    """
    Book a car for a date range.
    Validates ownership, conflicts, and date logic.
    """
    car = db_store.find_by_id('cars.json', car_id)
    if not car:
        return {'success': False, 'message': 'Car not found'}
    #Sadeq.Shryim: (3/18: Bug fix added extra fail condition)
    if car['owner_id'] == renter_id:
        return {'success': False, 'message': 'You cannot book your own car'}

    if not car.get('is_active', True):
        return {'success': False, 'message': 'This listing is no longer active'}

    # Validate dates
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return {'success': False, 'message': 'Invalid date format. Use YYYY-MM-DD'}

    days = (end - start).days
    if days <= 0:
        return {'success': False, 'message': 'End date must be after start date'}

    # Check availability
    if not _is_available(car, start_date, end_date):
        return {'success': False, 'message': 'This car is not available for the selected dates'}

    # Check conflicts
    if _has_conflict(car_id, start_date, end_date):
        return {'success': False, 'message': 'This car is already booked for overlapping dates'}

    total_price = round(days * car['daily_price'], 2)

    booking = create_booking(car_id, renter_id, car['owner_id'],
                             start_date, end_date, total_price)
    db_store.add('bookings.json', booking)

    # Notify owner
    renter = db_store.find_by_id('users.json', renter_id)
    renter_email = renter['email'] if renter else 'Unknown'
    notif = create_notification(
        car['owner_id'],
        f"📋 New booking: {car['make']} {car['model']} "
        f"from {start_date} to {end_date} by {renter_email}",
        'booking'
    )
    db_store.add('notifications.json', notif)

    return {
        'success': True,
        'message': f'Booking confirmed! Total: ${total_price:.2f} ({days} days)',
        'booking': booking
    }


def get_user_bookings(user_id, as_renter=True):
    """Get bookings for a user (as renter or owner)."""
    bookings = db_store.load_all('bookings.json')
    field = 'renter_id' if as_renter else 'owner_id'
    user_bookings = [b for b in bookings if b[field] == user_id]
    user_bookings.sort(key=lambda b: b['created_at'], reverse=True)
    return user_bookings


def cancel_booking(booking_id, user_id):
    """Cancel a booking (either party can cancel)."""
    booking = db_store.find_by_id('bookings.json', booking_id)
    if not booking:
        return {'success': False, 'message': 'Booking not found'}

    if booking['renter_id'] != user_id and booking['owner_id'] != user_id:
        return {'success': False, 'message': 'You can only cancel your own bookings'}

    if booking['status'] == 'cancelled':
        return {'success': False, 'message': 'Booking is already cancelled'}

    db_store.update('bookings.json', booking_id, {'status': 'cancelled'})

    # Notify the other party
    other_id = (booking['owner_id'] if user_id == booking['renter_id']
                else booking['renter_id'])
    car = db_store.find_by_id('cars.json', booking['car_id'])
    car_name = f"{car['make']} {car['model']}" if car else "Unknown car"

    notif = create_notification(
        other_id,
        f"Booking cancelled: {car_name} ({booking['start_date']} – {booking['end_date']})",
        'booking'
    )
    db_store.add('notifications.json', notif)

    return {'success': True, 'message': 'Booking cancelled'}


def get_booking_by_id(booking_id):
    """Get a single booking by ID."""
    return db_store.find_by_id('bookings.json', booking_id)
