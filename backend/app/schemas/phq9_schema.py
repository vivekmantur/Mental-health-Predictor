from pydantic import BaseModel
from typing import List


# ---------------------------------------------------------
# Request Schema
# ---------------------------------------------------------
class PHQ9Request(BaseModel):
    """
    Schema for incoming PHQ-9 assessment request.

    Attributes:
        user_id (str): Unique identifier for the user
        answers_text (List[str]): List of 9 free-text responses
    """
    user_id: str
    answers_text: List[str]   # Expected length: 9


# ---------------------------------------------------------
# Response Schema
# ---------------------------------------------------------
class PHQ9Response(BaseModel):
    """
    Schema for PHQ-9 assessment response.

    Attributes:
        score (int): Total PHQ-9 score (0–27)
        severity (str): Severity level (e.g., Mild, Moderate, Severe)
        ai_scores (List[int]): Individual AI-generated scores (length 9)
    """
    score: int
    severity: str
    ai_scores: List[int]