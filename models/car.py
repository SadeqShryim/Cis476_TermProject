"""Car listing model."""

import uuid
from datetime import datetime


def create_car(owner_id, make, model, year, mileage, daily_price, location,
               features=None, availability=None):
    """
    Create a new car listing dict.
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
