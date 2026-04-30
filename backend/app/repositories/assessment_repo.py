from sqlalchemy.orm import Session
from app.models.assessment import Assessment


# ---------------------------------------------------------
# Save Assessment to Database
# ---------------------------------------------------------
def save_assessment(db, user_id, answers, score, severity, notes, dsm_result):
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
        notes=notes,
        category=dsm_result.get("category"),
        subcategory=dsm_result.get("subcategory"),
        disorder=dsm_result.get("disorder")
    )

    print("💾 Saving assessment to DB:", new_assessment.__dict__)

    db.add(new_assessment)
    db.commit()
    db.refresh(new_assessment)

    return new_assessment

def update_llm_result(db: Session, assessment_id: int, insight: str, recommendation: str):
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()

    if not assessment:
        return

    assessment.insight = insight
    assessment.recommendation = recommendation
    assessment.status = "pending"

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    # verify
    fresh = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    print("📦 DB VALUE:", fresh.insight[:50])
    
def get_last_two_success_assessments(db, user_id):
    return (
        db.query(Assessment)
        .filter(
            Assessment.user_id == user_id,
            Assessment.status == "success"
        )
        .order_by(Assessment.created_at.desc())
        .limit(2)
        .all()
    )
    
def get_latest_success_assessment(db: Session, user_id: int):
    return (
        db.query(Assessment)
        .filter(
            Assessment.user_id == user_id,
            Assessment.status == "success"
        )
        .order_by(Assessment.created_at.desc())
        .first()
    )


def get_assessment_history(db: Session, user_id: int):
    return (
        db.query(Assessment)
        .filter(
            Assessment.user_id == user_id,
            Assessment.status == "success"
        )
        .order_by(Assessment.created_at.asc())
        .all()
    )