from sqlalchemy import Column, String, Integer, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

# This is required by SQLAlchemy. All our models inherit from Base
Base = declarative_base()

# Define status as an enum (only these 4 values allowed)
class JobStatus(str, enum.Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

# Define the Job table
class Job(Base):
    __tablename__ = "jobs"  # This is the table name in PostgreSQL
    
    # Define columns
    id = Column(String, primary_key=True)  # Unique identifier
    type = Column(String)  # "send_email", "resize_image", etc
    payload = Column(JSON)  # The data: {"to": "...", "subject": "..."}
    status = Column(SQLEnum(JobStatus), default=JobStatus.QUEUED)  # Current state
    result = Column(JSON, nullable=True)  # Output after completion (can be empty)
    error = Column(String, nullable=True)  # Error message if failed (can be empty)
    created_at = Column(DateTime, default=datetime.utcnow)  # When job was created
    started_at = Column(DateTime, nullable=True)  # When worker started (can be empty)
    completed_at = Column(DateTime, nullable=True)  # When job finished (can be empty)
    retry_count = Column(Integer, default=0)  # How many times we tried
    max_retries = Column(Integer, default=3)  # Give up after this many tries