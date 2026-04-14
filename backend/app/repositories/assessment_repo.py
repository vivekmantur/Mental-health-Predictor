from sqlalchemy.orm import Session
from app.models.assessment import Assessment


# ---------------------------------------------------------
# Save Assessment to Database
# ---------------------------------------------------------
def save_assessment(db: Session, user_id, answers, score, severity, answers_text):
    """
    Persists a PHQ-9 assessment record into the database.

    Args:
        db (Session): SQLAlchemy DB session
        user_id (str): Identifier for the user
        answers (list[int]): List of 9 PHQ-9 scores (0–3)
        score (int): Total PHQ-9 score
        severity (str): Severity classification
        answers_text (list[str]): Raw user answers (free text)

    Returns:
        Assessment: Saved assessment object
    """

    # -----------------------------------------------------
    # Create Assessment ORM object
    # -----------------------------------------------------
    new_assessment = Assessment(
        user_id=user_id,

        # Individual question scores
        q1=answers[0],
        q2=answers[1],
        q3=answers[2],
        q4=answers[3],
        q5=answers[4],
        q6=answers[5],
        q7=answers[6],
        q8=answers[7],
        q9=answers[8],

        # Aggregated results
        score=score,
        severity=severity,

        # Raw input
        answers_text=answers_text
    )

    # -----------------------------------------------------
    # Persist to database
    # -----------------------------------------------------
    db.add(new_assessment)     # Stage object for insert
    db.commit()                # Commit transaction
    db.refresh(new_assessment) # Refresh to get updated DB state

    return new_assessment