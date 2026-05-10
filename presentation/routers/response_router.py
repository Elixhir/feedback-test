from fastapi import APIRouter, HTTPException, Depends, Request, Query
from typing import List, Any
from presentation.schemas.response_schemas import ResponseCreateSchema, ResponseSchema, ResponseAnalyticsSchema
from presentation.schemas.pagination import PaginatedResponse
from presentation.mappers.entity_serializer import EntitySerializer
from presentation.mappers.response_mapper import ResponseMapper
from presentation.dependencies import get_response_use_cases
import uuid

router = APIRouter()

def get_use_cases() -> Any:
    return get_response_use_cases()

@router.post("/responses", response_model=ResponseSchema)
def submit_response(
    response_data: ResponseCreateSchema, 
    request: Request,
    use_cases: Any = Depends(get_use_cases)
):
    """
    Submit a response to a form with validation.
    Validates that:
    - Form exists
    - All required questions are answered
    - Answer types match question types
    """
    user_agent = response_data.user_agent or request.headers.get("user-agent", "")
    ip_address = response_data.ip_address or (request.client.host if request.client else None)
    response_entity = ResponseMapper.to_entity_create(
        response_data, 
        str(uuid.uuid4()),
        user_agent=user_agent,
        ip_address=ip_address
    )
    created = use_cases["submit"].execute(response_entity)
    return ResponseSchema(**EntitySerializer.response_to_dict(created))
@router.get("/responses/{form_id}", response_model=PaginatedResponse[ResponseSchema])
def get_responses(
    form_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    use_cases: Any = Depends(get_use_cases)
):
    """Get all responses for a specific form with pagination."""
    responses, total = use_cases["get_by_form"].execute(form_id, page=page, page_size=page_size)
    total_pages = (total + page_size - 1) // page_size
    return PaginatedResponse(
        items=[ResponseSchema(**EntitySerializer.response_to_dict(r)) for r in responses],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1
    )
@router.get("/responses/{form_id}/analytics", response_model=ResponseAnalyticsSchema)
def get_form_analytics(form_id: str, use_cases: Any = Depends(get_use_cases)):
    """
    Get analytics and statistics for a form's responses.
    Returns:
    - Total response count
    - Breakdown by language
    - Recent submissions
    """
    analytics = use_cases["analytics"].execute(form_id)
    return ResponseAnalyticsSchema(**analytics)
