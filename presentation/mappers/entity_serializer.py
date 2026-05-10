from typing import Dict, Any
from domain.entities.form import Form
from domain.entities.response import Response
class EntitySerializer:
    @staticmethod
    def form_to_dict(form: Form) -> Dict[str, Any]:
        return {
            "id": form.id,
            "title": {lang.value: text for lang, text in form.title.items()},
            "description": {lang.value: text for lang, text in form.description.items()},
            "questions": [EntitySerializer.question_to_dict(q) for q in form.questions],
            "version": form.version,
            "status": form.status,
            "created_at": form.created_at,
            "updated_at": form.updated_at,
            "created_by": form.created_by,
            "updated_by": form.updated_by,
        }
    @staticmethod
    def question_to_dict(question) -> Dict[str, Any]:
        result = {
            "id": question.id,
            "type": question.type.value,
            "text": {lang.value: text for lang, text in question.text.items()},
            "required": question.required,
        }
        if question.options:
            result["options"] = [
                {lang.value: opt for lang, opt in opt_dict.items()}
                for opt_dict in question.options
            ]
        return result
    @staticmethod
    def response_to_dict(response: Response) -> Dict[str, Any]:
        return {
            "id": response.id,
            "form_id": response.form_id,
            "form_version": response.form_version,
            "user_id": response.user_id,
            "answers": response.answers,
            "language": response.language,
            "submitted_at": response.submitted_at,
            "user_agent": response.user_agent,
            "ip_address": response.ip_address,
        }