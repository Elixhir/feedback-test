from typing import Type, Dict, Any
from domain.repositories.form_repository import FormRepository
from domain.repositories.response_repository import ResponseRepository

class Container:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    def __init__(self):
        if self._initialized:
            return
        self._repositories: Dict[str, Any] = {}
        self._use_cases = {}
        self._repository_bindings: Dict[str, Type] = {}
        self._initialized = True
        self._register_default_repositories()
    
    def _register_default_repositories(self):
        """Register default repository implementations."""
        from infrastructure.repositories.mock_form_repository import MockFormRepository
        from infrastructure.repositories.mock_response_repository import MockResponseRepository
        self._repository_bindings["form_repository"] = MockFormRepository
        self._repository_bindings["response_repository"] = MockResponseRepository
    
    def bind_repository(self, name: str, repository_class: Type) -> None:
        """Bind a repository implementation (for testing or different backends)."""
        self._repository_bindings[name] = repository_class
        if name in self._repositories:
            del self._repositories[name]
    
    def get_repository(self, name: str) -> Any:
        """Get a repository instance by name."""
        if name not in self._repositories:
            repository_class = self._repository_bindings.get(name)
            if repository_class:
                self._repositories[name] = repository_class()
            else:
                raise ValueError(f"Repository {name} not bound")
        return self._repositories[name]
    
    @property
    def form_repository(self) -> FormRepository:
        return self.get_repository("form_repository")
    
    @property
    def response_repository(self) -> ResponseRepository:
        return self.get_repository("response_repository")
    
    def _get_use_case(self, name: str, factory):
        if name not in self._use_cases:
            self._use_cases[name] = factory()
        return self._use_cases[name]
    
    @property
    def get_all_forms_use_case(self):
        from application.use_cases.form_use_cases import GetAllFormsUseCase
        return self._get_use_case("get_all_forms", lambda: GetAllFormsUseCase(self.form_repository))
    
    @property
    def get_form_by_id_use_case(self):
        from application.use_cases.form_use_cases import GetFormByIdUseCase
        return self._get_use_case("get_form_by_id", lambda: GetFormByIdUseCase(self.form_repository))
    
    @property
    def get_forms_by_status_use_case(self):
        from application.use_cases.form_use_cases import GetFormsByStatusUseCase
        return self._get_use_case("get_forms_by_status", lambda: GetFormsByStatusUseCase(self.form_repository))
    
    @property
    def get_form_versions_use_case(self):
        from application.use_cases.form_use_cases import GetFormVersionsUseCase
        return self._get_use_case("get_form_versions", lambda: GetFormVersionsUseCase(self.form_repository))
    
    @property
    def create_form_use_case(self):
        from application.use_cases.form_use_cases import CreateFormUseCase
        return self._get_use_case("create_form", lambda: CreateFormUseCase(self.form_repository))
    
    @property
    def update_form_use_case(self):
        from application.use_cases.form_use_cases import UpdateFormUseCase
        return self._get_use_case("update_form", lambda: UpdateFormUseCase(self.form_repository))
    
    @property
    def delete_form_use_case(self):
        from application.use_cases.form_use_cases import DeleteFormUseCase
        return self._get_use_case("delete_form", lambda: DeleteFormUseCase(self.form_repository))
    
    @property
    def submit_response_use_case(self):
        from application.use_cases.response_use_cases import SubmitResponseUseCase
        return self._get_use_case("submit_response", lambda: SubmitResponseUseCase(self.response_repository, self.form_repository))
    
    @property
    def get_responses_by_form_use_case(self):
        from application.use_cases.response_use_cases import GetResponsesByFormUseCase
        return self._get_use_case("get_responses_by_form", lambda: GetResponsesByFormUseCase(self.response_repository))
    
    @property
    def get_form_analytics_use_case(self):
        from application.use_cases.response_use_cases import GetFormAnalyticsUseCase
        return self._get_use_case("get_form_analytics", lambda: GetFormAnalyticsUseCase(self.response_repository, self.form_repository))

container = Container()