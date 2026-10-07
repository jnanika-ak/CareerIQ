"""
CareerIQ Database Session & Configuration Module
Step 10: PostgreSQL connection setup with SQLAlchemy 2.x and psycopg3.
"""

import os
from pathlib import Path
from typing import Generator, Optional, Tuple

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# 1. Load environment variables from .env file
# Try loading from backend directory specifically as well as parent directory
backend_dir = Path(__file__).resolve().parent.parent.parent
env_file = backend_dir / ".env"
if env_file.exists():
    load_dotenv(dotenv_path=env_file)
else:
    load_dotenv()

# Expected format: postgresql+psycopg://postgres:PASSWORD@localhost:5432/careeriq
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres@localhost:5432/careeriq"
)

# 2. Configure SQLAlchemy 2.x Engine
# pool_pre_ping checks the connection before handing it out to prevent stale connection errors
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)

# 3. Create SessionLocal session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# 4. Declarative Base using SQLAlchemy 2.x DeclarativeBase
class Base(DeclarativeBase):
    pass


# 5. FastAPI database session dependency
def get_db() -> Generator:
    """
    Yields an active database session for a request and guarantees cleanup.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 6. Database Health Check Utility
def check_database_connection() -> Tuple[bool, str]:
    """
    Executes a lightweight query (SELECT 1) to verify database connectivity.
    Returns (True, "connected") on success, or (False, error_detail) on failure.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True, "connected"
    except Exception as exc:
        return False, str(exc)


# 7. Safe Table Initialization Utility
def init_db() -> Tuple[bool, str]:
    """
    Creates any missing tables defined in Base.metadata.
    Guarantees:
    - Never drops existing tables
    - Never deletes existing records
    - Does not crash if the database is currently unreachable
    """
    try:
        # Import models here to ensure they are registered with Base.metadata
        from app.db import models  # noqa: F401

        Base.metadata.create_all(bind=engine)
        return True, "Database tables initialized successfully"
    except Exception as exc:
        return False, f"Database table initialization failed: {str(exc)}"
