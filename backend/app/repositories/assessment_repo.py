from sqlalchemy.orm import Session
from app.models.assessment import Assessment

def save_assessment(db: Session, user_id, answers, score, severity, answers_text):
    new_assessment = Assessment(
        user_id=user_id,
        q1=answers[0],
        q2=answers[1],
        q3=answers[2],
        q4=answers[3],
        q5=answers[4],
        q6=answers[5],
        q7=answers[6],
        q8=answers[7],
        q9=answers[8],
        score=score,
        severity=severity,
        answers_text=answers_text   # ✅ STORE TEXT
    )

    db.add(new_assessment)
    db.commit()
    db.refresh(new_assessment)

    return new_assessment