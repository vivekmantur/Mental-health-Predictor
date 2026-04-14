from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Schemas
from app.schemas.phq9_schema import PHQ9Request, PHQ9Response

# Database
from app.db.database import SessionLocal

# Repository
from app.repositories.assessment_repo import save_assessment

# Services
from app.services.scoring_service import calculate_phq9_score
from app.services.insight_service import generate_insight
from app.services.recommendation_service import generate_recommendation

# LLM Client
from app.llm.llm_client import ai_score_answers


# Initialize API Router
router = APIRouter()


def get_db():
    """
    Dependency function to provide a database session.
    Ensures that the DB session is properly closed after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/submit")
def submit_phq9(data: PHQ9Request, db: Session = Depends(get_db)):
    """
    Endpoint to process PHQ-9 assessment submission.

    Workflow:
    1. Convert user textual answers into numerical scores using AI
    2. Calculate total PHQ-9 score and severity
    3. Persist assessment data in database
    4. Generate AI-based insights
    5. Generate personalized recommendations
    """

    # ---------------------------------------------------------
    # Step 1: Convert natural language answers → PHQ-9 scores
    # ---------------------------------------------------------
    scores = ai_score_answers(data.answers_text)

    # Debug log (can be replaced with proper logger in production)
    print("FINAL SCORES:", scores)

    # ---------------------------------------------------------
    # Step 2: Calculate total score and severity level
    # ---------------------------------------------------------
    score, severity = calculate_phq9_score(scores)

    # ---------------------------------------------------------
    # Step 3: Save assessment data into database
    # ---------------------------------------------------------
    save_assessment(
        db,
        data.user_id,
        scores,
        score,
        severity,
        data.answers_text
    )

    # ---------------------------------------------------------
    # Step 4: Generate AI-driven insights
    # ---------------------------------------------------------
    insight = generate_insight(data.answers_text, severity)

    # ---------------------------------------------------------
    # Step 5: Generate recommendations based on severity
    # ---------------------------------------------------------
    recommendation = generate_recommendation(data.answers_text, severity)

    # ---------------------------------------------------------
    # Final API Response
    # ---------------------------------------------------------
    return {
        "score": score,
        "severity": severity,
        "ai_scores": scores,
        "insight": insight,
        "recommendation": recommendation
    }