"""
CLI Menus — Main menu, dashboard, navigation, and notifications.
Uses the Mediator pattern to coordinate between screens.
"""

import os
from patterns.singleton import SessionManager
from patterns.mediator import UIMediator
from services import notification_service
from services.auth_service import logout, get_user_by_id

# ─── Global mediator instance ───────────────────────────────────────────
mediator = UIMediator()


# ─── Helpers ─────────────────────────────────────────────────────────────

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    """Print a styled header bar."""
    clear_screen()
    print("=" * 60)
    print(f"  🚗  DriveShare — {title}")
    print("=" * 60)


def print_notification_badge():
    """Show unread notification count if the user is logged in."""
    session = SessionManager()
    if session.is_authenticated():
        count = notification_service.get_unread_count(
            session.get_current_user()['id']
        )
        if count > 0:
            print(f"  🔔 You have {count} unread notification(s)")
            print("-" * 60)


def pause(message="  Press Enter to continue..."):
    """Pause and wait for user input."""
    input(message)


# ─── Welcome Screen (Not Logged In) ────────────────────────────────────

def welcome_menu():
    """Entry point — shown when no user is logged in."""
    while True:
        print_header("Welcome")
        print()
        print("  1. Login")
        print("  2. Register")
        print("  3. Forgot Password")
        print("  0. Exit")
        print()

        choice = input("  Select an option: ").strip()

        if choice == '1':
            from cli.auth_cli import login_screen
            if login_screen():
                main_dashboard()
        elif choice == '2':
            from cli.auth_cli import register_screen
            if register_screen():
                main_dashboard()
        elif choice == '3':
            from cli.auth_cli import recover_password_screen
            recover_password_screen()
        elif choice == '0':
            print("\n  Goodbye! 👋")
            break
        else:
            print("\n  ❌ Invalid option.")
            pause()


# ─── Main Dashboard (Logged In) ────────────────────────────────────────

def main_dashboard():
    """Main dashboard — hub for all features."""
    session = SessionManager()

    while True:
        if not session.is_authenticated():
            break

        # Refresh user data (picks up balance changes, etc.)
        session.refresh()
        user = session.get_current_user()

        print_header("Dashboard")
        print_notification_badge()
        print(f"\n  Logged in as: {user['email']}")
        print(f"  Balance: ${user['balance']:.2f}")
        print()
        print("  1. 🚘  Owner — Manage My Cars")
        print("  2. 🔍  Renter — Search & Book Cars")
        print("  3. 💬  Messages")
        print("  4. 🔔  Notifications")
        print("  5. 💰  My Bookings & Payments")
        print("  6. 👤  Account Info")
        print("  0. Logout")
        print()

        choice = input("  Select an option: ").strip()

        if choice == '1':
            mediator.notify('main', 'navigate_owner_menu')
            from cli.owner_cli import owner_menu
            owner_menu()
        elif choice == '2':
            mediator.notify('main', 'navigate_renter_menu')
            from cli.renter_cli import renter_menu
            renter_menu()
        elif choice == '3':
            mediator.notify('main', 'navigate_messages')
            from cli.message_cli import message_menu
            message_menu()
        elif choice == '4':
            notifications_screen()
        elif choice == '5':
            mediator.notify('main', 'navigate_payment')
            from cli.payment_cli import bookings_and_payments_menu
            bookings_and_payments_menu()
        elif choice == '6':
            account_info_screen()
        elif choice == '0':
            logout()
            print("\n  ✅ Logged out successfully.")
            pause()
            break
        else:
            print("\n  ❌ Invalid option.")
            pause()


# ─── Notifications Screen ──────────────────────────────────────────────

def notifications_screen():
    """View and manage notifications."""
    session = SessionManager()
    user = session.get_current_user()

    while True:
        print_header("Notifications")
        notifs = notification_service.get_notifications(user['id'])

        if not notifs:
            print("\n  No notifications yet.")
        else:
            for i, n in enumerate(notifs, 1):
                status = "  " if n.get('read') else "🔴"
                type_tag = n.get('type', 'general').upper()
                print(f"  {status} [{type_tag}] {n['content']}")
                print(f"      {n['timestamp'][:16].replace('T', ' ')}")
                if i < len(notifs):
                    print()

        print()
        print("  1. Mark all as read")
        print("  0. Back")
        print()

        choice = input("  Select an option: ").strip()
        if choice == '1':
            notification_service.mark_all_read(user['id'])
            print("\n  ✅ All notifications marked as read.")
            pause()
        elif choice == '0':
            break
        else:
            print("\n  ❌ Invalid option.")
            pause()


# ─── Account Info Screen ───────────────────────────────────────────────

def account_info_screen():
    """Display current user's account details."""
    session = SessionManager()
    session.refresh()
    user = session.get_current_user()

    print_header("Account Info")
    print(f"\n  📧 Email:    {user['email']}")
    print(f"  💰 Balance:  ${user['balance']:.2f}")
    print(f"  🆔 User ID:  {user['id'][:8]}...")
    print(f"  📅 Joined:   {user['created_at'][:10]}")
    print()
    pause()
