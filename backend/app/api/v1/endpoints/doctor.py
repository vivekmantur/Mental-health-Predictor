from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from app.db.database import SessionLocal
from app.dependencies import get_current_user
from app.models.assessment import Assessment
from app.models.user import User
from app.schemas.phq9_schema import AssessmentUpdate, StatusUpdate
from datetime import datetime

router = APIRouter()


def get_db():
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
    if user.get("usertype") != "doctor":
        raise HTTPException(status_code=403, detail="Access denied")

    data = (
        db.query(Assessment, User)
        .join(User, User.user_id == Assessment.user_id)
        .all()
    )

    result = []

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
    if user["usertype"] != "doctor":
        raise HTTPException(status_code=403, detail="Not authorized")

    query = text("""
        SELECT a.id, a.score, a.severity, a.status, a.created_at,
               a.insight, a.recommendation,
               u.email
        FROM assessments a
        JOIN users u ON a.user_id = u.user_id
        ORDER BY a.created_at DESC
    """)

    result = db.execute(query).fetchall()

    return [dict(row._mapping) for row in result]


@router.put("/assessments/{assessment_id}")
def update_assessment(
    assessment_id: int,
    data: AssessmentUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    if user["usertype"] != "doctor":
        raise HTTPException(status_code=403, detail="Not authorized")

    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    assessment.score = data.score
    assessment.severity = data.severity
    assessment.insight = data.insight
    assessment.recommendation = data.recommendation
    assessment.doctor_notes = data.doctor_notes
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
    if user["usertype"] != "doctor":
        raise HTTPException(status_code=403, detail="Not authorized")

    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    # ✅ Update status
    assessment.status = data.status

    # ✅ NEW: Update approved_at
    if data.status.lower() == "success":
        assessment.approved_at = datetime.utcnow()
    else:
        assessment.approved_at = None  # optional reset

    db.commit()
    db.refresh(assessment)

    return {"message": "Status updated successfully"}
# =========================================================
# ✅ NEW METHODS (FOR PATIENT → ASSESSMENT FLOW)
# =========================================================

# 🔥 1. Get unique patient list (latest assessment info)
@router.get("/patients-list")
def get_unique_patients(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
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


# 🔥 2. Get assessments for selected patient
@router.get("/patient-assessments/{user_id}")
def get_patient_assessments(
    user_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    if user.get("usertype") != "doctor":
        raise HTTPException(status_code=403, detail="Access denied")

    query = text("""
        SELECT id, score, severity, status, created_at,
               insight, recommendation,approved_at,doctor_notes
        FROM assessments
        WHERE user_id = :uid
        ORDER BY created_at DESC
    """)

    result = db.execute(query, {"uid": user_id}).fetchall()

    return [dict(row._mapping) for row in result]