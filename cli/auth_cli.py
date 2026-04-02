"""
CLI Auth Screens — Register, Login, and Password Recovery.

Uses:
  - Singleton pattern (SessionManager) for session management
  - Chain of Responsibility pattern for password recovery
"""

from cli.menus import print_header, pause
from services import auth_service


def register_screen():
    """Registration screen — collects email, password, and 3 security questions."""
    print_header("Register")
    print()

    email = input("  Email: ").strip()
    if not email:
        print("\n  ❌ Email cannot be empty.")
        pause()
        return False

    password = input("  Password (min 4 chars): ").strip()
    confirm = input("  Confirm Password: ").strip()

    if password != confirm:
        print("\n  ❌ Passwords do not match.")
        pause()
        return False

    print("\n  Set up 3 security questions for password recovery:\n")

    security_questions = []
    default_questions = [
        "What is your pet's name?",
        "What city were you born in?",
        "What is your favorite movie?"
    ]

    for i in range(3):
        print(f"  --- Question {i + 1} ---")
        print(f"  Default: {default_questions[i]}")
        custom = input("  Custom question (or press Enter for default): ").strip()
        question = custom if custom else default_questions[i]
        answer = input(f"  Answer: ").strip()

        if not answer:
            print("\n  ❌ Answer cannot be empty.")
            pause()
            return False

        security_questions.append({'question': question, 'answer': answer})
        print()

    result = auth_service.register(email, password, security_questions)
    print(f"\n  {'✅' if result['success'] else '❌'} {result['message']}")
    pause()
    return result['success']


def login_screen():
    """Login screen — email and password authentication."""
    print_header("Login")
    print()

    email = input("  Email: ").strip()
    password = input("  Password: ").strip()

    result = auth_service.login(email, password)
    print(f"\n  {'✅' if result['success'] else '❌'} {result['message']}")
    pause()
    return result['success']


def recover_password_screen():
    """
    Password recovery screen.
    Uses Chain of Responsibility to verify 3 security questions.
    """
    print_header("Forgot Password")
    print()

    email = input("  Enter your email: ").strip()

    questions = auth_service.get_security_questions(email)
    if not questions:
        print("\n  ❌ Email not found.")
        pause()
        return

    print("\n  Answer your 3 security questions:\n")
    answers = []
    for i, question in enumerate(questions, 1):
        answer = input(f"  Q{i}: {question}\n  A{i}: ").strip()
        answers.append(answer)
        print()

    new_password = input("  New Password (min 4 chars): ").strip()
    confirm = input("  Confirm New Password: ").strip()

    if new_password != confirm:
        print("\n  ❌ Passwords do not match.")
        pause()
        return

    result = auth_service.recover_password(email, answers, new_password)
    print(f"\n  {'✅' if result['success'] else '❌'} {result['message']}")
    pause()
