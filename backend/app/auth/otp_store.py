"""
OTP Storage Utility

Handles storing and verifying OTPs with expiration support.
NOTE:
This implementation uses in-memory storage and is suitable
only for development/testing environments.
"""

import time
from typing import Dict, Any


# ==============================
# In-memory OTP storage
# ==============================

# Structure:
# {
#   phone: {
#       "otp": str,
#       "expires": float (timestamp)
#   }
# }
otp_db: Dict[str, Dict[str, Any]] = {}


# ==============================
# Store OTP
# ==============================

def store_otp(phone: str, otp: str, expire_seconds: int) -> None:
    """
    Store OTP with expiration time.

    Args:
        phone (str): User phone number.
        otp (str): Generated OTP.
        expire_seconds (int): Expiration duration in seconds.
    """
    otp_db[phone] = {
        "otp": otp,
        "expires": time.time() + expire_seconds,
    }


# ==============================
# Verify OTP
# ==============================

def verify_otp(phone: str, otp: str) -> bool:
    """
    Verify OTP for a phone number.

    Args:
        phone (str): User phone number.
        otp (str): OTP entered by user.

    Returns:
        bool: True if OTP is valid, otherwise False.
        
    """
    print(f"Verifying OTP for {phone}: {otp}")  # Debug log
    data = otp_db.get(phone)

    if not data:
        return False

    # Check expiration
    if time.time() > data["expires"]:
        # Remove expired OTP
        otp_db.pop(phone, None)
        return False

    # Validate OTP
    is_valid = data["otp"] == otp

    # Optional: remove OTP after successful verification
    if is_valid:
        otp_db.pop(phone, None)

    return is_valid