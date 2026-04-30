"""
PHQ-9 Assessment Router

This module handles:
- PHQ-9 submission and scoring
- LLM-based insight & recommendation generation
- Patient assessment history
- Trend analysis (progress tracking)
- Dashboard aggregation data

Design Highlights:
- Scoring is deterministic (no LLM)
- LLM is used only for insights and recommendations
- DSM-based embedding used for classification support
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.phq9_schema import PHQ9Request, PHQ9Response, PHQ9SubmitResponse
from app.db.database import SessionLocal
from app.repositories.assessment_repo import save_assessment, update_llm_result
from app.services.scoring_service import calculate_phq9_score
from app.dependencies import get_current_user
from app.services.trend_service import generate_trend_analysis
from app.repositories.assessment_repo import get_last_two_success_assessments

# LLM & AI services
from app.services.insight_service import generate_insight
from app.services.recommendation_service import generate_recommendation
from app.services.embedding_service import DSMEmbeddingService

# Repository methods
from app.repositories.assessment_repo import (
    get_last_two_success_assessments,
    get_latest_success_assessment,
    get_assessment_history
)

router = APIRouter()


# =========================================================
# Database Dependency
# =========================================================

def get_db():
    """
    Provides a database session.

    Yields:
        Session: SQLAlchemy session

    Ensures:
        Proper cleanup after request lifecycle
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================================
# SUBMIT PHQ-9
# =========================================================

