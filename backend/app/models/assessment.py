from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.db.database import Base
from sqlalchemy import Column, String, Text, DateTime
from datetime import datetime


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)

    q1 = Column(Integer, nullable=False)
    q2 = Column(Integer, nullable=False)
    q3 = Column(Integer, nullable=False)
    q4 = Column(Integer, nullable=False)
    q5 = Column(Integer, nullable=False)
    q6 = Column(Integer, nullable=False)
    q7 = Column(Integer, nullable=False)
    q8 = Column(Integer, nullable=False)
    q9 = Column(Integer, nullable=False)
    status = Column(String, default="pending")
    insight = Column(Text)
    recommendation = Column(Text)
    doctor_notes = Column(Text)
    approved_at = Column(DateTime, nullable=True)

    score = Column(Integer)
    severity = Column(String)
    # ✅ DSM Mapping Fields
    category = Column(String, nullable=True)
    subcategory = Column(String, nullable=True)
    disorder = Column(String, nullable=True)

    # ✅ NEW
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)