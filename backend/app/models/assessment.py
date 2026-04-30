"""
Assessment Model

Represents a PHQ-9 assessment submitted by a user.

This model stores:
- Individual question responses (Q1–Q9)
- Calculated score and severity
- AI-generated insights and recommendations
- Doctor review data
- DSM-based classification
- Metadata such as timestamps and notes
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.db.database import Base
from sqlalchemy import Column, String, Text, DateTime  # (duplicate import retained intentionally)
from datetime import datetime  # (duplicate import retained intentionally)


class Assessment(Base):
    """
    SQLAlchemy model for PHQ-9 assessments.

    Each record represents one assessment submission by a user.
    """

    __tablename__ = "assessments"

    # ---------------------------------------------------------
    # Primary Identifiers
    # ---------------------------------------------------------
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)  # Foreign key reference to user

    # ---------------------------------------------------------
    # PHQ-9 Responses (Q1–Q9)
    # Each value ranges from 0 to 3
    # ---------------------------------------------------------
    q1 = Column(Integer, nullable=False)
    q2 = Column(Integer, nullable=False)
    q3 = Column(Integer, nullable=False)
    q4 = Column(Integer, nullable=False)
    q5 = Column(Integer, nullable=False)
    q6 = Column(Integer, nullable=False)
    q7 = Column(Integer, nullable=False)
    q8 = Column(Integer, nullable=False)
    q9 = Column(Integer, nullable=False)

    # ---------------------------------------------------------
    # Assessment Status & Doctor Review
    # ---------------------------------------------------------
    status = Column(String, default="pending")
    # Possible values: pending, success, rejected (based on your flow)

    insight = Column(Text)
    # AI-generated mental health insight

    recommendation = Column(Text)
    # AI-generated recommendation

    doctor_notes = Column(Text)
    # Notes added by doctor after review

    approved_at = Column(DateTime, nullable=True)
    # Timestamp when doctor approves assessment

    # ---------------------------------------------------------
    # Scoring & Severity
    # ---------------------------------------------------------
    score = Column(Integer)
    # Total PHQ-9 score (0–27)

    severity = Column(String)
    # Example: Minimal, Mild, Moderate, Moderately Severe, Severe

    # ---------------------------------------------------------
    # DSM Classification (AI/Embedding-based)
    # ---------------------------------------------------------
    category = Column(String, nullable=True)
    # High-level mental health category

    subcategory = Column(String, nullable=True)
    # Subclassification within category

    disorder = Column(String, nullable=True)
    # Specific disorder prediction (if applicable)

    # ---------------------------------------------------------
    # Additional User Input
    # ---------------------------------------------------------
    notes = Column(Text, nullable=True)
    # Free-text notes provided by user during submission

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------
    created_at = Column(DateTime, default=datetime.utcnow)
    # Timestamp of assessment creation