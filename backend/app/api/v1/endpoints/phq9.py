from fastapi import APIRouter,Depends
from app.schemas.phq9_schema import PHQ9Request, PHQ9Response
from app.services.scoring_service import calculate_phq9_score
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.repositories.assessment_repo import save_assessment
from app.llm.llm_client import ai_score_answers
from app.services.scoring_service import calculate_phq9_score
from app.services.insight_service import generate_insight
from app.services.recommendation_service import generate_recommendation

router = APIRouter()   # ✅ THIS IS IMPORTANT

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@router.post("/submit")
def submit_phq9(data: PHQ9Request, db: Session = Depends(get_db)):

    # 🤖 Step 1: AI converts text → scores
    scores = ai_score_answers(data.answers_text)
  
    print("FINAL SCORES:", scores)  # DEBUGGING

    # 🧮 Step 2: Calculate total
    score, severity = calculate_phq9_score(scores)

    # 💾 Step 3: Save (UPDATED)
    save_assessment(
        db,
        data.user_id,
        scores,
        score,
        severity,
        data.answers_text   # ✅ ADD THIS
    )
      # Step 4: Generate AI insights
    insight = generate_insight(data.answers_text, severity)

    # Step 5: Generate recommendations
    recommendation = generate_recommendation(data.answers_text, severity)

    return {
    "score": score,
    "severity": severity,
    "ai_scores": scores,
    "insight": insight,
    "recommendation": recommendation
}