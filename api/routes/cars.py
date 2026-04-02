from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
from typing import List, Optional, Any
from services import car_service

router = APIRouter()

def get_current_user(x_auth_token: str = Header(default=None)):
    if not x_auth_token:
        raise HTTPException(status_code=401, detail="Missing X-Auth-Token header")
    return x_auth_token

class AvailabilityModel(BaseModel):
    start: str
    end: str

class CarCreateModel(BaseModel):
    make: str
    model: str
    year: int
    mileage: int
    daily_price: float
    location: str
    features: Optional[List[str]] = []
    availability: Optional[List[AvailabilityModel]] = []

class CarUpdateModel(BaseModel):
    daily_price: Optional[float] = None
    availability: Optional[List[AvailabilityModel]] = None

@router.get("/")
def get_active_listings():
    return car_service.get_active_listings()

@router.get("/my-cars")
def get_my_cars(user_id: str = Depends(get_current_user)):
    return car_service.get_owner_listings(user_id)

@router.post("/")
def create_listing(car: CarCreateModel, user_id: str = Depends(get_current_user)):
    avail_dicts = [{"start": a.start, "end": a.end} for a in car.availability]
    car_dict = car_service.list_car(
        owner_id=user_id,
        make=car.make,
        model=car.model,
        year=car.year,
        mileage=car.mileage,
        daily_price=car.daily_price,
        location=car.location,
        features=car.features,
        availability=avail_dicts
    )
    return {"message": "Car listed successfully", "car": car_dict}

@router.put("/{car_id}")
def update_listing(car_id: str, updates: CarUpdateModel, user_id: str = Depends(get_current_user)):
    avail_dicts = None
    if updates.availability is not None:
        avail_dicts = [{"start": a.start, "end": a.end} for a in updates.availability]
    
    updated_car = car_service.update_listing(car_id, user_id, updates.daily_price, avail_dicts)
    if not updated_car:
        raise HTTPException(status_code=403, detail="Could not update car or not authorized.")
    return {"message": "Car updated successfully", "car": updated_car}

@router.delete("/{car_id}")
def delete_listing(car_id: str, user_id: str = Depends(get_current_user)):
    success = car_service.remove_listing(car_id, user_id)
    if not success:
        raise HTTPException(status_code=403, detail="Could not delete car or not authorized.")
    return {"message": "Car deleted successfully"}
