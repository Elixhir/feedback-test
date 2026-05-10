from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime
from domain.constants import Language

@dataclass
class Response:
    id: str
    form_id: str
    answers: Dict[str, Any]
    form_version: int = 1
    user_id: Optional[str] = None
    language: str = Language.EN.value
    submitted_at: datetime = field(default_factory=datetime.utcnow)
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None