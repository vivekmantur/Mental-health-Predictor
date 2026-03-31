from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.db.database import Base
from sqlalchemy import JSON

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)

    q1 = Column(Integer)
    q2 = Column(Integer)
    q3 = Column(Integer)
    q4 = Column(Integer)
    q5 = Column(Integer)
    q6 = Column(Integer)
    q7 = Column(Integer)
    q8 = Column(Integer)
    q9 = Column(Integer)

    score = Column(Integer)
    severity = Column(String)

    # ✅ ADD THIS
    answers_text = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)