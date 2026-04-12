"""Message service — send/receive messages between users."""

from storage import db_store
from models.message import create_message
from models.notification import create_notification


def send_message(sender_id, receiver_id, content):
    """Send a message from one user to another."""
    if sender_id == receiver_id:
        return {'success': False, 'message': 'Cannot send a message to yourself'}

    receiver = db_store.find_by_id('users.json', receiver_id)
    if not receiver:
        return {'success': False, 'message': 'Recipient not found'}

    if not content.strip():
        return {'success': False, 'message': 'Message cannot be empty'}

    msg = create_message(sender_id, receiver_id, content.strip())
    db_store.add('messages.json', msg)

    # Notify recipient
    sender = db_store.find_by_id('users.json', sender_id)
    sender_email = sender['email'] if sender else 'Unknown'
    preview = content[:50] + ('...' if len(content) > 50 else '')
    notif = create_notification(
        receiver_id,
        f"New message from {sender_email}: {preview}",
        'message'
    )
    db_store.add('notifications.json', notif)

    return {'success': True, 'message': 'Message sent!', 'msg': msg}


def get_conversation(user1_id, user2_id):
    """Get all messages between two users, sorted chronologically."""
    messages = db_store.load_all('messages.json')
    convo = [
        m for m in messages
        if (m['sender_id'] == user1_id and m['receiver_id'] == user2_id)
        or (m['sender_id'] == user2_id and m['receiver_id'] == user1_id)
    ]
    convo.sort(key=lambda m: m['timestamp'])
    return convo


def get_conversations(user_id):
    """Get a list of conversation summaries (one per unique partner)."""
    messages = db_store.load_all('messages.json')
    partners = set()
    for m in messages:
        if m['sender_id'] == user_id:
            partners.add(m['receiver_id'])
        elif m['receiver_id'] == user_id:
            partners.add(m['sender_id'])

    result = []
    for partner_id in partners:
        partner = db_store.find_by_id('users.json', partner_id)
        convo = get_conversation(user_id, partner_id)
        last_msg = convo[-1] if convo else None
        unread = sum(
            1 for m in convo
            if m['receiver_id'] == user_id and not m.get('read', False)
        )
        result.append({
            'partner_id': partner_id,
            'partner_email': partner['email'] if partner else 'Unknown',
            'last_message': last_msg,
            'unread_count': unread
        })

    # Sort by most recent message
    result.sort(
        key=lambda c: c['last_message']['timestamp'] if c['last_message'] else '',
        reverse=True
    )
    return result


def mark_conversation_read(user_id, partner_id):
    """Mark all messages from partner to user as read."""
    messages = db_store.load_all('messages.json')
    changed = False
    for m in messages:
        if (m['receiver_id'] == user_id and m['sender_id'] == partner_id
                and not m.get('read', False)):
            m['read'] = True
            changed = True
    if changed:
        db_store.save_all('messages.json', messages)
