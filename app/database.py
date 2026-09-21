from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine (connection to PostgreSQL)
engine = create_engine(DATABASE_URL)

# Create all tables defined in models.py
Base.metadata.create_all(bind=engine)

# SessionLocal is used to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)