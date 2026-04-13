"""
Mediator Pattern — UIMediator

Coordinates communication between different UI components (CLI screens)
so they don't reference each other directly. Components register with the
mediator and route events (e.g., navigation, data passing) through it.
"""


class UIMediator:
    """Central mediator that coordinates CLI component communication."""

    def __init__(self):
        self._components = {}
        self._shared_data = {}

    def register(self, name, component):
        """Register a UI component by name."""
        self._components[name] = component
        if hasattr(component, 'set_mediator'):
            component.set_mediator(self)

    def notify(self, sender, event, data=None):
        """
        Route an event from one component to the appropriate target.
        """
        self._shared_data[event] = data

        # Event routing table
        event_routes = {
            'navigate_owner_menu': 'owner',
            'navigate_renter_menu': 'renter',
            'navigate_messages': 'messages',
            'navigate_payment': 'payment',
            'navigate_main': 'main',
            'navigate_auth': 'auth',
            'car_selected': 'renter',
            'booking_created': 'payment',
            'refresh_notifications': 'main',
        }

        target_name = event_routes.get(event)
        if target_name and target_name in self._components:
            component = self._components[target_name]
            if hasattr(component, 'receive'):
                component.receive(event, data)

    def get_data(self, key):
        """Retrieve shared data by key."""
        return self._shared_data.get(key)

    def set_data(self, key, value):
        """Store shared data by key."""
        self._shared_data[key] = value

    def get_component(self, name):
        """Get a registered component by name."""
        return self._components.get(name)
