from sqlalchemy.orm import Session
from app.models.user import User


def get_user_by_phone(db: Session, phone: str):
    return db.query(User).filter(User.phone_number == phone).first()


def create_user(db: Session, phone: str, email: str):
    user = User(
        phone_number=phone,
        email=email,
        usertype="patient"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user