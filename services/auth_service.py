"""Auth service — registration, login, logout, password recovery."""

from storage import db_store
from models.user import create_user, hash_password, verify_password
from patterns.singleton import SessionManager
from patterns.chain_of_responsibility import build_security_chain


def register(email, password, security_questions):
    """
    Register a new user.
    """
    # Check duplicate email
    existing = db_store.find_by_field('users.json', 'email', email.lower().strip())
    if existing:
        return {'success': False, 'message': 'Email already registered'}

    if len(security_questions) != 3:
        return {'success': False, 'message': 'Exactly 3 security questions required'}

    if len(password) < 4:
        return {'success': False, 'message': 'Password must be at least 4 characters'}

    user = create_user(email, password, security_questions)
    db_store.add('users.json', user)

    # Auto-login after registration
    session = SessionManager()
    session.login(user)

    return {'success': True, 'message': 'Registration successful!', 'user': user}


def login(email, password):
    """Authenticate a user and start a session."""
    users = db_store.find_by_field('users.json', 'email', email.lower().strip())
    if not users:
        return {'success': False, 'message': 'Invalid email or password'}

    user = users[0]
    if not verify_password(password, user['password_hash']):
        return {'success': False, 'message': 'Invalid email or password'}

    session = SessionManager()
    session.login(user)

    return {'success': True, 'message': 'Login successful!', 'user': user}


def logout():
    """End the current session."""
    session = SessionManager()
    session.logout()
    return {'success': True, 'message': 'Logged out successfully'}


def get_security_questions(email):
    """Return the 3 security question prompts for the given email, or None."""
    users = db_store.find_by_field('users.json', 'email', email.lower().strip())
    if not users:
        return None
    return [sq['question'] for sq in users[0]['security_questions']]


def recover_password(email, answers, new_password):
    """
    Recover password using Chain of Responsibility pattern.
    User must answer all 3 security questions correctly.
    """
    users = db_store.find_by_field('users.json', 'email', email.lower().strip())
    if not users:
        return {'success': False, 'message': 'Email not found'}

    user = users[0]

    # Chain of Responsibility — verify answers
    chain = build_security_chain()
    if not chain.handle(user, answers):
        return {'success': False, 'message': 'Security question answer(s) incorrect'}

    if len(new_password) < 4:
        return {'success': False, 'message': 'Password must be at least 4 characters'}

    # All verified — update password
    new_hash = hash_password(new_password)
    db_store.update('users.json', user['id'], {'password_hash': new_hash})

    return {'success': True, 'message': 'Password reset successfully!'}


def get_user_by_id(user_id):
    """Look up a user by ID."""
    return db_store.find_by_id('users.json', user_id)
