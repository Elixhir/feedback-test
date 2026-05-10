from typing import List, Optional, Tuple
from datetime import datetime
from domain.entities.form import Form
from domain.repositories.form_repository import FormRepository
from domain.constants import FormStatus, DefaultUser, QuestionType

class GetAllFormsUseCase:
    def __init__(self, repository: FormRepository):
        self.repository = repository
    
    def execute(
        self, 
        page: int = 1, 
        page_size: int = 10, 
        status: Optional[str] = None,
        version: Optional[int] = None
    ) -> Tuple[List[Form], int]:
        
        forms = []
        
        if status:
            try:
                FormStatus(status)
            except ValueError:
                raise ValueError(f"Invalid status: {status}. Must be one of: {', '.join([s.value for s in FormStatus])}")
            forms = self.repository.get_by_status(status)
        else:
            forms = self.repository.get_all()
            if version:
                forms = [f for f in forms if f.version == version]
            else:
                forms = self._get_latest_versions(forms)
        
        if version and not status:
            forms = [f for f in forms if f.version == version]
        
        total = len(forms)
        offset = (page - 1) * page_size
        paginated_forms = forms[offset:offset + page_size]
        return paginated_forms, total
    
    def _get_latest_versions(self, forms: List[Form]) -> List[Form]:
        latest_by_id = {}
        for form in forms:
            if form.id not in latest_by_id or form.version > latest_by_id[form.id].version:
                latest_by_id[form.id] = form
        return list(latest_by_id.values())
    
    def get_by_id(self, form_id: str, version: Optional[int] = None) -> Optional[Form]:
        versions = self.repository.get_version_history(form_id)
        if not versions:
            return None
        
        if version:
            for v in versions:
                if v.version == version:
                    return v
            return None
        
        return max(versions, key=lambda x: x.version)
    
class GetFormByIdUseCase:
    def __init__(self, repository: FormRepository):
        self.repository = repository
    
    def execute(self, form_id: str) -> Optional[Form]:
        return self.repository.get_by_id(form_id)
    
    def get_by_id(self, form_id: str) -> Optional[Form]:
        return self.repository.get_by_id(form_id)
    
class GetFormsByStatusUseCase:
    def __init__(self, repository: FormRepository):
        self.repository = repository
    
    def execute(self, status: str, page: int = 1, page_size: int = 10) -> Tuple[List[Form], int]:
        try:
            FormStatus(status)
        except ValueError:
            raise ValueError(f"Invalid status: {status}. Must be one of: {', '.join([s.value for s in FormStatus])}")
        all_forms = self.repository.get_by_status(status)
        total = len(all_forms)
        offset = (page - 1) * page_size
        paginated_forms = all_forms[offset:offset + page_size]
        return paginated_forms, total


class GetFormVersionsUseCase:
    def __init__(self, repository: FormRepository):
        self.repository = repository
    
    def execute(self, form_id: str) -> List[Form]:
        return self.repository.get_version_history(form_id)


class CreateFormUseCase:
    def __init__(self, repository: FormRepository):
        self.repository = repository
    
    def execute(self, form: Form, created_by: DefaultUser = DefaultUser.SYSTEM) -> Form:
        self._validate_questions(form.questions)
        form.created_at = datetime.utcnow()
        form.updated_at = datetime.utcnow()
        form.version = 1
        form.status = FormStatus.ACTIVE.value
        form.created_by = created_by.value
        return self.repository.create(form)
    
    def _validate_questions(self, questions: List) -> None:
        for q in questions:
            if q.type == QuestionType.MULTIPLE_CHOICE:
                if not q.options or len(q.options) < 2:
                    raise ValueError(f"Question '{q.id}' of type 'multiple_choice' requires at least 2 options")
    
    def get_by_id(self, form_id: str) -> Optional[Form]:
        return self.repository.get_by_id(form_id)


class UpdateFormUseCase:
    def __init__(self, repository: FormRepository):
        self.repository = repository
    
    def execute(self, form_id: str, form: Form, updated_by: DefaultUser = DefaultUser.SYSTEM) -> Optional[Form]:
        existing = self.repository.get_by_id(form_id)
        if not existing:
            return None
        if form.questions:
            self._validate_questions(form.questions)
        updated_form = Form(
            id=form_id,
            title=form.title,
            description=form.description,
            questions=form.questions,
            version=existing.version + 1,
            status=form.status if form.status else existing.status,
            created_at=existing.created_at,
            updated_at=datetime.utcnow(),
            created_by=existing.created_by,
            updated_by=updated_by.value
        )
        return self.repository.update(form_id, updated_form)
    
    def _validate_questions(self, questions: List) -> None:
        for q in questions:
            if q.type == QuestionType.MULTIPLE_CHOICE:
                if not q.options or len(q.options) < 2:
                    raise ValueError(f"Question '{q.id}' of type 'multiple_choice' requires at least 2 options")
    
    def get_by_id(self, form_id: str) -> Optional[Form]:
        return self.repository.get_by_id(form_id)
    

class DeleteFormUseCase:
    def __init__(self, repository: FormRepository):
        self.repository = repository
    
    def execute(self, form_id: str) -> bool:
        return self.repository.delete(form_id)