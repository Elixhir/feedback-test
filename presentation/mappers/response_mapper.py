from domain.entities.response import Response
from presentation.schemas.response_schemas import ResponseCreateSchema
class ResponseMapper:
    @staticmethod
    def to_entity_create(
        schema: ResponseCreateSchema,
        response_id: str,
        user_agent: str = None,
        ip_address: str = None
    ) -> Response:
        return Response(
            id=response_id,
            form_id=schema.form_id,
            answers=schema.answers,
            user_id=schema.user_id,
            language=schema.language,
            user_agent=user_agent,
            ip_address=ip_address
        )