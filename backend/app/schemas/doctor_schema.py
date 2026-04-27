from pydantic import BaseModel

class UpdateAssessmentRequest(BaseModel):
    insight: str
    recommendation: str
    status: str   # "pending" or "success"