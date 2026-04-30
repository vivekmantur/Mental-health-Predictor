"""
User Model

Represents an application user.

This model is used for:
- Authentication (via phone + OTP)
- Role-based access control (patient / doctor)
- Linking users to assessments
"""

from sqlalchemy import Column, Integer, String
from app.db.database import Base


class User(Base):
    """
    SQLAlchemy model for users.

    Each user can:
    - Submit PHQ-9 assessments (as a patient)
    - Review assessments (if usertype = doctor)
    """

    __tablename__ = "users"

    # ---------------------------------------------------------
    # Primary Identifier
    # ---------------------------------------------------------
    user_id = Column(Integer, primary_key=True, index=True)
    # Unique ID for each user (used across the system)

    # ---------------------------------------------------------
    # Authentication Fields
    # ---------------------------------------------------------
    phone_number = Column(String, unique=True, index=True)
    # Used for OTP-based login (primary identifier)

    email = Column(String, unique=True, index=True)
    # Used for OTP delivery and communication

    # ---------------------------------------------------------
    # Role / Authorization
    # ---------------------------------------------------------
    usertype = Column(String, default="patient")
    # Defines user role
    # Possible values:
    # - "patient" → can submit assessments
    # - "doctor"  → can review and manage assessments