from pydantic import BaseModel
from typing import List

class PHQ9Request(BaseModel):
    user_id: str
    answers_text: List[str]   # ✅ REQUIRED

class PHQ9Response(BaseModel):
    score: int
    severity: str
    ai_scores: List[int]