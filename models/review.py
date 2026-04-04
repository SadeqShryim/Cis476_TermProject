"""Review model."""

import uuid
from datetime import datetime

def create_review(booking_id, reviewer_id, reviewed_id, role, rating, comment):
    """
    Creates a new review dictionary.

    Args:
        booking_id (str): The ID of the booking this review is for.
        reviewer_id (str): The ID of the user writing the review.
        reviewed_id (str): The ID of the user being reviewed.
        role (str): The role of the reviewed user ('owner' or 'renter').
        rating (int): The numerical rating (e.g., 1-5).
        comment (str): The text of the review.
    
    Returns:
        dict: The new review object.
    """
    if not 1 <= rating <= 5:
        raise ValueError("Rating must be between 1 and 5.")

    return {
        'id': str(uuid.uuid4()),
        'booking_id': booking_id,
        'reviewer_id': reviewer_id,
        'reviewed_id': reviewed_id,
        'reviewed_role': role, # 'owner' or 'renter'
        'rating': rating,
        'comment': comment,
        'created_at': datetime.now().isoformat()
    }
