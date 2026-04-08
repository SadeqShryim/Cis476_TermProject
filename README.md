# DriveShare — Peer-to-Peer Car Rental Platform

**CIS 476 Term Project** — A full-stack car rental web application inspired by [Turo.com](https://turo.com).

- **Backend:** Python / FastAPI / SQLAlchemy / SQLite
- **Frontend:** React / Vite / Tailwind CSS

---

## Prerequisites

### Mac

1. **Python 3.10+**
   - Check with: `python3 --version`
   - Install via [Homebrew](https://brew.sh): `brew install python`
   - Or download from [python.org](https://www.python.org/downloads/)

2. **Node.js 18+** (includes npm)
   - Check with: `node --version`
   - Install via Homebrew: `brew install node`
   - Or download from [nodejs.org](https://nodejs.org/)

3. **Git**
   - Usually pre-installed on Mac. Check with: `git --version`
   - If missing: `brew install git`

### Windows

1. **Python 3.10+**
   - Check with: `python --version`
   - Download from [python.org](https://www.python.org/downloads/)
   - **Important:** During installation, check "Add Python to PATH"

2. **Node.js 18+** (includes npm)
   - Check with: `node --version`
   - Download the LTS installer from [nodejs.org](https://nodejs.org/)

3. **Git**
   - Check with: `git --version`
   - Download from [git-scm.com](https://git-scm.com/downloads)

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/SadeqShryim/Cis476_TermPoject.git
cd Cis476_TermPoject
```

### 2. Set up the backend

Create a virtual environment and install dependencies:

**Mac / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows (Command Prompt):**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Windows (PowerShell):**
```bash
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Start the backend server:

```bash
python main.py
```

The API will be running at **http://localhost:8000**. You can view the interactive API docs at **http://localhost:8000/docs**.

### 3. Set up the frontend

Open a **new terminal** window (keep the backend running), then:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be running at **http://localhost:5173** (default Vite port).

> The frontend proxies all `/api` requests to the backend at `localhost:8000`, so both servers must be running at the same time.

---

## Project Structure

```
Cis476_TermPoject/
├── main.py                 # Backend entry point (FastAPI + Uvicorn)
├── requirements.txt        # Python dependencies
├── api/                    # API route handlers
│   └── routes/             # auth, cars, bookings, user, payments, reviews
├── models/                 # Data models
├── services/               # Business logic layer
├── patterns/               # Design pattern implementations
├── storage/                # Database layer (SQLAlchemy + SQLite)
├── data/                   # Auto-created at runtime (holds driveshare.db)
│
├── frontend/               # React frontend
│   ├── package.json        # Node dependencies
│   ├── vite.config.js      # Vite config (includes API proxy)
│   └── src/
│       ├── pages/          # Page components
│       ├── components/     # Reusable UI components
│       ├── context/        # React context providers
│       ├── hooks/          # Custom React hooks
│       └── api/            # API client functions
│
└── diagrams/               # UML and architecture diagrams
```

---

## API Endpoints

The backend exposes the following route groups:

| Prefix           | Description              |
|------------------|--------------------------|
| `/api/auth`      | Registration and login   |
| `/api/cars`      | Car listings (CRUD)      |
| `/api/bookings`  | Booking management       |
| `/api/user`      | User profile and balance |
| `/api/payments`  | Payment processing       |
| `/api/reviews`   | Reviews and ratings      |

Full interactive documentation is available at `/docs` when the backend is running.

---

## Design Patterns

| Pattern                  | File                                  | Purpose                                        |
|--------------------------|---------------------------------------|-------------------------------------------------|
| Singleton                | `patterns/singleton.py`               | Single session manager instance across the app  |
| Observer                 | `patterns/observer.py`                | Notifies watchers on car price/availability changes |
| Builder                  | `patterns/builder.py`                 | Step-by-step car listing creation               |
| Proxy                    | `patterns/proxy.py`                   | Validates and logs payments before processing   |
| Chain of Responsibility  | `patterns/chain_of_responsibility.py` | Multi-question password recovery chain          |
| Mediator                 | `patterns/mediator.py`                | Coordinates navigation between UI screens       |

---

## Troubleshooting

- **Port already in use:** If port 8000 or 5173 is taken, kill the process using that port or change it. For the backend, edit `main.py`; for the frontend, Vite will automatically try the next available port.
- **`pip` not found:** Use `pip3` instead of `pip` on Mac/Linux.
- **`python` not found on Mac:** Use `python3` instead of `python`.
- **PowerShell execution policy error on Windows:** Run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` then try activating the venv again.
- **Database issues:** Delete the `data/` folder and restart the backend to reset the database from scratch.
