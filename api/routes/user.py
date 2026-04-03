from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
from services import watch_service, notification_service, message_service
from storage import db_store

router = APIRouter()

def get_current_user(x_auth_token: str = Header(default=None)):
    if not x_auth_token:
        raise HTTPException(status_code=401, detail="Missing X-Auth-Token header")
    return x_auth_token

class WatchModel(BaseModel):
    car_id: str
    target_price: float

class MessageModel(BaseModel):
    receiver_id: str
    content: str

@router.get("/profile")
def get_profile(user_id: str = Depends(get_current_user)):
    user = db_store.find_by_id('users.json', user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Return profile without hashing defaults
    return {
        "id": user["id"],
        "email": user["email"],
        "balance": user["balance"],
        "created_at": user["created_at"]
    }

@router.get("/notifications")
def get_notifications(user_id: str = Depends(get_current_user)):
    return notification_service.get_notifications(user_id)

@router.post("/notifications/mark-read")
def mark_read(user_id: str = Depends(get_current_user)):
    notification_service.mark_all_read(user_id)
    return {"message": "Notifications marked read"}

@router.get("/watched")
def get_watched_cars(user_id: str = Depends(get_current_user)):
    return watch_service.get_watched_cars(user_id)

@router.post("/watch")
def watch_car(data: WatchModel, user_id: str = Depends(get_current_user)):
    result = watch_service.watch_car(user_id, data.car_id, data.target_price)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return {"message": result['message']}

@router.post("/unwatch/{car_id}")
def unwatch_car(car_id: str, user_id: str = Depends(get_current_user)):
    result = watch_service.unwatch_car(user_id, car_id)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return {"message": result['message']}

@router.get("/messages")
def get_conversations(user_id: str = Depends(get_current_user)):
    return message_service.get_conversations(user_id)

@router.get("/messages/{other_user_id}")
def get_messages(other_user_id: str, user_id: str = Depends(get_current_user)):
    return message_service.get_conversation(user_id, other_user_id)

@router.post("/messages")
def send_message(data: MessageModel, user_id: str = Depends(get_current_user)):
    msg = message_service.send_message(user_id, data.receiver_id, data.content)
    if not msg:
        raise HTTPException(status_code=400, detail="Cannot send message. Perhaps you are messaging yourself.")
    return {"message": "Message sent", "data": msg}
