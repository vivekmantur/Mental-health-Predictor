"""
Authentication Router

This module handles OTP-based authentication workflows including:
- Login via OTP
- User registration via OTP
- JWT token issuance after successful verification

Design Notes:
- OTP is generated securely and stored temporarily.
- Email is used as the delivery mechanism for OTP.
- JWT token is issued after successful OTP verification.
"""

import os
import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.db.database import SessionLocal
from app.repositories.user_repo import get_user_by_phone, create_user
from app.auth.jwt_handler import create_access_token
from app.auth.otp_store import store_otp, verify_otp
from app.auth.otp_sender import send_otp_email


# FastAPI router instance for authentication endpoints
router = APIRouter()


# ==============================
# Database Dependency
# ==============================

def get_db():
    """
    Dependency to provide a database session.

    Yields:
        Session: SQLAlchemy database session

    Ensures:
        - Proper session lifecycle management
        - Session is always closed after request completion
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==============================
# Request Schemas
# ==============================

class PhoneRequest(BaseModel):
    """
    Schema for requesting OTP during login.

    Attributes:
        phone (str): User's registered phone number
    """
    phone: str


class RegisterRequest(BaseModel):
    """
    Schema for requesting OTP during registration.

    Attributes:
        phone (str): User's phone number
        email (EmailStr): User's email address for OTP delivery
    """
    phone: str
    email: EmailStr


class OTPVerifyRequest(BaseModel):
    """
    Schema for verifying OTP during login.

    Attributes:
        phone (str): User's phone number
        otp (str): One-Time Password received by user
    """
    phone: str
    otp: str


class RegisterVerifyRequest(BaseModel):
    """
    Schema for verifying OTP during registration.

    Attributes:
        phone (str): User's phone number
        email (EmailStr): User's email address
        otp (str): One-Time Password received by user
    """
    phone: str
    email: EmailStr
    otp: str


# ==============================
# Helper Functions
# ==============================

def generate_and_send_otp(phone: str, email: str) -> None:
    """
    Generate a secure OTP, store it temporarily, and send it via email.

    Args:
        phone (str): User's phone number (used as OTP key)
        email (str): Email address to send OTP

    Workflow:
        1. Generate a 6-digit cryptographically secure OTP
        2. Store OTP with expiration time
        3. Send OTP via email service

    Notes:
        - OTP expiration defaults to 300 seconds (5 minutes)
        - Expiry duration can be configured via environment variable
    """
    # Generate a secure 6-digit OTP (100000 - 999999)
    otp = str(secrets.randbelow(900000) + 100000)

    # Read OTP expiry time from environment (default: 5 minutes)
    expire_seconds = int(os.getenv("OTP_EXPIRE_SECONDS", 300))

    # Store OTP (e.g., Redis / in-memory store)
    store_otp(phone, otp, expire_seconds)

    # Send OTP to user's email
    send_otp_email(email, otp)


# ============================================================
# LOGIN — Request OTP
# ============================================================

@router.post("/request-otp")
def request_login_otp(
    data: PhoneRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint to request OTP for login.

    Args:
        data (PhoneRequest): Contains user's phone number
        db (Session): Database session dependency

    Returns:
        dict: Success message if OTP is sent

    Raises:
        HTTPException:
            - 404 if user does not exist
    """

    # Fetch user by phone number
    user = get_user_by_phone(db, data.phone)

    # Ensure user exists before sending OTP
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Generate and send OTP to registered email
    generate_and_send_otp(data.phone, user.email)

    return {"message": "OTP sent successfully"}


# ============================================================
# LOGIN — Verify OTP
# ============================================================

@router.post("/verify-otp")
def verify_login_otp(
    data: OTPVerifyRequest,
    db: Session = Depends(get_db)
):
    """
    Verify OTP for login and issue JWT token.

    Args:
        data (OTPVerifyRequest): Contains phone and OTP
        db (Session): Database session dependency

    Returns:
        dict:
            - access_token (str): JWT token
            - token_type (str): Bearer token type
            - user (dict): Basic user details

    Raises:
        HTTPException:
            - 400 if OTP is invalid or expired
            - 404 if user does not exist
    """

    # Validate OTP
    if not verify_otp(data.phone, data.otp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )

    # Fetch user after OTP validation
    user = get_user_by_phone(db, data.phone)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Generate JWT token with user identity and role
    token = create_access_token({
        "user_id": user.user_id,
        "usertype": user.usertype
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "user_id": user.user_id,
            "email": user.email,
            "usertype": user.usertype  # Required for frontend role handling
        }
    }


# ============================================================
# REGISTER — Request OTP
# ============================================================

@router.post("/register-otp")
def request_register_otp(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Request OTP for new user registration.

    Args:
        data (RegisterRequest): Contains phone and email
        db (Session): Database session dependency

    Returns:
        dict: Success message

    Raises:
        HTTPException:
            - 400 if user already exists
    """

    # Prevent duplicate user registration
    if get_user_by_phone(db, data.phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    # Generate and send OTP for registration
    generate_and_send_otp(data.phone, data.email)

    return {"message": "Registration OTP sent"}


# ============================================================
# REGISTER — Verify OTP & Create User
# ============================================================

@router.post("/register")
def register_user(
    data: RegisterVerifyRequest,
    db: Session = Depends(get_db)
):
    """
    Verify OTP and create a new user account.

    Args:
        data (RegisterVerifyRequest): Contains phone, email, and OTP
        db (Session): Database session dependency

    Returns:
        dict:
            - access_token (str): JWT token
            - token_type (str): Bearer
            - user (object): Created user object

    Raises:
        HTTPException:
            - 400 if OTP is invalid/expired
            - 400 if user already exists
    """

    # Validate OTP before proceeding
    if not verify_otp(data.phone, data.otp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )

    # Prevent duplicate user creation
    if get_user_by_phone(db, data.phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    # Create new user in database
    user = create_user(db, data.phone, data.email)

    # Generate JWT token (minimal payload)
    token = create_access_token({"user_id": user.user_id})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user,
    }