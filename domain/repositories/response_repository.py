from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from domain.entities.response import Response

class ResponseRepository(ABC):

    @abstractmethod
    def get_by_form_id(self, form_id: str) -> List[Response]:
        """Retrieve all responses for a specific form."""
        pass
    
    @abstractmethod
    def get_by_form_id_and_date_range(self, form_id: str, start_date: datetime, end_date: datetime) -> List[Response]:
        """Retrieve responses for a form within a date range."""
        pass
    
    @abstractmethod
    def create(self, response: Response) -> Response:
        """Store a new response submission."""
        pass
    
    @abstractmethod
    def get_total_responses_count(self, form_id: str) -> int:
        """Count total responses for a form."""
        pass
    
    @abstractmethod
    def get_responses_by_language(self, form_id: str, language: str) -> List[Response]:
        """Get responses filtered by language."""
        pass