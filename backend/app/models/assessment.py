from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from datetime import datetime
from app.db.database import Base


# ---------------------------------------------------------
# Assessment Model
# Represents a PHQ-9 assessment record in the database
# ---------------------------------------------------------
class Assessment(Base):
    __tablename__ = "assessments"

    # -----------------------------------------------------
    # Primary Identifier
    # -----------------------------------------------------
    id = Column(Integer, primary_key=True, index=True)

    # -----------------------------------------------------
    # User Information
    # -----------------------------------------------------
    user_id = Column(String, index=True)

    # -----------------------------------------------------
    # PHQ-9 Individual Question Scores (0–3 each)
    # -----------------------------------------------------
    q1 = Column(Integer)
    q2 = Column(Integer)
    q3 = Column(Integer)
    q4 = Column(Integer)
    q5 = Column(Integer)
    q6 = Column(Integer)
    q7 = Column(Integer)
    q8 = Column(Integer)
    q9 = Column(Integer)

    # -----------------------------------------------------
    # Aggregated Results
    # -----------------------------------------------------
    score = Column(Integer)        # Total PHQ-9 score (0–27)
    severity = Column(String)      # Severity label (e.g., Mild, Moderate, Severe)

    # -----------------------------------------------------
    # Raw User Input (Free-text answers)
    # Stored as JSON for flexibility
    # -----------------------------------------------------
    answers_text = Column(JSON)

    # -----------------------------------------------------
    # Timestamp
    # -----------------------------------------------------
    created_at = Column(DateTime, default=datetime.utcnow)