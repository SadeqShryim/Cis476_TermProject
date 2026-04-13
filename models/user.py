"""User model — registration, password hashing, security questions."""

import uuid
import hashlib
from datetime import datetime


def create_user(email, password, security_questions):
    """
    Create a new user dict.
    """
    return {
        'id': str(uuid.uuid4()),
        'email': email.lower().strip(),
        'password_hash': hash_password(password),
        'security_questions': [
            {'question': sq['question'], 'answer': sq['answer'].lower().strip()}
            for sq in security_questions
        ],
        'balance': 1000.00,  # Starting balance for demo
        'created_at': datetime.now().isoformat()
    }


def hash_password(password):
    """Hash a password with SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, password_hash):
    """Verify a plain-text password against a stored hash."""
    return hash_password(password) == password_hash
