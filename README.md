# Data Analytics API
FastAPI + Pandas + SQLAlchemy service to ingest CSV datasets, validate structured data, persist records, and calculate descriptive statistics.

## Features
- CSV upload with extension, size, empty-file, and header validation.
- SQL persistence through SQLAlchemy; SQLite default and PostgreSQL configurable.
- Pandas numeric summary: count, mean, standard deviation, min, quartiles, median, and max.
- Dataset listing, metadata, bounded preview, and summary endpoints.
- Pydantic response schemas, OpenAPI docs, and pytest tests.

## Setup
Python 3.11+. Create virtual environment, activate it, install requirements, copy .env.example to .env, then run: uvicorn app.main:app --reload.
Open http://127.0.0.1:8000/docs.

## Endpoints
- POST /api/v1/datasets — upload CSV using multipart field named file.
- GET /api/v1/datasets — list datasets.
- GET /api/v1/datasets/{id} — metadata.
- GET /api/v1/datasets/{id}/preview?limit=10 — preview rows.
- GET /api/v1/datasets/{id}/summary — Pandas numeric statistics.
- GET /health — health check.

Example: curl -X POST http://127.0.0.1:8000/api/v1/datasets -F "file=@sample_data/sales.csv"

## Configuration
DATABASE_URL defaults to sqlite:///./analytics.db. PostgreSQL example: postgresql+psycopg://user:password@localhost:5432/analytics. MAX_UPLOAD_BYTES defaults to 5 MB.

## Structure
- app/api/: HTTP route handlers.
- app/core/: environment configuration and SQLAlchemy session.
- app/schemas/: Pydantic response contracts.
- app/services/: CSV parsing and Pandas analytics.
- app/models.py: SQLAlchemy dataset model.
- tests/: API tests and isolated test database.
- sample_data/: sample sales CSV.

## Tests
Run pytest.

## Production considerations
This learning project does not include authentication or per-user dataset isolation. Before production, add auth, quotas, async processing for large files, malware scanning, observability, and data retention policies. Uploaded filenames are metadata only and never used as filesystem paths.
