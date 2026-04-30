"""
Database Configuration Module

This module initializes:
- SQLAlchemy Engine (DB connection)
- Session factory (SessionLocal)
- Base class for ORM models

Usage:
- Import `SessionLocal` to create DB sessions
- Import `Base` to define ORM models
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DATABASE_URL


# ---------------------------------------------------------
# SQLAlchemy Engine
# ---------------------------------------------------------
# The engine is the core interface to the database.
# It manages:
# - Connection pooling
# - DB dialect (PostgreSQL, MySQL, etc.)
# - Execution of SQL statements
#
# DATABASE_URL example:
# postgresql://user:password@host:port/dbname
# ---------------------------------------------------------
engine = create_engine(DATABASE_URL)


# ---------------------------------------------------------
# Session Factory (SessionLocal)
# ---------------------------------------------------------
# This creates new database sessions for each request.
#
# Config:
# - autocommit=False → Changes must be committed manually
# - autoflush=False → Prevents automatic flush before queries
# - bind=engine     → Associates session with the DB engine
#
# Best Practice:
# - Use one session per request
# - Always close session after use (via dependency)
# ---------------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ---------------------------------------------------------
# Base ORM Class
# ---------------------------------------------------------
# All SQLAlchemy models should inherit from this Base.
#
# Example:
# class User(Base):
#     __tablename__ = "users"
#
# Purpose:
# - Maintains model metadata
# - Used for table creation (Base.metadata.create_all)
# ---------------------------------------------------------
Base = declarative_base()