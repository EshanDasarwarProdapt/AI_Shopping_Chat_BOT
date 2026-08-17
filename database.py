"""
Database configuration and session utilities for DemoShop.

This module sets up the SQLAlchemy engine for the SQLite database, provides a
session factory, and defines helper functions for initializing the schema and
getting a session generator usable as a FastAPI dependency.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# SQLite URL; the database file resides in the project root.
SQLALCHEMY_DATABASE_URL = "sqlite:///./demo_shop.db"

# Create the engine with `check_same_thread` disabled for compatibility with
# FastAPI's async context.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory used throughout the app. `autocommit=False` and
# `autoflush=False` give explicit transaction control.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Create all tables defined in the ORM models.

    This should be called once at application startup to ensure the database
    schema exists before any queries are executed.
    """
    Base.metadata.create_all(bind=engine)


def get_db():
    """Yield a SQLAlchemy session for FastAPI route dependencies.

    The function is a generator that yields a session instance and guarantees
    that the session is closed after the request is processed, even if an
    exception occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
