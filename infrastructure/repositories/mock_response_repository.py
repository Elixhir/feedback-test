from typing import List, Dict
from datetime import datetime
from domain.entities.response import Response
from domain.repositories.response_repository import ResponseRepository

class MockResponseRepository(ResponseRepository):
    def __init__(self):
        self.responses: Dict[str, List[Response]] = {}  
    
    def get_by_form_id(self, form_id: str) -> List[Response]:
        """Get all responses for a form."""
        return self.responses.get(form_id, [])
    
    def get_by_form_id_and_date_range(self, form_id: str, start_date: datetime, end_date: datetime) -> List[Response]:
        """Get responses within a date range."""
        responses = self.responses.get(form_id, [])
        return [r for r in responses if start_date <= r.submitted_at <= end_date]
    
    def create(self, response: Response) -> Response:
        """Store a new response."""
        if response.form_id not in self.responses:
            self.responses[response.form_id] = []
        self.responses[response.form_id].append(response)
        return response
    
    def get_total_responses_count(self, form_id: str) -> int:
        """Count total responses for a form."""
        return len(self.responses.get(form_id, []))
    
    def get_responses_by_language(self, form_id: str, language: str) -> List[Response]:
        """Get responses filtered by language."""
        responses = self.responses.get(form_id, [])
        return [r for r in responses if r.language == language]