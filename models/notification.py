"""Notification model."""

import uuid
from datetime import datetime


def create_notification(user_id, content, notif_type='general'):
    """
    Create a new notification dict.
    """
    return {
        'id': str(uuid.uuid4()),
        'user_id': user_id,
        'content': content,
        'type': notif_type,
        'timestamp': datetime.now().isoformat(),
        'read': False
    }
