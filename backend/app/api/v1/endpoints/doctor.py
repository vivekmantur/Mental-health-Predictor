"""
Doctor Assessment Router

This module provides endpoints for doctor-side operations including:
- Fetching patients and assessments
- Updating assessment data
- Updating assessment status
- Viewing patient-specific assessment history

Access Control:
- All endpoints are restricted to users with 'doctor' role
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from app.db.database import SessionLocal
from app.dependencies import get_current_user
from app.models.assessment import Assessment
from app.models.user import User
from app.schemas.phq9_schema import AssessmentUpdate, StatusUpdate
from datetime import datetime

# Router instance for doctor endpoints
router = APIRouter()


# =========================================================
# Database Dependency
# =========================================================

def get_db():
    """
    Provides a database session for each request.

    Yields:
        Session: SQLAlchemy session instance

    Ensures:
        - Proper cleanup after request execution
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================================
# EXISTING METHODS (UNCHANGED)
# =========================================================

@router.get("/patients")
def get_all_patients(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Fetch all patients along with their assessment summary.

    Returns:
        List[dict]: Patient details including score and severity

    Raises:
        HTTPException: If user is not a doctor
    """

    # Authorization check
    if user.get("usertype") != "doctor":
        raise HTTPException(status_code=403, detail="Access denied")

    # Join Assessment and User tables
    data = (
        db.query(Assessment, User)
        .join(User, User.user_id == Assessment.user_id)
        .all()
    )

    result = []

    # Transform ORM result into response format
    for assessment, user in data:
        result.append({
            "user_id": user.user_id,
            "email": user.email,
            "score": assessment.score,
            "severity": assessment.severity,
            "created_at": assessment.created_at
        })

    return result


@router.get("/assessments")
def get_all_assessments(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Fetch all assessments with user details.

    Uses raw SQL for optimized query execution.

    Returns:
        List[dict]: Assessment records with user email

    Raises:
        HTTPException: If user is not authorized
    """

    # Authorization check
    if user["usertype"] != "doctor":
        raise HTTPException(status_code=403, detail="Not authorized")

    # Raw SQL query for better performance and control
    query = text("""
        SELECT a.id, a.score, a.severity, a.status, a.created_at,
               a.insight, a.recommendation,
               u.email
        FROM assessments a
        JOIN users u ON a.user_id = u.user_id
        ORDER BY a.created_at DESC
    """)

    result = db.execute(query).fetchall()

    # Convert SQLAlchemy Row objects to dictionaries
    return [dict(row._mapping) for row in result]


@router.put("/assessments/{assessment_id}")
def update_assessment(
    assessment_id: int,
    data: AssessmentUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Update assessment details (doctor input).

    Args:
        assessment_id (int): ID of the assessment
        data (AssessmentUpdate): Updated assessment fields

    Returns:
        dict: Success message

    Raises:
        HTTPException:
            - 403 if unauthorized
            - 404 if assessment not found
    """

    # Authorization check
    if user["usertype"] != "doctor":
        raise HTTPException(status_code=403, detail="Not authorized")

    # Fetch assessment
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    # Update fields from request
    assessment.score = data.score
    assessment.severity = data.severity
    assessment.insight = data.insight
    assessment.recommendation = data.recommendation
    assessment.doctor_notes = data.doctor_notes

    # Persist changes
    db.commit()
    db.refresh(assessment)

    return {"message": "Assessment updated successfully"}


@router.put("/assessments/{assessment_id}/status")
def update_status(
    assessment_id: int,
    data: StatusUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Update assessment status (e.g., success, rejected).

    Business Logic:
        - If status is 'success', set approved_at timestamp
        - Otherwise, reset approved_at

    Args:
        assessment_id (int): Assessment ID
        data (StatusUpdate): Status payload

    Returns:
        dict: Success message
    """

    # Authorization check
    if user["usertype"] != "doctor":
        raise HTTPException(status_code=403, detail="Not authorized")

    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    # Update status field
    assessment.status = data.status

    # Maintain approval timestamp logic
    if data.status.lower() == "success":
        assessment.approved_at = datetime.utcnow()
    else:
        assessment.approved_at = None  # Reset if not approved

    db.commit()
    db.refresh(assessment)

    return {"message": "Status updated successfully"}


# =========================================================
# NEW METHODS (PATIENT → ASSESSMENT FLOW)
# =========================================================

@router.get("/patients-list")
def get_unique_patients(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Fetch unique patients with their latest assessment.

    Uses DISTINCT ON (PostgreSQL-specific) to get latest record per user.

    Returns:
        List[dict]: Unique patient records with latest assessment data
    """

    if user.get("usertype") != "doctor":
        raise HTTPException(status_code=403, detail="Access denied")

    query = text("""
        SELECT DISTINCT ON (u.user_id)
            u.user_id,
            u.email,
            a.score,
            a.severity,
            a.created_at
        FROM users u
        JOIN assessments a ON u.user_id = a.user_id
        ORDER BY u.user_id, a.created_at DESC
    """)

    result = db.execute(query).fetchall()

    return [dict(row._mapping) for row in result]


@router.get("/patient-assessments/{user_id}")
def get_patient_assessments(
    user_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Fetch all assessments for a specific patient.

    Args:
        user_id (int): Patient ID

    Returns:
        List[dict]: Assessment history sorted by latest first

    Notes:
        - Includes doctor inputs (insight, recommendation, notes)
        - Includes approval timestamp
    """

    if user.get("usertype") != "doctor":
        raise HTTPException(status_code=403, detail="Access denied")

    query = text("""
        SELECT id, score, severity, status, created_at,
               insight, recommendation, approved_at, doctor_notes
        FROM assessments
        WHERE user_id = :uid
        ORDER BY created_at DESC
    """)

    result = db.execute(query, {"uid": user_id}).fetchall()

    return [dict(row._mapping) for row in result]