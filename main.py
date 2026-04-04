import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from storage import db_store

# Ensure data directory exists
db_store.Base.metadata.create_all(bind=db_store.engine)

app = FastAPI(title="DriveShare API", description="Phase 2 Web Application Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Since frontend will be on another port locally
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from api.routes import auth, cars, bookings, user, payments, reviews
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(cars.router, prefix="/api/cars", tags=["Cars"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["Bookings"])
app.include_router(user.router, prefix="/api/user", tags=["User"])
app.include_router(payments.router, prefix="/api/payments", tags=["Payments"])
app.include_router(reviews.router, prefix="/api/reviews", tags=["Reviews"])
# ...

@app.get("/")
def root():
    return {"message": "DriveShare API is running."}

if __name__ == '__main__':
    import uvicorn
    # Restore any persisted watchers into the in-memory WatchManager
    from services.watch_service import restore_watchers
    restore_watchers()
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
