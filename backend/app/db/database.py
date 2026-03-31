from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DATABASE_URL

# Create engine
engine = create_engine(DATABASE_URL)

# ✅ THIS IS WHAT YOU ARE MISSING OR WRONG
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()