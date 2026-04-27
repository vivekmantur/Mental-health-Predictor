"""
Authentication Router

Handles OTP-based login and registration workflows.
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


router = APIRouter()


# ==============================
# Database Dependency
# ==============================

def get_db():
    """
    Provide database session dependency.
    Ensures session is closed after request.
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
    """Request schema for phone-based OTP login."""
    phone: str


class RegisterRequest(BaseModel):
    """Request schema for registration OTP."""
    phone: str
    email: EmailStr


class OTPVerifyRequest(BaseModel):
    """OTP verification schema for login."""
    phone: str
    otp: str


class RegisterVerifyRequest(BaseModel):
    """OTP verification schema for registration."""
    phone: str
    email: EmailStr
    otp: str


# ==============================
# Helper Functions
# ==============================

def generate_and_send_otp(phone: str, email: str) -> None:
    """
    Generate secure OTP, store it, and send via email.
    """
    # Cryptographically secure OTP
    otp = str(secrets.randbelow(900000) + 100000)

    expire_seconds = int(os.getenv("OTP_EXPIRE_SECONDS", 300))

    store_otp(phone, otp, expire_seconds)
    send_otp_email(email, otp)


# ============================================================
# LOGIN — Request OTP
# ============================================================

@router.post("/request-otp")
def request_login_otp(
    data: PhoneRequest,
    db: Session = Depends(get_db)
):
    """Send OTP for existing users."""

    user = get_user_by_phone(db, data.phone)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

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
    """Verify OTP and issue JWT token."""

    if not verify_otp(data.phone, data.otp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )

    user = get_user_by_phone(db, data.phone)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    token = create_access_token({"user_id": user.user_id,"usertype": user.usertype})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "user_id": user.user_id,
            "email": user.email,
            "usertype": user.usertype   # 🔥 MUST
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
    """Send OTP for new user registration."""

    if get_user_by_phone(db, data.phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

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
    """Verify OTP and create a new user."""

    if not verify_otp(data.phone, data.otp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )

    if get_user_by_phone(db, data.phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    user = create_user(db, data.phone, data.email)

    token = create_access_token({"user_id": user.user_id})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user,
    }