"""Watch service — watch/unwatch cars, trigger observer notifications."""

from storage import db_store
from services.car_service import watch_manager
from services.notification_service import add_notification
from patterns.observer import WatcherObserver


def _make_callback():
    """Create a notification callback for the observer."""
    def notification_callback(user_id, message):
        add_notification(user_id, message, 'watch')
    return notification_callback


def watch_car(user_id, car_id, max_price=None, desired_start=None, desired_end=None):
    """
    Start watching a car with optional criteria.
    Uses the Observer pattern to register the watcher.
    """
    car = db_store.find_by_id('cars.json', car_id)
    if not car:
        return {'success': False, 'message': 'Car not found'}

    if car['owner_id'] == user_id:
        return {'success': False, 'message': 'You cannot watch your own car'}

    # Check if already watching
    watchers = car.get('watchers', [])
    for w in watchers:
        if w['user_id'] == user_id:
            return {'success': False, 'message': 'You are already watching this car'}

    # Save watcher data to car record (persistence)
    watcher_data = {
        'user_id': user_id,
        'max_price': max_price,
        'desired_start': desired_start,
        'desired_end': desired_end
    }
    watchers.append(watcher_data)
    db_store.update('cars.json', car_id, {'watchers': watchers})

    # Register observer with the in-memory WatchManager
    observer = WatcherObserver(
        user_id=user_id,
        max_price=max_price,
        desired_start=desired_start,
        desired_end=desired_end,
        callback=_make_callback()
    )
    watch_manager.add_watcher(car_id, observer)

    return {'success': True, 'message': f"Now watching {car['make']} {car['model']}"}


def unwatch_car(user_id, car_id):
    """Stop watching a car."""
    car = db_store.find_by_id('cars.json', car_id)
    if not car:
        return {'success': False, 'message': 'Car not found'}

    watchers = car.get('watchers', [])
    new_watchers = [w for w in watchers if w['user_id'] != user_id]

    if len(new_watchers) == len(watchers):
        return {'success': False, 'message': 'You are not watching this car'}

    db_store.update('cars.json', car_id, {'watchers': new_watchers})
    watch_manager.remove_watcher(car_id, user_id)

    return {'success': True, 'message': 'Stopped watching this car'}


def get_watched_cars(user_id):
    """Return a list of cars the user is watching, with their criteria."""
    cars = db_store.load_all('cars.json')
    watched = []
    for car in cars:
        if not car.get('is_active', True):
            continue
        for w in car.get('watchers', []):
            if w['user_id'] == user_id:
                watched.append({'car': car, 'criteria': w})
                break
    return watched


def restore_watchers():
    """
    Reload watcher registrations from JSON into the in-memory WatchManager.
    Must be called on application startup so observers are listening.
    """
    cars = db_store.load_all('cars.json')
    for car in cars:
        for w in car.get('watchers', []):
            observer = WatcherObserver(
                user_id=w['user_id'],
                max_price=w.get('max_price'),
                desired_start=w.get('desired_start'),
                desired_end=w.get('desired_end'),
                callback=_make_callback()
            )
            watch_manager.add_watcher(car['id'], observer)
