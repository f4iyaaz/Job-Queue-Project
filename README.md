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