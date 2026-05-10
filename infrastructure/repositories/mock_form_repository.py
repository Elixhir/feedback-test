from typing import List, Optional, Dict
from domain.entities.form import Form
from domain.repositories.form_repository import FormRepository
from domain.constants import FormStatus
from infrastructure.data.mock_forms import get_initial_forms

class MockFormRepository(FormRepository):
    def __init__(self):
        self.forms: Dict[str, Form] = {}
        self.form_history: Dict[str, List[Form]] = {}
        self._initialize_mock_data()
    
    def _initialize_mock_data(self):
        for form in get_initial_forms():
            self.forms[form.id] = form
            self.form_history[form.id] = [form]
    
    def get_all(self) -> List[Form]:
        return [f for f in self.forms.values() if f.status == FormStatus.ACTIVE.value]
    
    def get_by_id(self, form_id: str) -> Optional[Form]:
        return self.forms.get(form_id)
    
    def get_by_status(self, status: str) -> List[Form]:
        return [f for f in self.forms.values() if f.status == status]
    
    def create(self, form: Form) -> Form:
        self.forms[form.id] = form
        if form.id not in self.form_history:
            self.form_history[form.id] = []
        self.form_history[form.id].append(form)
        return form
    
    def update(self, form_id: str, form: Form) -> Optional[Form]:
        if form_id in self.forms:
            self.forms[form_id] = form
            if form_id not in self.form_history:
                self.form_history[form_id] = []
            self.form_history[form_id].append(form)
            return form
        return None
    
    def get_version_history(self, form_id: str) -> List[Form]:
        return self.form_history.get(form_id, [])
    
    def delete(self, form_id: str) -> bool:
        if form_id in self.forms:
            form = self.forms[form_id]
            form.status = FormStatus.ARCHIVED.value
            self.forms[form_id] = form
            return True
        return False