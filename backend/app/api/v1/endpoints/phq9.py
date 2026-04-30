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

# ✅ Keep LLM only for insights
from app.services.insight_service import generate_insight
from app.services.recommendation_service import generate_recommendation
from app.services.embedding_service import DSMEmbeddingService


from app.repositories.assessment_repo import (
    get_last_two_success_assessments,
    get_latest_success_assessment,
    get_assessment_history
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/submit", response_model=PHQ9SubmitResponse)
def submit_phq9(data: PHQ9Request, db: Session = Depends(get_db),user: dict = Depends(get_current_user)):
    user_id = user["user_id"]  # Extract user_id from token payload
    embedding_service = DSMEmbeddingService()
    # ---------------------------------------------------------
    # ✅ Step 1: Validate answers
    # ---------------------------------------------------------
    for val in data.answers:
        if val not in [0, 1, 2, 3]:
            raise HTTPException(status_code=400, detail="Invalid answer value")

    # ---------------------------------------------------------
    # ✅ Step 2: Calculate score (NO LLM)
    # ---------------------------------------------------------
    score, severity = calculate_phq9_score(data.answers)
    # ---------------------------------------------------------
# ✅ Step 2.5: Get DSM mapping from notes
# ---------------------------------------------------------
    dsm_result = embedding_service.find_best_match(data.notes or "")

    # ---------------------------------------------------------
    # ✅ Step 3: Save to DB
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
    # ✅ Step 4: Prepare LLM input (clean + structured)
    # ---------------------------------------------------------
    llm_context = f"""
    PHQ-9 Score: {score}
    Severity: {severity}
    User Notes: {data.notes if data.notes else "No additional notes"}
    """
    # ---------------------------------------------------------
    # ✅ Step 5: Generate insight + recommendation (LLM)
    # ---------------------------------------------------------
    insight = generate_insight(llm_context,severity)
    print("💡 Insight Generated:", insight)
    recommendation = generate_recommendation(llm_context, severity)
    print("✅ Recommendation Generated:", recommendation)
    update_llm_result(
        db=db,
        assessment_id=assessment.id,
        insight=insight,
        recommendation=recommendation
    )

    # ---------------------------------------------------------
    # ✅ Response
    # ---------------------------------------------------------
    return {
        "score": score,
        "severity": severity,
        "status": "pending"
    }
    
@router.get("/my-assessments")
def get_my_assessments(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    user_id = user["user_id"]

    query = text("""
        SELECT id, score, severity, status, created_at,approved_at,
            insight, recommendation,
            category, subcategory, disorder,doctor_notes
        FROM assessments
        WHERE user_id = :uid
        ORDER BY created_at DESC
    """)

    result = db.execute(query, {"uid": user_id}).fetchall()

    return [dict(row._mapping) for row in result]

@router.get("/trend-analysis")
def get_trend_analysis(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    records = get_last_two_success_assessments(db, user["user_id"])

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

    ai_response = generate_trend_analysis(latest, previous)

    return {
        "latest_score": latest.score,
        "previous_score": previous.score,
        "category": latest.category,     # ✅ ADD THIS
        "disorder": latest.disorder,     # ✅ ADD THIS
        "insight": ai_response["insight"],
        "recommendation": ai_response["recommendation"]
    }
    
    
@router.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    user_id = user["user_id"]

    # ---------------------------------------------------------
    # ✅ Latest Assessment
    # ---------------------------------------------------------
    latest = get_latest_success_assessment(db, user_id)

    if not latest:
        return {"message": "No assessments found"}

    # ---------------------------------------------------------
    # ✅ Extract answers (Q1–Q9)
    # ---------------------------------------------------------
    answers = [
        latest.q1, latest.q2, latest.q3,
        latest.q4, latest.q5, latest.q6,
        latest.q7, latest.q8, latest.q9
    ]

    # ---------------------------------------------------------
    # ✅ Trend (last two)
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
    # ✅ History for chart
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
    # ✅ Final Response
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