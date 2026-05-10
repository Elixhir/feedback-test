from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from datetime import datetime

class ResponseCreateSchema(BaseModel):
    """Schema for submitting a response to a form."""
    form_id: str
    user_id: Optional[str] = None
    answers: Dict[str, Any]
    language: str = "en"
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None

class ResponseSchema(BaseModel):
    """Schema for response objects from the API."""
    id: str
    form_id: str
    form_version: int
    user_id: Optional[str] = None
    answers: Dict[str, Any]
    language: str
    submitted_at: datetime
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None

class ResponseAnalyticsSchema(BaseModel):
    """Schema for response analytics."""
    form_id: str
    total_responses: int
    responses_by_language: Dict[str, int]
    version: int
    recent_submissions: List[Dict[str, Any]] = []