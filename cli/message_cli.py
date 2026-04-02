"""
CLI Message Screens — Inbox, conversations, send/receive messages.
"""

from cli.menus import print_header, pause
from patterns.singleton import SessionManager
from services import message_service
from storage import db_store


def message_menu():
    """Messaging main menu."""
    while True:
        print_header("Messages")
        print()
        print("  1. 📥 My Conversations")
        print("  2. ✉️  New Message")
        print("  0. ⬅  Back to Dashboard")
        print()

        choice = input("  Select an option: ").strip()

        if choice == '1':
            conversations_screen()
        elif choice == '2':
            new_message_screen()
        elif choice == '0':
            break
        else:
            print("\n  ❌ Invalid option.")
            pause()


def conversations_screen():
    """List all conversations with summary info."""
    session = SessionManager()
    user = session.get_current_user()

    print_header("My Conversations")
    convos = message_service.get_conversations(user['id'])

    if not convos:
        print("\n  No conversations yet. Start one from 'New Message'!")
        pause()
        return

    for i, c in enumerate(convos, 1):
        unread = f" 🔴 {c['unread_count']} new" if c['unread_count'] > 0 else ""
        last = c.get('last_message')
        preview = ""
        if last:
            who = "You" if last['sender_id'] == user['id'] else c['partner_email'].split('@')[0]
            preview = f"  {who}: {last['content'][:40]}{'...' if len(last['content']) > 40 else ''}"

        print(f"\n  [{i}] {c['partner_email']}{unread}")
        if preview:
            print(f"     {preview}")

    print()
    print("  Type a number to open conversation, or 0 to go back")
    print()

    choice = input("  Select: ").strip()

    if choice == '0':
        return

    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(convos):
            raise ValueError
        open_conversation(user['id'], convos[idx]['partner_id'],
                          convos[idx]['partner_email'])
    except ValueError:
        print("\n  ❌ Invalid selection.")
        pause()


def open_conversation(user_id, partner_id, partner_email):
    """View a conversation thread and send replies."""
    while True:
        print_header(f"Chat with {partner_email}")

        # Mark as read
        message_service.mark_conversation_read(user_id, partner_id)

        messages = message_service.get_conversation(user_id, partner_id)

        if not messages:
            print("\n  No messages in this conversation yet.")
        else:
            print()
            for m in messages[-20:]:  # Show last 20 messages
                if m['sender_id'] == user_id:
                    sender = "You"
                    arrow = ">>>"
                else:
                    sender = partner_email.split('@')[0]
                    arrow = "<<<"

                time_str = m['timestamp'][:16].replace('T', ' ')
                print(f"  {arrow} [{time_str}] {sender}:")
                print(f"      {m['content']}")
                print()

        print("-" * 60)
        print("  Type a message and press Enter, or 'q' to go back")
        print()

        text = input("  > ").strip()
        if text.lower() == 'q':
            break
        if text:
            result = message_service.send_message(user_id, partner_id, text)
            if not result['success']:
                print(f"\n  ❌ {result['message']}")
                pause()


def new_message_screen():
    """Send a message to any user by email address."""
    session = SessionManager()
    user = session.get_current_user()

    print_header("New Message")
    print()

    email = input("  Recipient email: ").strip()
    if not email:
        print("\n  ❌ Email cannot be empty.")
        pause()
        return

    # Find user by email
    recipients = db_store.find_by_field('users.json', 'email', email.lower().strip())
    if not recipients:
        print(f"\n  ❌ No user found with email: {email}")
        pause()
        return

    recipient = recipients[0]
    if recipient['id'] == user['id']:
        print("\n  ❌ You cannot message yourself.")
        pause()
        return

    print(f"  To: {recipient['email']}\n")
    content = input("  Message: ").strip()

    if not content:
        print("\n  ❌ Message cannot be empty.")
        pause()
        return

    result = message_service.send_message(user['id'], recipient['id'], content)
    print(f"\n  {'✅' if result['success'] else '❌'} {result['message']}")
    pause()
