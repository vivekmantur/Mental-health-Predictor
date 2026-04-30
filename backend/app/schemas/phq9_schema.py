"""
PHQ-9 Schemas

Defines all request and response models related to:
- PHQ-9 submission
- Result retrieval
- Doctor updates
- Status updates

Design Notes:
- Uses strict validation for answers (exactly 9 values)
- Separates request/response schemas for clarity
- Supports optional AI/doctor-generated fields
"""

from pydantic import BaseModel, conlist
from typing import List, Optional


# ---------------------------------------------------------
# PHQ-9 Submission Request
# ---------------------------------------------------------
class PHQ9Request(BaseModel):
    """
    Request schema for submitting PHQ-9 assessment.

    Attributes:
        answers (List[int]): List of 9 responses (values 0–3)
        notes (Optional[str]): Optional user notes for additional context

    Validation:
        - Exactly 9 answers required
        - Each value should be between 0 and 3 (validated in service layer)
    """

    # exactly 9 answers, values 0–3
    answers: conlist(int, min_length=9, max_length=9)

    notes: Optional[str] = None


# ---------------------------------------------------------
# Full PHQ-9 Response (with AI output)
# ---------------------------------------------------------
class PHQ9Response(BaseModel):
    """
    Response schema for complete PHQ-9 result.

    Attributes:
        score (int): Total PHQ-9 score (0–27)
        severity (str): Severity level based on score
        answers (List[int]): Original responses
        insight (str): AI-generated mental health insight
        recommendation (str): AI-generated recommendation
    """

    score: int
    severity: str
    answers: List[int]
    insight: str
    recommendation: str


# ---------------------------------------------------------
# Submit Response (Minimal)
# ---------------------------------------------------------
class PHQ9SubmitResponse(BaseModel):
    """
    Response after submitting PHQ-9.

    Attributes:
        score (int): Calculated score
        severity (str): Derived severity level
        status (str): Current status (typically 'pending')
    """

    score: int
    severity: str
    status: str


# ---------------------------------------------------------
# PHQ-9 Result Response (Flexible)
# ---------------------------------------------------------
class PHQ9ResultResponse(BaseModel):
    """
    Response schema for fetching PHQ-9 results.

    Attributes:
        score (int): PHQ-9 score
        severity (str): Severity level
        answers (List[int]): User responses
        insight (Optional[str]): AI/doctor insight (may be absent initially)
        recommendation (Optional[str]): Recommendation (may be absent initially)
        status (str): Current status of assessment
    """

    score: int
    severity: str
    answers: List[int]
    insight: Optional[str]
    recommendation: Optional[str]
    status: str


# ---------------------------------------------------------
# Doctor Assessment Update
# ---------------------------------------------------------
class AssessmentUpdate(BaseModel):
    """
    Schema for updating assessment details by doctor.

    Attributes:
        score (int): Updated score (if recalculated)
        severity (str): Updated severity level
        insight (Optional[str]): Updated insight
        recommendation (Optional[str]): Updated recommendation
        doctor_notes (Optional[str]): Additional notes from doctor
    """

    score: int
    severity: str
    insight: Optional[str] = None
    recommendation: Optional[str] = None
    doctor_notes: Optional[str] = None


# ---------------------------------------------------------
# Status Update Schema
# ---------------------------------------------------------
class StatusUpdate(BaseModel):
    """
    Schema for updating assessment status.

    Attributes:
        status (str): New status of assessment

    Common Values:
        - "pending"
        - "success"
        - "rejected" (optional based on workflow)
    """

    status: str