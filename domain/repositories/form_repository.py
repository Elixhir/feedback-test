from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.form import Form

class FormRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[Form]:
        """Retrieve all forms."""
        pass
    
    @abstractmethod
    def get_by_id(self, form_id: str) -> Optional[Form]:
        """Retrieve a form by its ID."""
        pass
    
    @abstractmethod
    def get_by_status(self, status: str) -> List[Form]:
        """Retrieve all forms with a specific status (active, archived, draft)."""
        pass
    
    @abstractmethod
    def create(self, form: Form) -> Form:
        """Create a new form."""
        pass
    
    @abstractmethod
    def update(self, form_id: str, form: Form) -> Optional[Form]:
        """Update an existing form."""
        pass
    
    @abstractmethod
    def get_version_history(self, form_id: str) -> List[Form]:
        """Retrieve all versions of a form."""
        pass
    
    @abstractmethod
    def delete(self, form_id: str) -> bool:
        """Delete a form (archive it)."""
        pass