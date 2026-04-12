"""
Observer Pattern — Car Watch System

Subject (car listing) notifies Observer (renter watcher) when the car's
price drops or availability changes. Watchers define criteria and receive
targeted notifications.
"""


class CarSubject:
    """Subject — represents a car listing being watched by renters."""

    def __init__(self):
        self._observers = []

    def attach(self, observer):
        """Register an observer to this subject."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """Remove an observer from this subject."""
        self._observers = [o for o in self._observers if o is not observer]

    def detach_by_user(self, user_id):
        """Remove all observers for a given user."""
        self._observers = [o for o in self._observers if o.user_id != user_id]

    def notify(self, car_data, change_type):
        """Notify all registered observers of a change."""
        for observer in self._observers:
            observer.update(car_data, change_type)


class WatcherObserver:
    """Observer — a renter watching a car with optional criteria."""

    def __init__(self, user_id, max_price=None, desired_start=None,
                 desired_end=None, callback=None):
        self.user_id = user_id
        self.max_price = max_price
        self.desired_start = desired_start
        self.desired_end = desired_end
        self.callback = callback  # function(user_id, message) to deliver notification

    def update(self, car_data, change_type):
        """Called by the subject when the car changes."""
        message = ""

        if change_type == 'price_drop':
            if self.max_price and car_data['daily_price'] <= self.max_price:
                message = (f"Price drop! {car_data['make']} {car_data['model']} "
                           f"is now ${car_data['daily_price']:.2f}/day "
                           f"(your max: ${self.max_price:.2f})")
            else:
                message = (f"Price update: {car_data['make']} {car_data['model']} "
                           f"is now ${car_data['daily_price']:.2f}/day")

        elif change_type == 'availability':
            message = (f"Availability update: {car_data['make']} {car_data['model']} "
                       f"has new availability!")

        if message and self.callback:
            self.callback(self.user_id, message)


class WatchManager:
    """Manages all car subjects and their observer registrations."""

    def __init__(self):
        self._subjects = {}  # car_id -> CarSubject

    def get_or_create_subject(self, car_id):
        """Get or create a CarSubject for the given car."""
        if car_id not in self._subjects:
            self._subjects[car_id] = CarSubject()
        return self._subjects[car_id]

    def add_watcher(self, car_id, observer):
        """Register a watcher for a car."""
        subject = self.get_or_create_subject(car_id)
        subject.attach(observer)

    def remove_watcher(self, car_id, user_id):
        """Remove a user's watcher from a car."""
        if car_id in self._subjects:
            self._subjects[car_id].detach_by_user(user_id)

    def notify_car_change(self, car_id, car_data, change_type):
        """Notify all watchers of a car about a change."""
        if car_id in self._subjects:
            self._subjects[car_id].notify(car_data, change_type)
