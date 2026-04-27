"""
Email Utility Module

Handles OTP email sending functionality using SMTP.
"""

import os
import smtplib
import logging
from typing import Optional

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# ==============================
# Logger Configuration
# ==============================

logger = logging.getLogger(__name__)


# ==============================
# SMTP Configuration
# ==============================

SMTP_SERVER: Optional[str] = os.getenv("SMTP_SERVER")
SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
EMAIL_USER: Optional[str] = os.getenv("EMAIL_USER")
EMAIL_PASS: Optional[str] = os.getenv("EMAIL_PASS")


# ==============================
# OTP Email Sender
# ==============================

def send_otp_email(email: str, otp: str) -> bool:
    """
    Send OTP email to the user.

    Args:
        email (str): Recipient email address.
        otp (str): One-time password.

    Returns:
        bool: True if email sent successfully, False otherwise.
    """

    if not all([SMTP_SERVER, EMAIL_USER, EMAIL_PASS]):
        logger.error("SMTP configuration is missing.")
        return False

    subject = "Your AI Phq9 OTP"

    body = f"""
Hello,

Your OTP for Phq9 login is: {otp}

This OTP will expire in 5 minutes.

If you did not request this, please ignore.

Regards,
Phq9 Team
"""

    # Create email message
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        # Use context manager to ensure connection closes properly
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        logger.info("OTP email sent successfully to %s", email)
        return True

    except Exception as exc:
        logger.exception("Email OTP sending failed: %s", exc)
        return False