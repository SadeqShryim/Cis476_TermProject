"""
Singleton Pattern — SessionManager

Ensures only ONE instance of the session manager exists across the entire
application. Used to track the currently logged-in user.
"""


class SessionManager:
    """Manages the current user session. Only one instance can exist."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._current_user = None
        return cls._instance

    def login(self, user):
        """Set the current user session."""
        self._current_user = user

    def logout(self):
        """Clear the current user session."""
        self._current_user = None

    def get_current_user(self):
        """Return the currently logged-in user dict, or None."""
        return self._current_user

    def is_authenticated(self):
        """Return True if a user is currently logged in."""
        return self._current_user is not None

    def update_user(self, updates):
        """Update fields on the in-memory session user."""
        if self._current_user:
            self._current_user.update(updates)

    def refresh(self):
        """Reload the current user from storage to pick up balance changes, etc."""
        if self._current_user:
            from storage import db_store
            fresh = db_store.find_by_id('users.json', self._current_user['id'])
            if fresh:
                self._current_user = fresh

    @classmethod
    def reset(cls):
        """Reset the singleton (for testing)."""
        cls._instance = None
