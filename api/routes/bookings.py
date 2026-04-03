from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
from typing import Optional
from services import booking_service

router = APIRouter()

def get_current_user(x_auth_token: str = Header(default=None)):
    if not x_auth_token:
        raise HTTPException(status_code=401, detail="Missing X-Auth-Token header")
    return x_auth_token

class SearchQueryModel(BaseModel):
    location: Optional[str] = None
    make: Optional[str] = None
    max_price: Optional[float] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class BookCarModel(BaseModel):
    car_id: str
    owner_id: str
    start_date: str
    end_date: str

@router.post("/search")
def search_cars(query: SearchQueryModel):
    results = booking_service.search_cars(
        location=query.location,
        make=query.make,
        max_price=query.max_price,
        start_date=query.start_date,
        end_date=query.end_date
    )
    return {"results": results}

@router.post("/")
def book_car(data: BookCarModel, user_id: str = Depends(get_current_user)):
    result = booking_service.book_car(
        car_id=data.car_id,
        renter_id=user_id,
        start_date=data.start_date,
        end_date=data.end_date
    )
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "Cannot book car. It may be your own car or unavailable dates."))
    return {"message": "Booking successful", "booking": result.get("booking")}

@router.post("/{booking_id}/cancel")
def cancel_booking(booking_id: str, user_id: str = Depends(get_current_user)):
    result = booking_service.cancel_booking(booking_id, user_id)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "Cancellation failed or unauthorized."))
    return {"message": "Booking cancelled successfully"}

@router.get("/as-renter")
def get_renter_bookings(user_id: str = Depends(get_current_user)):
    return booking_service.get_user_bookings(user_id)

@router.get("/as-owner")
def get_owner_bookings(user_id: str = Depends(get_current_user)):
    return booking_service.get_user_bookings(user_id, as_renter=False)
