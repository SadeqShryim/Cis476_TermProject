"""
Builder Pattern — CarListingBuilder

This constructs a complex Car listing objects step by step and handles
optional/variable attributes in a cleaner way.
"""

from models.car import create_car


class CarListingBuilder:
    """Builds a car listing object step by step."""

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset all fields to start a new build."""
        self._owner_id = None
        self._make = None
        self._model = None
        self._year = None
        self._mileage = 0
        self._daily_price = None
        self._location = None
        self._features = []
        self._availability = []
        return self

    def set_owner(self, owner_id):
        self._owner_id = owner_id
        return self

    def set_make(self, make):
        self._make = make
        return self

    def set_model(self, model):
        self._model = model
        return self

    def set_year(self, year):
        self._year = int(year)
        return self

    def set_mileage(self, mileage):
        self._mileage = int(mileage)
        return self

    def set_daily_price(self, price):
        self._daily_price = float(price)
        return self

    def set_location(self, location):
        self._location = location
        return self

    def add_feature(self, feature):
        self._features.append(feature)
        return self

    def add_availability(self, start_date, end_date):
        self._availability.append({'start': start_date, 'end': end_date})
        return self

    def validate(self):
        """Ensure all required fields are set before building."""
        required = {
            'owner_id': self._owner_id,
            'make': self._make,
            'model': self._model,
            'year': self._year,
            'daily_price': self._daily_price,
            'location': self._location
        }
        missing = [k for k, v in required.items() if v is None]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")
        return True

    def build(self):
        """Validate and construct the final car dict."""
        self.validate()
        car = create_car(
            owner_id=self._owner_id,
            make=self._make,
            model=self._model,
            year=self._year,
            mileage=self._mileage,
            daily_price=self._daily_price,
            location=self._location,
            features=list(self._features),
            availability=list(self._availability)
        )
        return car
