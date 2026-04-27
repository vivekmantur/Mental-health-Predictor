from sqlalchemy import Column, Integer, String
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    usertype = Column(String, default="patient")