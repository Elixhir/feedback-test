import uuid
from typing import Dict, List, Optional
from domain.entities.form import Form
from domain.entities.question import Question
from domain.constants import Language, QuestionType, DefaultUser
from presentation.schemas.form_schemas import FormCreateSchema, FormUpdateSchema

class FormMapper:
    _question_counter = 0
    
    @staticmethod
    def _generate_question_id() -> str:
        FormMapper._question_counter += 1
        return f"{FormMapper._question_counter}"

    @staticmethod
    def to_entity_create(schema: FormCreateSchema, form_id: str) -> Form:
        return Form(
            id=form_id,
            title=FormMapper._dict_str_to_language(schema.title),
            description=FormMapper._dict_str_to_language(schema.description),
            questions=[
                Question(
                    id=q.id if q.id else FormMapper._generate_question_id(),
                    type=QuestionType(q.type),
                    text=FormMapper._dict_str_to_language(q.text),
                    options=FormMapper._dict_list_to_language(q.options) if q.options else None,
                    required=q.required
                )
                for q in schema.questions
            ]
        )

    @staticmethod
    def to_entity_update(schema: FormUpdateSchema, existing: Form, form_id: str, updated_by: DefaultUser = DefaultUser.API) -> Form:
        title = FormMapper._dict_str_to_language(schema.title) if schema.title else existing.title
        description = FormMapper._dict_str_to_language(schema.description) if schema.description else existing.description

        if schema.questions is not None:
            questions = [
                Question(
                    id=q.id if q.id else FormMapper._generate_question_id(),
                    type=QuestionType(q.type),
                    text=FormMapper._dict_str_to_language(q.text),
                    options=FormMapper._dict_list_to_language(q.options) if q.options else None,
                    required=q.required
                )
                for q in schema.questions
            ]
        else:
            questions = existing.questions

        return Form(
            id=form_id,
            title=title,
            description=description,
            questions=questions,
            version=existing.version + 1,
            status=existing.status,
            created_at=existing.created_at,
            created_by=existing.created_by,
            updated_by=updated_by.value
        )

    @staticmethod
    def _dict_str_to_language(d: Dict[str, str]) -> Dict[Language, str]:
        result = {}
        for key, value in d.items():
            try:
                result[Language(key)] = value
            except ValueError:
                result[Language.EN] = value
        return result

    @staticmethod
    def _dict_list_to_language(d: Optional[List[Dict[str, str]]]) -> Optional[List[Dict[Language, str]]]:
        if d is None:
            return None
        result = []
        for item in d:
            mapped = {}
            for key, value in item.items():
                try:
                    mapped[Language(key)] = value
                except ValueError:
                    mapped[Language.EN] = value
            result.append(mapped)
        return result