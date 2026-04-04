from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
from services import payment_service, booking_service

router = APIRouter()

def get_current_user(x_auth_token: str = Header(default=None)):
    if not x_auth_token:
        raise HTTPException(status_code=401, detail="Missing X-Auth-Token header")
    return x_auth_token

class PaymentModel(BaseModel):
    booking_id: str

@router.post("/")
def process_payment(data: PaymentModel, user_id: str = Depends(get_current_user)):
    booking = booking_service.get_booking_by_id(data.booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found.")

    if booking['renter_id'] != user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to pay for this booking.")

    if booking.get('paid'):
        raise HTTPException(status_code=400, detail="This booking has already been paid for.")

    result = payment_service.process_payment(
        renter_id=booking['renter_id'],
        owner_id=booking['owner_id'],
        amount=booking['total_price'],
        booking_id=data.booking_id
    )
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "Payment failed."))
    return {"message": "Payment successful"}
