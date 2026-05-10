from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
from domain.constants import Language
from domain.entities.question import Question
from domain.constants import FormStatus

@dataclass
class Form:
    id: str
    title: Dict[Language, str]
    description: Dict[Language, str]
    questions: List[Question]
    version: int = 1
    status: str = FormStatus.ACTIVE.value
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None
    updated_by: Optional[str] = None