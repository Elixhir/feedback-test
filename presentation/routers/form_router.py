from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Any, Optional, Union
from presentation.schemas.form_schemas import (
    FormCreateSchema, FormUpdateSchema, FormResponseSchema
)
from presentation.schemas.pagination import PaginatedResponse
from presentation.mappers.entity_serializer import EntitySerializer
from presentation.mappers.form_mapper import FormMapper
from presentation.dependencies import get_form_use_cases
import uuid

router = APIRouter()

def get_use_cases() -> Any:
    return get_form_use_cases()

@router.get("/forms", response_model=Union[List[FormResponseSchema], PaginatedResponse[FormResponseSchema]])
def get_forms(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[str] = Query(None, description="Filter by status: active, archived, draft"),
    form_id: Optional[str] = Query(None, description="Get specific form by ID"),
    versions: bool = Query(False, description="If true and form_id provided, return all versions"),
    use_cases: Any = Depends(get_use_cases)
):

    if form_id:
        if versions:
            forms = use_cases["get_versions"].execute(form_id)
            if not forms:
                raise HTTPException(status_code=404, detail="Form not found")
            return [FormResponseSchema(**EntitySerializer.form_to_dict(f)) for f in forms]
        else:
            form = use_cases["get_by_id"].get_by_id(form_id)
            if not form:
                raise HTTPException(status_code=404, detail="Form not found")
            return [FormResponseSchema(**EntitySerializer.form_to_dict(form))]
    
    forms, total = use_cases["get_all"].execute(page=page, page_size=page_size, status=status)
    total_pages = (total + page_size - 1) // page_size
    return PaginatedResponse(
        items=[FormResponseSchema(**EntitySerializer.form_to_dict(f)) for f in forms],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1
    )

@router.post("/forms", response_model=FormResponseSchema)
def create_form(form_data: FormCreateSchema, use_cases: Any = Depends(get_use_cases)):
    """Create a new form with validation."""
    form_entity = FormMapper.to_entity_create(form_data, str(uuid.uuid4()))
    created = use_cases["create"].execute(form_entity)
    return FormResponseSchema(**EntitySerializer.form_to_dict(created))

@router.put("/forms/{form_id}", response_model=FormResponseSchema)
def update_form(form_id: str, form_data: FormUpdateSchema, use_cases: Any = Depends(get_use_cases)):
    """Update an existing form (creates new version)."""
    existing = use_cases["get_by_id"].get_by_id(form_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Form not found")
    form_entity = FormMapper.to_entity_update(form_data, existing, form_id)
    updated = use_cases["update"].execute(form_id, form_entity)
    return FormResponseSchema(**EntitySerializer.form_to_dict(updated))

@router.delete("/forms/{form_id}")
def delete_form(form_id: str, use_cases: Any = Depends(get_use_cases)):
    """Archive a form (soft delete)."""
    if not use_cases["delete"].execute(form_id):
        raise HTTPException(status_code=404, detail="Form not found")
    return {"message": "Form archived successfully", "form_id": form_id}