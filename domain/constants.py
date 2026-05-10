from enum import Enum

class FormStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DRAFT = "draft"

class DefaultUser(str, Enum):
    SYSTEM = "system"
    API = "api"

class Language(str, Enum):
    EN = "en"
    ES = "es"
    FR = "fr"

class QuestionType(str, Enum):
    TEXT = "text"
    MULTIPLE_CHOICE = "multiple_choice"
    RATING = "rating"
    BOOLEAN = "boolean"
    DATE = "date"
    SCALE = "scale"