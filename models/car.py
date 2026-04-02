"""Car listing model."""

import uuid
from datetime import datetime


def create_car(owner_id, make, model, year, mileage, daily_price, location,
               features=None, availability=None):
    """
    Create a new car listing dict.
    
    Args:
        owner_id: ID of the car owner
        make: Car manufacturer (e.g., Toyota)
        model: Car model (e.g., Camry)
        year: Model year
        mileage: Current mileage
        daily_price: Rental price per day
        location: Pick-up location
        features: Optional list of features (e.g., ['Bluetooth', 'GPS'])
        availability: Optional list of dicts {'start': 'YYYY-MM-DD', 'end': 'YYYY-MM-DD'}
    """
    return {
        'id': str(uuid.uuid4()),
        'owner_id': owner_id,
        'make': make,
        'model': model,
        'year': int(year),
        'mileage': int(mileage),
        'daily_price': float(daily_price),
        'location': location,
        'features': features or [],
        'availability': availability or [],
        'watchers': [],
        'is_active': True,
        'created_at': datetime.now().isoformat()
    }
