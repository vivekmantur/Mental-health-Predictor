"""
Assessment Repository

This module handles all database operations related to assessments.

Responsibilities:
- Creating new assessments
- Updating LLM-generated results
- Fetching assessment data for analytics (trend, history, dashboard)

Design Notes:
- Keeps DB logic separate from API/business logic
- Ensures reusable and maintainable queries
"""

from sqlalchemy.orm import Session
from app.models.assessment import Assessment


# ---------------------------------------------------------
# Save Assessment to Database
# ---------------------------------------------------------
def save_assessment(db, user_id, answers, score, severity, notes, dsm_result):
    """
    Create and persist a new assessment record.

    Args:
        db (Session): Database session
        user_id (int): ID of the user submitting the assessment
        answers (list): List of PHQ-9 answers (length = 9)
        score (int): Calculated PHQ-9 score
        severity (str): Severity level derived from score
        notes (str): Optional user notes
        dsm_result (dict): DSM classification result (category, subcategory, disorder)

    Returns:
        Assessment: Newly created assessment object

    Notes:
        - Maps answers to q1–q9 fields
        - Stores DSM classification for later analysis
    """

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

    # Debug: Log object before saving
    print("💾 Saving assessment to DB:", new_assessment.__dict__)

    db.add(new_assessment)
    db.commit()
    db.refresh(new_assessment)

    return new_assessment


# ---------------------------------------------------------
# Update LLM Results
# ---------------------------------------------------------
def update_llm_result(db: Session, assessment_id: int, insight: str, recommendation: str):
    """
    Update assessment with LLM-generated insight and recommendation.

    Args:
        db (Session): Database session
        assessment_id (int): ID of the assessment
        insight (str): Generated insight text
        recommendation (str): Generated recommendation text

    Notes:
        - Sets status to 'pending' after LLM update
        - Used after initial assessment creation
    """

    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()

    if not assessment:
        return  # Silent fail (can be logged in production)

    # Update LLM-generated fields
    assessment.insight = insight
    assessment.recommendation = recommendation

    # Reset status for doctor review
    assessment.status = "pending"

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    # Debug: Verify update
    fresh = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    print("📦 DB VALUE:", fresh.insight[:50])


# ---------------------------------------------------------
# Fetch Last Two Successful Assessments
# ---------------------------------------------------------
def get_last_two_success_assessments(db, user_id):
    """
    Retrieve the latest two successful assessments for a user.

    Args:
        db (Session): Database session
        user_id (int): User ID

    Returns:
        List[Assessment]: Up to two recent successful assessments

    Usage:
        - Used for trend analysis
    """

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


# ---------------------------------------------------------
# Fetch Latest Successful Assessment
# ---------------------------------------------------------
def get_latest_success_assessment(db: Session, user_id: int):
    """
    Retrieve the most recent successful assessment.

    Args:
        db (Session): Database session
        user_id (int): User ID

    Returns:
        Assessment | None: Latest successful assessment

    Usage:
        - Used in dashboard API
    """

    return (
        db.query(Assessment)
        .filter(
            Assessment.user_id == user_id,
            Assessment.status == "success"
        )
        .order_by(Assessment.created_at.desc())
        .first()
    )


# ---------------------------------------------------------
# Fetch Assessment History
# ---------------------------------------------------------
def get_assessment_history(db: Session, user_id: int):
    """
    Retrieve full history of successful assessments.

    Args:
        db (Session): Database session
        user_id (int): User ID

    Returns:
        List[Assessment]: Chronologically ordered assessment history

    Notes:
        - Ordered ascending for chart plotting (old → new)
    """

    return (
        db.query(Assessment)
        .filter(
            Assessment.user_id == user_id,
            Assessment.status == "success"
        )
        .order_by(Assessment.created_at.asc())
        .all()
    )