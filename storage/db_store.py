import os
import json
from sqlalchemy import create_engine, Column, String, Float, Integer, Boolean, JSON
from sqlalchemy.orm import declarative_base, sessionmaker

# Data directory sits at project root / data /
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, 'driveshare.db')

engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    email = Column(String, index=True)
    password_hash = Column(String)
    security_questions = Column(JSON)
    balance = Column(Float)
    created_at = Column(String)

class CarModel(Base):
    __tablename__ = "cars"
    id = Column(String, primary_key=True, index=True)
    owner_id = Column(String, index=True)
    make = Column(String)
    model = Column(String)
    year = Column(Integer)
    mileage = Column(Integer)
    daily_price = Column(Float)
    location = Column(String)
    features = Column(JSON)
    availability = Column(JSON)
    watchers = Column(JSON)
    is_active = Column(Boolean)
    created_at = Column(String)

class BookingModel(Base):
    __tablename__ = "bookings"
    id = Column(String, primary_key=True, index=True)
    car_id = Column(String, index=True)
    renter_id = Column(String, index=True)
    owner_id = Column(String, index=True)
    start_date = Column(String)
    end_date = Column(String)
    total_price = Column(Float)
    status = Column(String)
    paid = Column(Boolean)
    created_at = Column(String)

class MessageModel(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True, index=True)
    sender_id = Column(String, index=True)
    receiver_id = Column(String, index=True)
    content = Column(String)
    read = Column(Boolean)
    timestamp = Column(String)

class NotificationModel(Base):
    __tablename__ = "notifications"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    content = Column(String)
    type = Column(String)
    read = Column(Boolean)
    timestamp = Column(String)

class ReviewModel(Base):
    __tablename__ = "reviews"
    id = Column(String, primary_key=True, index=True)
    booking_id = Column(String, index=True)
    reviewer_id = Column(String, index=True)
    reviewed_id = Column(String, index=True)
    reviewed_role = Column(String)
    rating = Column(Integer)
    comment = Column(String)
    created_at = Column(String)

class TestModel(Base):
    __tablename__ = "tests"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)

Base.metadata.create_all(bind=engine)

TABLE_MAP = {
    "users.json": UserModel,
    "cars.json": CarModel,
    "bookings.json": BookingModel,
    "messages.json": MessageModel,
    "notifications.json": NotificationModel,
    "reviews.json": ReviewModel,
    "test.json": TestModel
}

def _get_model(filename):
    return TABLE_MAP.get(filename)

def _model_to_dict(model_obj):
    if not model_obj: return None
    d = {c.name: getattr(model_obj, c.name) for c in model_obj.__table__.columns}
    # SQLite JSON columns sometimes return actual dicts/lists, sometimes strings. 
    # SQLAlchemy's JSON type handles serialization automatically usually.
    return d

def _dict_to_model(ModelClass, item_dict):
    return ModelClass(**item_dict)

def load_all(filename):
    """Load all records."""
    ModelClass = _get_model(filename)
    if not ModelClass: return []
    with SessionLocal() as db:
        records = db.query(ModelClass).all()
        return [_model_to_dict(r) for r in records]

def save_all(filename, data):
    """Overwrite entirely. Mostly used in tests now or after massive mutations."""
    ModelClass = _get_model(filename)
    if not ModelClass: return
    with SessionLocal() as db:
        db.query(ModelClass).delete()
        for item in data:
            db.add(_dict_to_model(ModelClass, item))
        db.commit()

def add(filename, item):
    """Append a single record."""
    ModelClass = _get_model(filename)
    if not ModelClass: return item
    with SessionLocal() as db:
        # Check if exists to avoid PK errors if a test double-adds
        existing = db.query(ModelClass).filter(ModelClass.id == item['id']).first()
        if not existing:
            db.add(_dict_to_model(ModelClass, item))
            db.commit()
    return item

def find_by_id(filename, item_id):
    """Find a single record by 'id'."""
    ModelClass = _get_model(filename)
    if not ModelClass: return None
    with SessionLocal() as db:
        record = db.query(ModelClass).filter(ModelClass.id == item_id).first()
        return _model_to_dict(record)

def update(filename, item_id, updates):
    """Update a record by id."""
    ModelClass = _get_model(filename)
    if not ModelClass: return None
    with SessionLocal() as db:
        record = db.query(ModelClass).filter(ModelClass.id == item_id).first()
        if record:
            for k, v in updates.items():
                if hasattr(record, k):
                    setattr(record, k, v)
            db.commit()
            db.refresh(record)
            return _model_to_dict(record)
    return None

def delete(filename, item_id):
    """Remove a record by id."""
    ModelClass = _get_model(filename)
    if not ModelClass: return False
    with SessionLocal() as db:
        record = db.query(ModelClass).filter(ModelClass.id == item_id).first()
        if record:
            db.delete(record)
            db.commit()
            return True
    return False

def find_by_field(filename, field, value):
    """Return all records where record[field] == value."""
    ModelClass = _get_model(filename)
    if not ModelClass: return []
    with SessionLocal() as db:
        column = getattr(ModelClass, field)
        records = db.query(ModelClass).filter(column == value).all()
        return [_model_to_dict(r) for r in records]
