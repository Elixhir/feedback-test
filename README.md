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

## Contratos de API por Consumidor

### 🖥️ Backoffice (Admin)

Administración de formularios y visualización de respuestas.

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/forms` | Listar formularios (paginado, filtrar por status) |
| GET | `/api/v1/forms?form_id={id}` | Obtener formulario por ID |
| GET | `/api/v1/forms?form_id={id}&versions=true` | Ver historial de versiones |
| POST | `/api/v1/forms` | Crear formulario |
| PUT | `/api/v1/forms/{form_id}` | Actualizar formulario |
| DELETE | `/api/v1/forms/{form_id}` | Archivar formulario |
| GET | `/api/v1/responses/{form_id}` | Ver respuestas de un formulario |
| GET | `/api/v1/responses/{form_id}/analytics` | Ver analytics |

### App Web/Mobile (Usuario Final)

Envío de respuestas a formularios.

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/forms?status=active` | Listar formularios activos |
| GET | `/api/v1/forms?form_id={id}` | Obtener detalles de formulario |
| POST | `/api/v1/responses` | Enviar respuesta |

### System

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información de la API |
| GET | `/health` | Health check |

---

## Ejemplos de Uso

### Health Check
```bash
curl http://localhost:8000/health
```

### Listar formularios activos (App)
```bash
curl "http://localhost:8000/api/v1/forms?status=active"
```

### Obtener formulario (App)
```bash
curl "http://localhost:8000/api/v1/forms?form_id=form123"
```

### Crear formulario (Backoffice)
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

### Actualizar formulario (Backoffice)
```bash
curl -X PUT "http://localhost:8000/api/v1/forms/form123" \
  -H "Content-Type: application/json" \
  -d '{"title": {"en": "Updated Form"}}'
```

### Archivar formulario (Backoffice)
```bash
curl -X DELETE "http://localhost:8000/api/v1/forms/form123"
```

### Enviar respuesta (App)
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

### Ver respuestas (Backoffice)
```bash
curl "http://localhost:8000/api/v1/responses/form123"
```

### Ver analytics (Backoffice)
```bash
curl "http://localhost:8000/api/v1/responses/form123/analytics"
```

---

## Parámetros

### Paginación
| Parámetro | Default | Máximo | Descripción |
|-----------|---------|--------|-------------|
| `page` | 1 | - | Página número |
| `page_size` | 10 | 100 | Items por página |

### Query Params para Forms
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `page` | int | Número de página |
| `page_size` | int | Items por página |
| `status` | string | Filtrar: active, archived, draft |
| `form_id` | string | Obtener formulario específico |
| `versions` | bool | true = devolver todas las versiones |

---

## Tipos de Pregunta Soportados

- `text` - Texto libre
- `multiple_choice` - Opción única
- `rating` - Rating numérico
- `boolean` - True/False
- `date` - Fecha
- `scale` - Valor numérico en rango

---

## Estados de Formulario

- `active` - Formulario disponible
- `archived` - Formulario archivado
- `draft` - Borrador

---

## Idiomas Soportados

- `en` - English
- `es` - Spanish
- `fr` - French