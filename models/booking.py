"""Booking model."""

import uuid
from datetime import datetime


def create_booking(car_id, renter_id, owner_id, start_date, end_date, total_price):
    """
    Create a new booking dict.
    """
    return {
        'id': str(uuid.uuid4()),
        'car_id': car_id,
        'renter_id': renter_id,
        'owner_id': owner_id,
        'start_date': start_date,
        'end_date': end_date,
        'total_price': float(total_price),
        'status': 'confirmed',
        'paid': False,
        'created_at': datetime.now().isoformat()
    }
