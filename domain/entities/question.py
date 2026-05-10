from dataclasses import dataclass, field
from typing import Dict, List, Optional
from domain.constants import Language, QuestionType

@dataclass
class Question:
    id: str
    type: QuestionType
    text: Dict[Language, str]
    options: Optional[List[Dict[Language, str]]] = None
    required: bool = True