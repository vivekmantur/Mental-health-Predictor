from sqlalchemy.orm import Session
from app.models.assessment import Assessment


def update_assessment_by_doctor(
    db: Session,
    assessment_id: int,
    insight: str,
    recommendation: str,
    status: str
):
    assessment = db.query(Assessment).filter(
        Assessment.id == assessment_id
    ).first()

    if not assessment:
        return None

    assessment.insight = insight
    assessment.recommendation = recommendation
    assessment.status = status

    db.commit()
    db.refresh(assessment)

    return assessment