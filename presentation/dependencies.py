from functools import lru_cache

@lru_cache()

def get_container():
    from application.container import container
    return container

def get_form_use_cases(container=None):
    if container is None:
        container = get_container()
    from application.use_cases.form_use_cases import (
        GetAllFormsUseCase,
        GetFormByIdUseCase,
        GetFormsByStatusUseCase,
        GetFormVersionsUseCase,
        CreateFormUseCase,
        UpdateFormUseCase,
        DeleteFormUseCase,
    )
    return {
        "get_all": container.get_all_forms_use_case,
        "get_by_id": container.get_form_by_id_use_case,
        "get_by_status": container.get_forms_by_status_use_case,
        "get_versions": container.get_form_versions_use_case,
        "create": container.create_form_use_case,
        "update": container.update_form_use_case,
        "delete": container.delete_form_use_case,
    }

def get_response_use_cases(container=None):
    if container is None:
        container = get_container()
    from application.use_cases.response_use_cases import (
        SubmitResponseUseCase,
        GetResponsesByFormUseCase,
        GetFormAnalyticsUseCase,
    )
    return {
        "submit": container.submit_response_use_case,
        "get_by_form": container.get_responses_by_form_use_case,
        "analytics": container.get_form_analytics_use_case,
    }