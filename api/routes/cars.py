from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
from typing import List, Optional, Any
from services import car_service
from patterns.builder import CarListingBuilder

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
    return car_service.get_user_listings(user_id)

@router.post("/")
def create_listing(car: CarCreateModel, user_id: str = Depends(get_current_user)):
    builder = CarListingBuilder()
    
    builder.set_owner(user_id)
    builder.set_make(car.make)
    builder.set_model(car.model)
    builder.set_year(car.year)
    builder.set_mileage(car.mileage)
    builder.set_daily_price(car.daily_price)
    builder.set_location(car.location)

    if car.features:
        for feature in car.features:
            builder.add_feature(feature)
        
    if car.availability:
        for avail in car.availability:
            builder.add_availability(avail.start, avail.end)

    try:
        car_data = builder.build()
        result = car_service.create_listing(car_data)
        if result.get("success"):
            return {"message": "Car listed successfully", "car": result['car']}
        else:
            raise HTTPException(status_code=400, detail=result.get("message", "Failed to create car listing."))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{car_id}")
def update_listing(car_id: str, updates: CarUpdateModel, user_id: str = Depends(get_current_user)):
    update_data = {}
    if updates.daily_price is not None:
        update_data["daily_price"] = updates.daily_price
    if updates.availability is not None:
        update_data["availability"] = [{"start": a.start, "end": a.end} for a in updates.availability]

    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided.")

    result = car_service.update_listing(car_id, update_data, user_id)
    if not result.get("success"):
        raise HTTPException(status_code=403, detail=result.get("message", "Could not update car or not authorized."))
    return {"message": "Car updated successfully", "car": result.get("car")}

@router.delete("/{car_id}")
def delete_listing(car_id: str, user_id: str = Depends(get_current_user)):
    success = car_service.delete_listing(car_id, user_id)
    if not success:
        raise HTTPException(status_code=403, detail="Could not delete car or not authorized.")
    return {"message": "Car deleted successfully"}
