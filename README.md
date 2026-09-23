# Job Queue System

A backend system for processing asynchronous jobs using FastAPI, PostgreSQL, and Redis.

## What It Does

Users submit jobs (like sending emails or resizing images). The API instantly returns a job ID. Worker processes handle jobs in the background while the user continues using the app.

**Without queue:** User waits 5 seconds for their email to send.
**With queue:** User gets response instantly. Email sends in background.

---

## Tech Stack

- **FastAPI** - Python web framework
- **PostgreSQL** - Database (stores jobs)
- **Redis** - Message queue (holds pending jobs)
- **SQLAlchemy** - ORM for database queries

---

## Project Structure
job-queue-project/
├── app/
│ ├── main.py # API endpoints
│ ├── models.py # Database Job model
│ ├── schemas.py # Request/response formats
│ ├── database.py # Database connection
│ └── init.py
├── worker.py # Background job processor
├── requirements.txt # Dependencies
├── .env # Environment variables (local)
├── .gitignore
└── README.md


---

## Local Setup

### Prerequisites

- Python 3.9+
- PostgreSQL
- Redis (or Docker)

### Installation

1. Clone and setup:

```bash
git clone <your-repo>
cd job-queue-project
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Create PostgreSQL database:

```bash
psql -U postgres
CREATE DATABASE job_queue;
\q
```

3. Start Redis (with Docker):

```bash
docker run -d -p 6379:6379 redis
```

4. Create `.env` file: