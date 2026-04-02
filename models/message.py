"""Message model."""

import uuid
from datetime import datetime


def create_message(sender_id, receiver_id, content):
    """
    Create a new message dict.
    
    Args:
        sender_id: ID of the message sender
        receiver_id: ID of the message recipient
        content: Message text
    """
    return {
        'id': str(uuid.uuid4()),
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'content': content,
        'timestamp': datetime.now().isoformat(),
        'read': False
    }
