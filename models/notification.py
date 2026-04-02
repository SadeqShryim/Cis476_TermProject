"""Notification model."""

import uuid
from datetime import datetime


def create_notification(user_id, content, notif_type='general'):
    """
    Create a new notification dict.
    
    Args:
        user_id: ID of the user to notify
        content: Notification message
        notif_type: Type of notification (general, booking, payment, watch, message)
    """
    return {
        'id': str(uuid.uuid4()),
        'user_id': user_id,
        'content': content,
        'type': notif_type,
        'timestamp': datetime.now().isoformat(),
        'read': False
    }
