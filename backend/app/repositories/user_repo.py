"""
User Repository

Handles database operations related to users.

Responsibilities:
- Fetching users by phone number (for authentication)
- Creating new users (registration flow)

Design Notes:
- Phone number acts as primary login identifier
- Default user role is 'patient'
"""

from sqlalchemy.orm import Session
from app.models.user import User


# ---------------------------------------------------------
# Fetch User by Phone Number
# ---------------------------------------------------------
def get_user_by_phone(db: Session, phone: str):
    """
    Retrieve a user by phone number.

    Args:
        db (Session): Database session
        phone (str): User's phone number

    Returns:
        User | None:
            - User object if found
            - None if no matching user exists

    Usage:
        - Used in login flow (OTP request & verification)
        - Used to check if user already exists during registration
    """

    return db.query(User).filter(User.phone_number == phone).first()


# ---------------------------------------------------------
# Create New User
# ---------------------------------------------------------
def create_user(db: Session, phone: str, email: str):
    """
    Create and persist a new user.

    Args:
        db (Session): Database session
        phone (str): User's phone number
        email (str): User's email address

    Returns:
        User: Newly created user object

    Notes:
        - Default role is set to 'patient'
        - Assumes uniqueness of phone and email is enforced at DB level
    """

    user = User(
        phone_number=phone,
        email=email,
        usertype="patient"  # Default role assignment
    )

    # Persist new user
    db.add(user)
    db.commit()
    db.refresh(user)

    return user