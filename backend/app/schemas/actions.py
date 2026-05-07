from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ActionBase(BaseModel):
    action_type: str
    action_summary: str
    department: str
    deadline: str = "Not specified"
    priority: str = "Medium"
    compliance_requirement: str = ""
    appeal_consideration: str = ""
    confidence: float = Field(ge=0, le=1)
    source_text: str
    extraction_reason: str = ""
    page_reference: Optional[int] = None


class ActionOut(ActionBase):
    id: int
    judgment_id: int
    verification_status: str
    reviewer_notes: str = ""
    created_at: datetime

    class Config:
        from_attributes = True


class ActionUpdate(BaseModel):
    action_type: Optional[str] = None
    action_summary: Optional[str] = None
    department: Optional[str] = None
    deadline: Optional[str] = None
    priority: Optional[str] = None
    compliance_requirement: Optional[str] = None
    appeal_consideration: Optional[str] = None
    reviewer_notes: Optional[str] = None


class VerificationRequest(ActionUpdate):
    status: str

