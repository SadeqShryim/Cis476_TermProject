from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
from services import payment_service

router = APIRouter()

def get_current_user(x_auth_token: str = Header(default=None)):
    if not x_auth_token:
        raise HTTPException(status_code=401, detail="Missing X-Auth-Token header")
    return x_auth_token

class PaymentModel(BaseModel):
    booking_id: str

@router.post("/")
def process_payment(data: PaymentModel, user_id: str = Depends(get_current_user)):
    success = payment_service.process_payment(data.booking_id, user_id)
    if not success:
        raise HTTPException(status_code=400, detail="Payment failed. Insufficient funds, already paid, or not authorized.")
    return {"message": "Payment successful"}
