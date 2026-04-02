"""Car service — CRUD for car listings, availability checks."""

from storage import db_store
from patterns.observer import WatchManager

# Global watch manager — shared across the app
watch_manager = WatchManager()


def create_listing(car_data):
    """
    Persist a car listing (already built by CarListingBuilder).
    
    Args:
        car_data: dict from CarListingBuilder.build()
    """
    db_store.add('cars.json', car_data)
    return {'success': True, 'message': 'Car listed successfully!', 'car': car_data}


def get_all_listings():
    """Return all car listings."""
    return db_store.load_all('cars.json')


def get_active_listings():
    """Return only active (non-deleted) car listings."""
    cars = db_store.load_all('cars.json')
    return [c for c in cars if c.get('is_active', True)]


def get_user_listings(owner_id):
    """Return all listings owned by a specific user."""
    return db_store.find_by_field('cars.json', 'owner_id', owner_id)


def get_car_by_id(car_id):
    """Get a single car by ID."""
    return db_store.find_by_id('cars.json', car_id)


def update_listing(car_id, updates, owner_id):
    """
    Update a car listing. Notifies watchers on price drops and availability changes.
    Uses the Observer pattern via WatchManager.
    """
    car = db_store.find_by_id('cars.json', car_id)
    if not car:
        return {'success': False, 'message': 'Car not found'}
    if car['owner_id'] != owner_id:
        return {'success': False, 'message': 'You can only update your own listings'}

    old_price = car['daily_price']

    updated = db_store.update('cars.json', car_id, updates)

    # Observer pattern — notify watchers
    if 'daily_price' in updates and updates['daily_price'] < old_price:
        watch_manager.notify_car_change(car_id, updated, 'price_drop')
    if 'availability' in updates:
        watch_manager.notify_car_change(car_id, updated, 'availability')

    return {'success': True, 'message': 'Listing updated!', 'car': updated}


def delete_listing(car_id, owner_id):
    """Soft-delete a car listing (mark as inactive)."""
    car = db_store.find_by_id('cars.json', car_id)
    if not car:
        return {'success': False, 'message': 'Car not found'}
    if car['owner_id'] != owner_id:
        return {'success': False, 'message': 'You can only delete your own listings'}

    db_store.update('cars.json', car_id, {'is_active': False})
    return {'success': True, 'message': 'Listing removed'}
