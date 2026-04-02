"""
DriveShare — Peer-to-Peer Car Rental Platform
CIS 476 Term Project

Entry point for the terminal (CLI) application.
Run with: python main.py
"""

import sys
import os

# Ensure the project root is on the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    """Initialize subsystems and launch the welcome menu."""
    # Restore any persisted watchers into the in-memory WatchManager
    from services.watch_service import restore_watchers
    restore_watchers()

    # Launch the CLI
    from cli.menus import welcome_menu
    welcome_menu()


if __name__ == '__main__':
    main()
