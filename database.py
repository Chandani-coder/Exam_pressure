import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Safety check (prevents crash like yours)
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Check your environment variables.")

# Fix for Render / older postgres URLs
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"sslmode": "require"}
)

# Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base
Base = declarative_base()
