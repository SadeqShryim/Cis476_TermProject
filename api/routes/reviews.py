"""API routes for reviews and ratings."""

from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel, conint
from typing import List
from services import review_service

router = APIRouter()

def get_current_user(x_auth_token: str = Header(default=None)):
    if not x_auth_token:
        raise HTTPException(status_code=401, detail="Missing X-Auth-Token header")
    return x_auth_token

class ReviewCreateModel(BaseModel):
    booking_id: str
    rating: conint(ge=1, le=5) # Rating must be between 1 and 5
    comment: str

@router.post("/", status_code=201)
def create_review_endpoint(review_data: ReviewCreateModel, reviewer_id: str = Depends(get_current_user)):
    """
    Endpoint to create a new review for a completed booking.
    The reviewer is determined from the auth token.
    """
    result = review_service.leave_review(
        booking_id=review_data.booking_id,
        reviewer_id=reviewer_id,
        rating=review_data.rating,
        comment=review_data.comment
    )
    if not result.get('success'):
        raise HTTPException(status_code=400, detail=result.get('message'))
    return result

@router.get("/user/{user_id}")
def get_user_reviews_endpoint(user_id: str):
    """
    Endpoint to get all reviews for a specific user.
    """
    reviews = review_service.get_reviews_for_user(user_id)
    return {"user_id": user_id, "reviews": reviews}

@router.get("/booking/{booking_id}")
def get_booking_reviews_endpoint(booking_id: str):
    """
    Endpoint to get all reviews associated with a specific booking.
    """
    reviews = review_service.get_reviews_by_booking(booking_id)
    return {"booking_id": booking_id, "reviews": reviews}
