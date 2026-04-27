"""
JWT Authentication Utilities

This module handles JWT token creation and verification
for user authentication.
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from jose import jwt, JWTError

# ==============================
# Configuration Constants
# ==============================

DEFAULT_SECRET_KEY = (
    "f5c4ec45416b27934a18c21095cb8411db84eb98bab12b40c9ef1bc1b245adb6"
)
SECRET_KEY = os.getenv("JWT_SECRET", DEFAULT_SECRET_KEY)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120


# ==============================
# Token Creation
# ==============================

def create_access_token(data: Dict[str, Any]) -> str:
    """
    Create a JWT access token.

    Args:
        data (Dict[str, Any]): Payload data to encode in token.

    Returns:
        str: Encoded JWT access token.
    """
    to_encode = data.copy()

    # Create expiration timestamp (UTC timezone-aware)
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# ==============================
# Token Verification
# ==============================

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify and decode a JWT token.

    Args:
        token (str): JWT token string.

    Returns:
        Optional[Dict[str, Any]]:
            Decoded payload if valid, otherwise None.
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload

    except JWTError:
        # Token invalid, expired, or corrupted
        return None
