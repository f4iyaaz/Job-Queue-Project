from fastapi import FastAPI
from sqlalchemy.orm import Session
import uuid
import redis
import json
from datetime import datetime
from .database import SessionLocal, engine
from .models import Job, JobStatus, Base
from .schemas import JobCreate, JobResponse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(title="Job Queue API")

# Connect to Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# Create all tables
Base.metadata.create_all(bind=engine)


# ENDPOINT 1: Create Job
@app.post("/jobs", response_model=JobResponse)
def create_job(job_data: JobCreate):
    """Create a new job and add it to the queue"""
    db = SessionLocal()
    
    try:
        job_id = str(uuid.uuid4())
        
        db_job = Job(
            id=job_id,
            type=job_data.type,
            payload=job_data.payload,
            status=JobStatus.QUEUED
        )
        
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        
        queue_data = {
            "id": job_id,
            "type": job_data.type,
            "payload": job_data.payload
        }
        redis_client.rpush("job_queue", json.dumps(queue_data))
        
        return db_job
        
    finally:
        db.close()


# ENDPOINT 2: Get Job Status
@app.get("/jobs/{job_id}", response_model=JobResponse)
def get_job_status(job_id: str):
    """Get status of a specific job"""
    db = SessionLocal()
    
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        
        if not job:
            return {"error": "Job not found"}
        
        return job
        
    finally:
        db.close()


# ENDPOINT 3: List All Jobs
@app.get("/jobs", response_model=list[JobResponse])
def list_jobs():
    """List all jobs"""
    db = SessionLocal()
    
    try:
        jobs = db.query(Job).all()
        return jobs
        
    finally:
        db.close()


# ENDPOINT 4: Get Statistics
@app.get("/stats")
def get_stats():
    """Get queue statistics"""
    db = SessionLocal()
    
    try:
        queued = db.query(Job).filter(Job.status == JobStatus.QUEUED).count()
        processing = db.query(Job).filter(Job.status == JobStatus.PROCESSING).count()
        completed = db.query(Job).filter(Job.status == JobStatus.COMPLETED).count()
        failed = db.query(Job).filter(Job.status == JobStatus.FAILED).count()
        
        queue_size = redis_client.llen("job_queue")
        
        return {
            "queued": queued,
            "processing": processing,
            "completed": completed,
            "failed": failed,
            "queue_size": queue_size
        }
        
    finally:
        db.close()