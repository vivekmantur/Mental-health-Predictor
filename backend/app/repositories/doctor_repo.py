"""
Doctor Assessment Update Repository

Handles database updates performed by doctors on assessments.

Responsibilities:
- Updating AI-generated insight (if edited)
- Updating recommendation
- Updating assessment status (approved/rejected/etc.)
"""

from sqlalchemy.orm import Session
from app.models.assessment import Assessment


def update_assessment_by_doctor(
    db: Session,
    assessment_id: int,
    insight: str,
    recommendation: str,
    status: str
):
    """
    Update an assessment based on doctor input.

    Args:
        db (Session): Database session
        assessment_id (int): ID of the assessment to update
        insight (str): Updated insight (can override AI-generated content)
        recommendation (str): Updated recommendation
        status (str): New status (e.g., 'success', 'rejected')

    Returns:
        Assessment | None:
            - Updated assessment object if found
            - None if assessment does not exist

    Notes:
        - This function is typically called after doctor review
        - Allows doctors to override AI-generated outputs
        - Status change may trigger downstream logic (e.g., dashboard updates)
    """

    # Fetch assessment by ID
    assessment = db.query(Assessment).filter(
        Assessment.id == assessment_id
    ).first()

    # Handle case where assessment does not exist
    if not assessment:
        return None

    # ---------------------------------------------------------
    # Update doctor-controlled fields
    # ---------------------------------------------------------
    assessment.insight = insight
    assessment.recommendation = recommendation
    assessment.status = status

    # Persist changes
    db.commit()
    db.refresh(assessment)

    return assessment