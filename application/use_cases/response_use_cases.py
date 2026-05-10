from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
from domain.entities.response import Response
from domain.repositories.response_repository import ResponseRepository
from domain.repositories.form_repository import FormRepository
from domain.constants import QuestionType

class SubmitResponseUseCase:
    def __init__(self, response_repository: ResponseRepository, form_repository: FormRepository):
        self.response_repository = response_repository
        self.form_repository = form_repository
    
    def execute(self, response: Response, validate_version: bool = False) -> Response:
        form = self.form_repository.get_by_id(response.form_id)
        if not form:
            raise ValueError(f"Form {response.form_id} not found")
        if validate_version and response.form_version != form.version:
            raise ValueError(
                f"Form version mismatch. Expected version {form.version}, "
                f"but got {response.form_version}. Please refresh and try again."
            )
        self._validate_response(response, form)
        response.form_version = form.version
        return self.response_repository.create(response)
   
    def get_form_by_id(self, form_id: str):
        return self.form_repository.get_by_id(form_id)
    
    def _validate_response(self, response: Response, form) -> None:
        question_ids = {q.id for q in form.questions}
        for question in form.questions:
            if question.required:
                if question.id not in response.answers:
                    raise ValueError(f"Required question {question.id} is not answered")
                answer = response.answers[question.id]
                if answer is None or (isinstance(answer, str) and answer.strip() == ""):
                    raise ValueError(f"Required question {question.id} cannot be empty")
        for answer_id in response.answers.keys():
            if answer_id not in question_ids:
                raise ValueError(f"Answer for unknown question {answer_id}")
        for question in form.questions:
            if question.id not in response.answers:
                continue
            answer = response.answers[question.id]
            self._validate_answer_type(question, answer)
            if question.type == QuestionType.MULTIPLE_CHOICE and question.options:
                valid_options = []
                for option_dict in question.options:
                    if isinstance(option_dict, dict):
                        valid_options.append(str(list(option_dict.values())[0]))
                if answer not in valid_options:
                    raise ValueError(f"Answer '{answer}' is not a valid option for question {question.id}")
    
    def _validate_answer_type(self, question, answer) -> None:
        if question.type == QuestionType.BOOLEAN:
            if not isinstance(answer, bool):
                raise ValueError(f"Question {question.id} expects a boolean value")
        elif question.type == QuestionType.DATE:
            if isinstance(answer, str):
                try:
                    datetime.fromisoformat(answer.replace('Z', '+00:00'))
                except ValueError:
                    raise ValueError(f"Question {question.id} expects a valid date string (ISO format)")
            elif not isinstance(answer, (datetime, str)):
                raise ValueError(f"Question {question.id} expects a date value")
        elif question.type == QuestionType.SCALE:
            if question.options:
                scale_range = question.options
                try:
                    scale_value = int(answer) if isinstance(answer, str) else answer
                    min_scale = scale_range[0].get("min", 1) if scale_range else 1
                    max_scale = scale_range[0].get("max", 10) if scale_range else 10
                    if not (min_scale <= scale_value <= max_scale):
                        raise ValueError(f"Question {question.id} expects value between {min_scale} and {max_scale}")
                except (ValueError, TypeError):
                    raise ValueError(f"Question {question.id} expects a numeric scale value")
                

class GetResponsesByFormUseCase:
    def __init__(self, repository: ResponseRepository):
        self.repository = repository

    def execute(self, form_id: str, page: int = 1, page_size: int = 10) -> Tuple[List[Response], int]:
        all_responses = self.repository.get_by_form_id(form_id)
        total = len(all_responses)
        offset = (page - 1) * page_size
        paginated_responses = all_responses[offset:offset + page_size]
        return paginated_responses, total
    
    
class GetFormAnalyticsUseCase:
    def __init__(self, response_repository: ResponseRepository, form_repository: FormRepository):
        self.response_repository = response_repository
        self.form_repository = form_repository

    def execute(self, form_id: str) -> Dict[str, Any]:
        form = self.form_repository.get_by_id(form_id)
        if not form:
            raise ValueError(f"Form {form_id} not found")
        total = self.response_repository.get_total_responses_count(form_id)
        responses = self.response_repository.get_by_form_id(form_id)
        language_counts: Dict[str, int] = {}
        for response in responses:
            lang = response.language
            language_counts[lang] = language_counts.get(lang, 0) + 1
        recent = sorted(responses, key=lambda x: x.submitted_at, reverse=True)[:5]
        return {
            "form_id": form_id,
            "total_responses": total,
            "responses_by_language": language_counts,
            "version": form.version,
            "recent_submissions": [
                {
                    "id": r.id,
                    "submitted_at": r.submitted_at,
                    "language": r.language
                }
                for r in recent
            ]
        }
    
    def get_form_by_id(self, form_id: str):
        return self.form_repository.get_by_id(form_id)