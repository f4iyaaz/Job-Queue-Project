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

````
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

````

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


Replace `password` with your PostgreSQL password.

### Run Locally

**Terminal 1 - Start API:**

```bash
uvicorn app.main:app --reload
```

Visit: http://localhost:8000/docs (interactive API docs)

**Terminal 2 - Start Worker:**

```bash
python worker.py
```

You should see: `[Worker] Started. Waiting for jobs...`

---

## API Endpoints

### Create a Job

```bash
curl -X POST http://localhost:8000/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "type": "send_email",
    "payload": {"to": "user@example.com", "subject": "Hello"}
  }'
```

Response:

```json
{
  "id": "abc-123-xyz",
  "type": "send_email",
  "status": "queued",
  "created_at": "2024-01-15T10:30:00",
  "payload": {"to": "user@example.com", "subject": "Hello"},
  "result": null,
  "error": null
}
```

### Get Job Status

```bash
curl http://localhost:8000/jobs/abc-123-xyz
```

### List All Jobs

```bash
curl http://localhost:8000/jobs
```

### Get Statistics

```bash
curl http://localhost:8000/stats
```

---

## How It Works

1. **User creates job via API**
   - Job validated and saved in PostgreSQL
   - Job added to Redis queue
   - API returns job ID immediately

2. **Worker pulls job from queue**
   - Updates job status to "processing"

3. **Worker processes the job**
   - Executes the work (send email, resize image, etc.)
   - Updates job status to "completed"
   - Stores the result

4. **User checks job status**
   - Queries API for current status
   - Gets result when completed

---

## Supported Job Types

**send_email** - Simulates sending an email (2 second delay)

```json
{
  "type": "send_email",
  "payload": {
    "to": "user@example.com",
    "subject": "Hello World"
  }
}
```

**resize_image** - Simulates resizing an image (3 second delay)

```json
{
  "type": "resize_image",
  "payload": {
    "image_path": "/path/to/image.jpg"
  }
}
```

---

## Job Status

- **queued** - Waiting to be processed
- **processing** - Currently being processed by worker
- **completed** - Finished successfully with result
- **failed** - Failed with error message

---

## Testing

### Using Swagger UI (Easiest)

1. Start the API: `uvicorn app.main:app --reload`
2. Open browser: http://localhost:8000/docs
3. Try endpoints interactively

### Using curl (Command Line)

Create a job, copy the job ID, then check its status:

```bash
# Create job
JOB_ID=$(curl -s -X POST http://localhost:8000/jobs \
  -H "Content-Type: application/json" \
  -d '{"type": "send_email", "payload": {"to": "test@example.com"}}' | jq -r '.id')

# Wait a moment
sleep 3

# Check status
curl http://localhost:8000/jobs/$JOB_ID
```

---

## Key Concepts

**Why separate API and Worker?**

- API needs to respond fast (free up the request)
- Worker can take time to process in background
- Both can scale independently

**Why Redis queue?**

- Fast in-memory operations
- FIFO (first in, first out) for fair job processing
- Prevents jobs from being processed twice

**Why PostgreSQL?**

- Permanent storage (survives crashes)
- Query job history
- Track job lifecycle

---

## What I Learned
```
✅ Asynchronous job processing patterns
✅ Message queue architecture
✅ Decoupling API from long-running tasks
✅ Scalable system design
✅ Database job tracking
```
---

## Future Enhancements

- Retry logic with exponential backoff
- Dead letter queue for failed jobs
- Job priority levels
- Webhook notifications
- Job scheduling
- Better logging and monitoring
- Unit tests

---

