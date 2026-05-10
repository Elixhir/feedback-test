# Flexible Multi-Language Feedback Form System

REST API for managing multilingual feedback forms with versioning and analytics support.

## Requirements

- Python 3.12+
- FastAPI
- Pydantic

## Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd feedback-test
```

2. Create virtual environment (optional):
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running

Start the server:
```bash
uvicorn app:app --reload
```

API available at: `http://localhost:8000`

Auto-generated docs: `http://localhost:8000/docs`

---

## API Contracts by Consumer

### 🖥️ Backoffice (Admin)

Form administration and response visualization.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/forms` | List forms (paginated, filter by status) |
| GET | `/api/v1/forms?form_id={id}` | Get form by ID |
| GET | `/api/v1/forms?form_id={id}&versions=true` | View version history |
| POST | `/api/v1/forms` | Create form |
| PUT | `/api/v1/forms/{form_id}` | Update form |
| DELETE | `/api/v1/forms/{form_id}` | Archive form |
| GET | `/api/v1/responses/{form_id}` | View form responses |
| GET | `/api/v1/responses/{form_id}/analytics` | View analytics |

### 📱 App Web/Mobile (End User)

Response submission to forms.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/forms?status=active` | List active forms |
| GET | `/api/v1/forms?form_id={id}` | Get form details |
| POST | `/api/v1/responses` | Submit response |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |

---

## Usage Examples

### Health Check
```bash
curl http://localhost:8000/health
```

### List active forms (App)
```bash
curl "http://localhost:8000/api/v1/forms?status=active"
```

### Get form (App)
```bash
curl "http://localhost:8000/api/v1/forms?form_id=form123"
```

### Create form (Backoffice)
```bash
curl -X POST "http://localhost:8000/api/v1/forms" \
  -H "Content-Type: application/json" \
  -d '{
    "title": {"en": "Customer Feedback"},
    "description": {"en": "Help us improve"},
    "questions": [
      {
        "id": "q1",
        "type": "text",
        "text": {"en": "How was your experience?"},
        "required": true
      }
    ]
  }'
```

### Update form (Backoffice)
```bash
curl -X PUT "http://localhost:8000/api/v1/forms/form123" \
  -H "Content-Type: application/json" \
  -d '{"title": {"en": "Updated Form"}}'
```

### Archive form (Backoffice)
```bash
curl -X DELETE "http://localhost:8000/api/v1/forms/form123"
```

### Submit response (App)
```bash
curl -X POST "http://localhost:8000/api/v1/responses" \
  -H "Content-Type: application/json" \
  -d '{
    "form_id": "form123",
    "user_id": "user456",
    "language": "en",
    "answers": {"q1": "Great service!"}
  }'
```

### View responses (Backoffice)
```bash
curl "http://localhost:8000/api/v1/responses/form123"
```

### View analytics (Backoffice)
```bash
curl "http://localhost:8000/api/v1/responses/form123/analytics"
```

---

## Parameters

### Pagination
| Parameter | Default | Max | Description |
|-----------|---------|-----|-------------|
| `page` | 1 | - | Page number |
| `page_size` | 10 | 100 | Items per page |

### Query Params for Forms
| Parameter | Type | Description |
|-----------|------|-------------|
| `page` | int | Page number |
| `page_size` | int | Items per page |
| `status` | string | Filter: active, archived, draft |
| `form_id` | string | Get specific form |
| `versions` | bool | true = return all versions |

---

## Supported Question Types

- `text` - Free text
- `multiple_choice` - Single choice
- `rating` - Numeric rating
- `boolean` - True/False
- `date` - Date
- `scale` - Numeric value in range

---

## Form Status

- `active` - Form available
- `archived` - Form archived
- `draft` - Draft

---

## Supported Languages

- `en` - English
- `es` - Spanish
- `fr` - French