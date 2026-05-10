from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
from domain.constants import QuestionType

class QuestionSchema(BaseModel):
    """Schema for a question in the API."""
    id: Optional[str] = None
    type: QuestionType
    text: Dict[str, str]
    options: Optional[List[Dict[str, str]]] = None
    required: bool = True

class FormCreateSchema(BaseModel):
    """Schema for creating a new form."""
    title: Dict[str, str]
    description: Dict[str, str]
    questions: List[QuestionSchema]

class FormUpdateSchema(BaseModel):
    """Schema for updating an existing form."""
    title: Optional[Dict[str, str]] = None
    description: Optional[Dict[str, str]] = None
    questions: Optional[List[QuestionSchema]] = None

class FormResponseSchema(BaseModel):
    """Schema for form responses from the API."""
    id: str
    title: Dict[str, str]
    description: Dict[str, str]
    questions: List[QuestionSchema]
    version: int
    status: str = "active"
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None
    updated_by: Optional[str] = None

class FormAnalyticsSchema(BaseModel):
    """Schema for form analytics/feedback summary."""
    form_id: str
    total_responses: int
    responses_by_language: Dict[str, int]
    version: int
    recent_submissions: List[dict] = []