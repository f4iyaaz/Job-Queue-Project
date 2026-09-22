import redis
import json
import time
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import Job, JobStatus
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env
load_dotenv()

# Get database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Create database connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Get Redis URL from .env (default to localhost if not set)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Connect to Redis
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def process_job(job_data):
    """
    Actually do the work here.
    Different job types need different processing.
    
    Args:
        job_data: Dictionary with 'type' and 'payload' keys
        
    Returns:
        result: Dictionary with the output/result of the job
        
    Raises:
        Exception: If job type is unknown
    """
    job_type = job_data.get("type")
    payload = job_data.get("payload")
    
    if job_type == "send_email":
        # Handle email jobs
        to = payload.get("to")
        subject = payload.get("subject", "No subject")
        print(f"[Worker] Sending email to {to}: {subject}")
        time.sleep(2)  # Simulate 2 seconds of work
        return {
            "email_sent": True,
            "to": to,
            "subject": subject
        }
    
    elif job_type == "resize_image":
        # Handle image resize jobs
        image_path = payload.get("image_path")
        print(f"[Worker] Resizing image: {image_path}")
        time.sleep(3)  # Simulate 3 seconds of work
        return {
            "image_resized": True,
            "path": image_path,
            "size": "thumbnail"
        }
    
    else:
        # Unknown job type
        raise Exception(f"Unknown job type: {job_type}")

def worker():
    """
    Main worker loop.
    Continuously pulls jobs from Redis queue and processes them.
    """
    print("[Worker] Started. Waiting for jobs...")
    
    while True:
        # Step 1: Pull next job from queue
        job_json = redis_client.lpop("job_queue")
        
        if job_json:
            # Job found! Let's process it
            job_data = json.loads(job_json)
            job_id = job_data["id"]
            
            # Create database session
            db = SessionLocal()
            
            try:
                # Step 2: Update job status to PROCESSING
                print(f"[Worker] Processing job {job_id}...")
                job = db.query(Job).filter(Job.id == job_id).first()
                
                if job:
                    job.status = JobStatus.PROCESSING
                    job.started_at = datetime.utcnow()
                    db.commit()
                    
                    # Step 3: Do the actual work
                    result = process_job(job_data)
                    
                    # Step 4: Update job status to COMPLETED
                    job.status = JobStatus.COMPLETED
                    job.completed_at = datetime.utcnow()
                    job.result = result
                    db.commit()
                    
                    print(f"[Worker] Job {job_id} completed successfully")
                
            except Exception as e:
                # Step 5: Handle errors
                print(f"[Worker] Job {job_id} failed: {str(e)}")
                job.status = JobStatus.FAILED
                job.error = str(e)
                job.completed_at = datetime.utcnow()
                db.commit()
            
            finally:
                # Always close the database session
                db.close()
        
        else:
            # No job in queue, wait and check again
            time.sleep(1)

if __name__ == "__main__":
    worker()