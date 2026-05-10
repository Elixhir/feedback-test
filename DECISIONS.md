# Design Decisions

## 1. Clean Architecture

**Decision:** Layered architecture (domain, application, infrastructure, presentation)

**Justification:**
- Allows changing implementations (DB, frameworks) without affecting business logic
- Facilitates unit testing
- Clear separation of responsibilities

**Alternative considered:** Simple MVC structure - rejected due to lower scalability

---

## 2. Domain Entities Without Pydantic

**Decision:** Use Python `dataclasses` in domain, Pydantic only in presentation

**Justification:**
- Domain should be independent of external frameworks
- Pydantic is for input/output validation, not business logic
- Maintains clean architecture

---

## 3. Form Versioning

**Decision:** Each update creates a new version, history is preserved

**Justification:**
- Traceability: I can see how a form evolved
- Consistency: submitted responses always reference a specific version
- Rollback: ability to revert to previous versions if errors occur

**Alternative:** Only store current version - rejected because it loses history

---

## 4. Languages as Enum + Dictionaries

**Decision:**
- `Language` is an Enum (EN, ES, FR)
- Texts are stored as `Dict[Language, str]`

**Justification:**
- Type safety: I can't accidentally use an invalid language
- Extensible: adding a new language = adding to the enum
- Fast lookup by language

**How to add more languages?**
1. Add to `Language` enum in `domain/constants.py`:
   ```python
   class Language(str, Enum):
       EN = "en"
       ES = "es"
       FR = "fr"
       DE = "de"  # New language
       PT = "pt"  # Another new one
   ```
2. The system automatically accepts that language in all endpoints

---

## 5. Extensible Question Types

**Decision:** QuestionType as Enum with answer type validation

**Justification:**
- Adding a new question type = adding to the enum
- Type-specific validation (boolean, date, scale, etc.)
- Type safety at development time

**Current types:**
- TEXT - free response
- MULTIPLE_CHOICE - single choice from list
- RATING - numeric rating
- BOOLEAN - true/false
- DATE - date
- SCALE - numeric value in range

---

## 6. DI Container as Singleton

**Decision:** Single Container instantiated as singleton

**Justification:**
- Prevents creating multiple repository instances
- Makes testing easier: I can replace implementations
- Performance: connection reuse

**For testing:**
```python
# Replace implementation
container.bind_repository("form_repository", MockFormRepository)
```

---

## 7. Mappers in Presentation Layer

**Decision:** Mappers convert schema <-> entity in presentation/, not in application/

**Justification:**
- Application layer should not know about presentation (avoids cycles)
- Use cases receive and return domain entities
- Routers are responsible for translation

---

## 8. Pagination on All List Endpoints

**Decision:** `page` and `page_size` parameters with standardized response

**Justification:**
- Scalability: doesn't return all records
- UX: frontend can paginate
- Standardized: same structure on all endpoints

---

## 9. Response Validation in Use Case

**Decision:** Validation happens in SubmitResponseUseCase, not in schemas

**Justification:**
- Validation rules are business logic, not input validation
- Schemas only validate format (types, required)
- Use case validates semantics (required questions, valid options, etc.)

---

## 10. Mock Data Separated

**Decision:** Initial data in `infrastructure/data/`, not in the repository

**Justification:**
- Separates configuration from implementation
- Easy to replace for testing
- Cleaner repository code
