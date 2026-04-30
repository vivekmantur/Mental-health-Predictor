"""
Assessment Update Schema

Defines the request payload for updating an assessment
by a doctor.

Used in:
- Doctor review/update APIs
"""

from pydantic import BaseModel


class UpdateAssessmentRequest(BaseModel):
    """
    Schema for updating assessment details.

    Attributes:
        insight (str): Updated or refined insight (can override AI-generated content)
        recommendation (str): Updated recommendation provided by doctor
        status (str): Current status of assessment

    Expected Values for status:
        - "pending" → awaiting review or re-evaluation
        - "success" → approved by doctor
        (Other values like "rejected" can be added based on business logic)
    """

    insight: str
    recommendation: str
    status: str   # "pending" or "success"