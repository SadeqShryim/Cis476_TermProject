"""Review service for handling business logic of reviews and ratings."""

from datetime import datetime
from storage import db_store
from models.review import create_review

def leave_review(booking_id, reviewer_id, rating, comment):
    """
    Allows a renter or owner to leave a review after a booking is complete.
    """
    booking = db_store.find_by_id('bookings.json', booking_id)
    if not booking:
        return {'success': False, 'message': 'Booking not found.'}

    # 1. Validate that the reviewer is part of the booking
    if reviewer_id not in [booking['renter_id'], booking['owner_id']]:
        return {'success': False, 'message': 'You are not authorized to review this booking.'}

    # 2. Determine who is being reviewed
    if reviewer_id == booking['renter_id']:
        reviewed_id = booking['owner_id']
        reviewed_role = 'owner'
    else: # reviewer is the owner
        reviewed_id = booking['renter_id']
        reviewed_role = 'renter'

    # 3. Check if the booking is completed (end date is in the past)
    if datetime.strptime(booking['end_date'], '%Y-%m-%d') >= datetime.now():
        return {'success': False, 'message': 'You can only review a booking after it has been completed.'}

    # 4. Check if this user has already reviewed this booking for the other party
    reviews = db_store.load_all('reviews.json')
    existing_review = next((r for r in reviews if r['booking_id'] == booking_id and r['reviewer_id'] == reviewer_id), None)
    if existing_review:
        return {'success': False, 'message': 'You have already submitted a review for this booking.'}

    # 5. Create and save the review
    try:
        review = create_review(booking_id, reviewer_id, reviewed_id, reviewed_role, rating, comment)
        db_store.add('reviews.json', review)
        print(f"DEBUG: Review saved: {review}") # DEBUG
        return {'success': True, 'message': 'Review submitted successfully!', 'review': review}
    except ValueError as e:
        return {'success': False, 'message': str(e)}

def get_reviews_for_user(user_id):
    """
    Get all reviews where the given user was the one being reviewed.
    """
    reviews = db_store.load_all('reviews.json')
    user_reviews = [r for r in reviews if r['reviewed_id'] == user_id]
    return user_reviews

def get_reviews_by_booking(booking_id):
    """
    Get all reviews associated with a specific booking.
    """
    reviews = db_store.load_all('reviews.json')
    print(f"DEBUG: All reviews from DB: {reviews}") # DEBUG
    print(f"DEBUG: Filtering for booking_id: {booking_id}") # DEBUG
    booking_reviews = [r for r in reviews if r['booking_id'] == booking_id]
    return booking_reviews