@router.post("/submit", response_model=PHQ9SubmitResponse)
def submit_phq9(
    data: PHQ9Request,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Submit PHQ-9 responses and generate results.

    Workflow:
        1. Validate answers
        2. Calculate score (deterministic logic)
        3. Map DSM category using embeddings
        4. Save assessment to DB
        5. Generate insight & recommendation (LLM)
        6. Update DB with LLM outputs

    Args:
        data (PHQ9Request): User answers and optional notes
        db (Session): Database session
        user (dict): Authenticated user payload

    Returns:
        dict: Score, severity, and status

    Raises:
        HTTPException: If invalid answer values are provided
    """

    user_id = user["user_id"]  # Extract user ID from JWT
    embedding_service = DSMEmbeddingService()

    # ---------------------------------------------------------
    # Step 1: Validate answers (must be 0–3)
    # ---------------------------------------------------------
    for val in data.answers:
        if val not in [0, 1, 2, 3]:
            raise HTTPException(status_code=400, detail="Invalid answer value")

    # ---------------------------------------------------------
    # Step 2: Calculate PHQ-9 score (no AI)
    # ---------------------------------------------------------
    score, severity = calculate_phq9_score(data.answers)

    # ---------------------------------------------------------
    # Step 2.5: DSM classification using embeddings
    # ---------------------------------------------------------
    dsm_result = embedding_service.find_best_match(data.notes or "")

    # ---------------------------------------------------------
    # Step 3: Save assessment
    # ---------------------------------------------------------
    assessment = save_assessment(
        db=db,
        user_id=user_id,
        answers=data.answers,
        score=score,
        severity=severity,
        notes=data.notes,
        dsm_result=dsm_result
    )

    # ---------------------------------------------------------
    # Step 4: Prepare structured LLM context
    # ---------------------------------------------------------
    llm_context = f"""
    PHQ-9 Score: {score}
    Severity: {severity}
    User Notes: {data.notes if data.notes else "No additional notes"}
    """

    # ---------------------------------------------------------
    # Step 5: Generate AI insights & recommendations
    # ---------------------------------------------------------
    insight = generate_insight(llm_context, severity)
    print("💡 Insight Generated:", insight)

    recommendation = generate_recommendation(llm_context, severity)
    print("✅ Recommendation Generated:", recommendation)

    # Persist LLM outputs
    update_llm_result(
        db=db,
        assessment_id=assessment.id,
        insight=insight,
        recommendation=recommendation
    )

    # ---------------------------------------------------------
    # Final Response
    # ---------------------------------------------------------
    return {
        "score": score,
        "severity": severity,
        "status": "pending"  # Doctor review pending
    }


# =========================================================
# GET USER ASSESSMENTS
# =========================================================

@router.get("/my-assessments")
def get_my_assessments(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Fetch all assessments for the logged-in user.

    Returns:
        List[dict]: Assessment history with insights and doctor notes

    Notes:
        - Includes DSM classification fields
        - Ordered by latest first
    """

    user_id = user["user_id"]

    query = text("""
        SELECT id, score, severity, status, created_at, approved_at,
            insight, recommendation,
            category, subcategory, disorder, doctor_notes
        FROM assessments
        WHERE user_id = :uid
        ORDER BY created_at DESC
    """)

    result = db.execute(query, {"uid": user_id}).fetchall()

    return [dict(row._mapping) for row in result]


# =========================================================
# TREND ANALYSIS
# =========================================================

@router.get("/trend-analysis")
def get_trend_analysis(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Analyze trend between last two successful assessments.

    Returns:
        dict:
            - Score comparison
            - DSM classification
            - AI-generated trend insight & recommendation

    Notes:
        Requires at least 2 successful assessments
    """

    records = get_last_two_success_assessments(db, user["user_id"])

    # Not enough data case
    if len(records) < 2:
        return {
            "message": "Not enough data",
            "insight": None,
            "recommendation": None,
            "category": None,
            "disorder": None
        }

    latest = records[0]
    previous = records[1]

    # Generate AI-based trend analysis
    ai_response = generate_trend_analysis(latest, previous)

    return {
        "latest_score": latest.score,
        "previous_score": previous.score,
        "category": latest.category,
        "disorder": latest.disorder,
        "insight": ai_response["insight"],
        "recommendation": ai_response["recommendation"]
    }


# =========================================================
# DASHBOARD DATA
# =========================================================

@router.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Fetch aggregated dashboard data for frontend.

    Includes:
        - Latest assessment
        - Trend comparison
        - Historical chart data

    Returns:
        dict: Dashboard payload
    """

    user_id = user["user_id"]

    # ---------------------------------------------------------
    # Latest Assessment
    # ---------------------------------------------------------
    latest = get_latest_success_assessment(db, user_id)

    if not latest:
        return {"message": "No assessments found"}

    # ---------------------------------------------------------
    # Extract Q1–Q9 answers
    # ---------------------------------------------------------
    answers = [
        latest.q1, latest.q2, latest.q3,
        latest.q4, latest.q5, latest.q6,
        latest.q7, latest.q8, latest.q9
    ]

    # ---------------------------------------------------------
    # Trend Data (last two assessments)
    # ---------------------------------------------------------
    last_two = get_last_two_success_assessments(db, user_id)

    trend_data = {
        "latest_score": latest.score,
        "previous_score": None,
        "insight": None,
        "recommendation": None,
        "history": []
    }

    if len(last_two) >= 2:
        trend_ai = generate_trend_analysis(last_two[0], last_two[1])

        trend_data.update({
            "previous_score": last_two[1].score,
            "insight": trend_ai.get("insight"),
            "recommendation": trend_ai.get("recommendation")
        })

    # ---------------------------------------------------------
    # Historical Data (for charts)
    # ---------------------------------------------------------
    history = get_assessment_history(db, user_id)

    trend_data["history"] = [
        {
            "date": record.created_at.strftime("%b %d"),
            "score": record.score
        }
        for record in history
    ]

    # ---------------------------------------------------------
    # Final Dashboard Response
    # ---------------------------------------------------------
    return {
        "latest": {
            "score": latest.score,
            "severity": latest.severity,
            "answers": answers,
            "category": latest.category,
            "subcategory": latest.subcategory,
            "disorder": latest.disorder,
            "insight": latest.insight,
            "recommendation": latest.recommendation
        },
        "trend": trend_data
    }