from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DATABASE_URL


# ---------------------------------------------------------
# Create SQLAlchemy engine
# This manages the connection to the database
# ---------------------------------------------------------
engine = create_engine(DATABASE_URL)


# ---------------------------------------------------------
# Create SessionLocal class
# This will be used to create DB sessions per request
#
# autocommit=False → changes require explicit commit
# autoflush=False → prevents automatic flush to DB
# bind=engine      → binds session to DB engine
# ---------------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ---------------------------------------------------------
# Base class for all ORM models
# All database models should inherit from this
# ---------------------------------------------------------
Base = declarative_base()