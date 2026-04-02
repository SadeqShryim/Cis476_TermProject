# 🚗 DriveShare — Peer-to-Peer Car Rental Platform

**CIS 476 Term Project** — A terminal-based car rental platform inspired by [Turo.com](https://turo.com).

---

## ⚡ Quick Start

### Prerequisites

- **Python 3.10+** installed on your machine
- That's it — no external packages needed

### 1. Clone the repo

```bash
git clone https://github.com/SadeqShryim/Cis476_TermPoject.git
cd Cis476_TermPoject
```

### 2. Run the app

```bash
python main.py
```

### 3. Run the tests (108 automated tests)

```bash
python test_all.py
```

> **Note:** The test suite resets all data. If you've been using the app and want to keep your data, back up the `data/` folder first.

---

## 🧭 How to Use the App

When you run `python main.py`, you'll see the welcome screen:

```
============================================================
  🚗  DriveShare — Welcome
============================================================

  1. Login
  2. Register
  3. Forgot Password
  0. Exit
```

### Step-by-step walkthrough:

1. **Register** — Create an account with email, password, and 3 security questions
2. **Dashboard** — After registering you'll land on the main dashboard
3. **As an Owner** — List your car for rent (option 1), set price/availability
4. **As a Renter** — Search for cars (option 2), book one, or watch it for price drops
5. **Messages** — Send messages to other users (option 3)
6. **Payments** — Pay for bookings from the Bookings & Payments menu (option 5)

> 💡 **Tip:** Every user starts with a **$1,000 balance** for testing payments.

---

## 📁 Project Structure

```
Cis476_TermPoject/
├── main.py                     # Run this to start the app
├── test_all.py                 # Run this to test everything
├── requirements.txt            # No external dependencies needed
│
├── models/                     # Data models (User, Car, Booking, Message, Notification)
├── patterns/                   # All 6 design patterns (see below)
├── services/                   # Business logic layer
├── cli/                        # Terminal UI screens
├── storage/                    # JSON file persistence
└── data/                       # Auto-created at runtime — stores all app data
```

---

## 🎯 Design Patterns Implemented

| # | Pattern | File | What It Does |
|---|---------|------|--------------|
| 1 | **Singleton** | `patterns/singleton.py` | One session manager instance across the app |
| 2 | **Observer** | `patterns/observer.py` | Notifies watchers when car price/availability changes |
| 3 | **Builder** | `patterns/builder.py` | Step-by-step car listing creation |
| 4 | **Proxy** | `patterns/proxy.py` | Validates & logs payments before processing |
| 5 | **Chain of Responsibility** | `patterns/chain_of_responsibility.py` | 3-question password recovery chain |
| 6 | **Mediator** | `patterns/mediator.py` | Coordinates navigation between UI screens |

---

## ✅ Features

- **User Registration & Auth** — Email/password with SHA-256 hashing
- **3 Security Questions** — Set during registration, used for password recovery
- **Car Listings (Owner)** — Create, update price/availability, delete listings
- **Search & Book (Renter)** — Filter by location, date, price, make
- **Overlap Prevention** — Cannot double-book a car for overlapping dates
- **Watch Cars** — Get notified when a watched car's price drops
- **Messaging** — Direct messages between owners and renters
- **Simulated Payments** — Pay button updates balances and notifies both parties
- **Notifications** — In-app notifications for bookings, payments, messages, and watches

---

## 🗂️ Data Storage

All data is saved as JSON files in the `data/` folder (auto-created when you first run the app):

| File | Contents |
|------|----------|
| `users.json` | User accounts |
| `cars.json` | Car listings |
| `bookings.json` | Reservations |
| `messages.json` | User messages |
| `notifications.json` | Notifications |

> To start fresh, just delete the `data/` folder and run the app again.

---

## 🧪 Testing

Run the full test suite:

```bash
python test_all.py
```

This runs **108 automated tests** covering:
- Storage layer (CRUD)
- All 6 design patterns
- User registration, login, password recovery
- Car listing, search, booking, conflict detection
- Watch notifications (Observer pattern)
- Payment processing (Proxy pattern)
- Messaging
- Data persistence

Expected output:
```
RESULTS: 108 passed, 0 failed, 108 total
🎉 ALL TESTS PASSED!
```

---

## 🚀 What's Next (Phase 2)

Phase 2 will convert this into a **web application**:
- Add a **FastAPI** backend (wrapping the existing `services/` and `patterns/`)
- Build a **web front-end**
- Swap JSON storage for a **real database**

The terminal code (`cli/`) gets replaced — everything else stays the same.
