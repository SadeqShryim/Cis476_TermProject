"""Notification service — in-app notification delivery."""

from storage import db_store
from models.notification import create_notification


def add_notification(user_id, content, notif_type='general'):
    """Create and store a notification."""
    notif = create_notification(user_id, content, notif_type)
    db_store.add('notifications.json', notif)
    return notif


def get_notifications(user_id, unread_only=False):
    """Get all notifications for a user, newest first."""
    notifs = db_store.find_by_field('notifications.json', 'user_id', user_id)
    if unread_only:
        notifs = [n for n in notifs if not n.get('read', False)]
    notifs.sort(key=lambda n: n['timestamp'], reverse=True)
    return notifs


def mark_read(notification_id):
    """Mark a single notification as read."""
    db_store.update('notifications.json', notification_id, {'read': True})


def mark_all_read(user_id):
    """Mark all notifications for a user as read."""
    notifs = get_notifications(user_id, unread_only=True)
    for n in notifs:
        mark_read(n['id'])


def get_unread_count(user_id):
    """Return the count of unread notifications."""
    return len(get_notifications(user_id, unread_only=True))
