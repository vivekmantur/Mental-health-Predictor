from pydantic import BaseModel, conlist
from typing import List, Optional


class PHQ9Request(BaseModel):

    # exactly 9 answers, values 0–3
    answers: conlist(int, min_length=9, max_length=9)

    notes: Optional[str] = None


class PHQ9Response(BaseModel):
    score: int
    severity: str
    answers: List[int]
    insight: str
    recommendation: str
    

class PHQ9SubmitResponse(BaseModel):
    score: int
    severity: str
    status: str


class PHQ9ResultResponse(BaseModel):
    score: int
    severity: str
    answers: List[int]
    insight: Optional[str]
    recommendation: Optional[str]
    status: str
    
class AssessmentUpdate(BaseModel):
    score: int
    severity: str
    insight: Optional[str] = None
    recommendation: Optional[str] = None


class StatusUpdate(BaseModel):
    status: str