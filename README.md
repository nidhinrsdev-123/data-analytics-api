# Data Analytics API

A FastAPI service that accepts CSV datasets, validates their structure, stores records in SQL, and uses **Pandas** to calculate numeric summary statistics.

## Features
- CSV upload through a multipart form field named file.
- File extension, maximum size, empty-file, and duplicate/blank header checks.
- SQLAlchemy persistence; SQLite by default and PostgreSQL configurable.
- Dataset listing and metadata retrieval.
- Bounded row preview (1–100 rows).
- Pandas numeric summary: count, mean, standard deviation, minimum, quartiles, median, and maximum.
- Pydantic response schemas and interactive OpenAPI documentation.
- pytest API tests using an isolated in-memory SQLite database.

## Technology
Python 3.11+, FastAPI, Uvicorn, Pandas, SQLAlchemy 2, SQLite/PostgreSQL, pytest, and HTTPX.

## Exact repository structure

This tree matches the files currently committed to GitHub. Inline comments explain the purpose of each folder and file.

```text
data-analytics-api/
├── .env.example  # Template for environment variables
├── .github/  # GitHub automation and repository workflows
│   └── workflows/  # Continuous integration workflows
│       └── tests.yml  # Runs automated tests on pushes and pull requests
├── .gitignore  # Files Git should ignore
├── LICENSE  # Project license
├── README.md  # Project overview, setup guide and API documentation
├── app/  # Main FastAPI application package
│   ├── __init__.py  # Marks app as a Python package
│   ├── api/  # HTTP API layer
│   │   ├── __init__.py  # Marks api as a Python package
│   │   └── routes.py  # Defines dataset upload, listing, preview and summary endpoints
│   ├── core/  # Shared configuration and infrastructure
│   │   ├── __init__.py  # Marks core as a Python package
│   │   ├── config.py  # Loads application settings and environment variables
│   │   └── database.py  # Configures SQLAlchemy engine and sessions
│   ├── main.py  # Creates the FastAPI application and startup routes
│   ├── models.py  # Defines SQLAlchemy database models
│   ├── schemas/  # Pydantic request and response schemas
│   │   ├── __init__.py  # Marks schemas as a Python package
│   │   └── datasets.py  # Defines dataset validation and response schemas
│   └── services/  # Reusable business and data-processing logic
│       ├── __init__.py  # Marks services as a Python package
│       └── analytics.py  # Validates CSV data and calculates Pandas statistics
├── requirements.txt  # Lists required Python packages
├── sample_data/  # Example input files
│   └── sales.csv  # Sample sales dataset for upload and analysis
└── tests/  # Automated API tests
    ├── conftest.py  # Configures shared fixtures and an isolated test database
    └── test_api.py  # Tests health, upload, preview, summary and error responses
```
## Step-by-step: run locally (Windows)

### 1. Install Python
Install Python 3.11 or newer and verify:

~~~powershell
py --version
~~~

### 2. Clone the repository

~~~powershell
git clone https://github.com/nidhinrsdev-123/data-analytics-api.git
cd data-analytics-api
~~~

### 3. Create and activate a virtual environment

~~~powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
~~~

If PowerShell blocks activation, use Command Prompt:

~~~bat
.venv\Scripts\activate.bat
~~~

### 4. Install dependencies

~~~powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
~~~

### 5. Configure the database

**Quick start with SQLite:** No configuration is required. The app defaults to sqlite:///./analytics.db.

**Use PostgreSQL:** Create a database, then copy the example environment file:

~~~powershell
Copy-Item .env.example .env
~~~

Edit DATABASE_URL in .env. Example:

~~~text
DATABASE_URL=postgresql+psycopg://analytics_user:your_password@localhost:5432/analytics
~~~

MAX_UPLOAD_BYTES defaults to 5,000,000 bytes (5 MB). Do not commit .env or credentials.

### 6. Start the FastAPI server

From the repository root:

~~~powershell
uvicorn app.main:app --reload
~~~

The app creates its database tables when it starts.

Open:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health check: http://127.0.0.1:8000/health

Stop with Ctrl+C.

## Try the API

### 1. Upload the included sample CSV

With the server running, open a second PowerShell window in the project folder:

~~~powershell
curl.exe -X POST "http://127.0.0.1:8000/api/v1/datasets" -F "file=@sample_data/sales.csv"
~~~

Copy the dataset id from the response.

Alternatively, open /docs, expand POST /api/v1/datasets, select Try it out, choose a CSV file for file, and click Execute.

### 2. List datasets

~~~powershell
curl.exe "http://127.0.0.1:8000/api/v1/datasets"
~~~

### 3. Preview a dataset

Replace 1 with the ID returned by upload:

~~~powershell
curl.exe "http://127.0.0.1:8000/api/v1/datasets/1/preview?limit=10"
~~~

### 4. Get numeric statistics

~~~powershell
curl.exe "http://127.0.0.1:8000/api/v1/datasets/1/summary"
~~~

### 5. Get dataset metadata

~~~powershell
curl.exe "http://127.0.0.1:8000/api/v1/datasets/1"
~~~

## API reference

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /health | Health check |
| POST | /api/v1/datasets | Upload a CSV |
| GET | /api/v1/datasets | List datasets |
| GET | /api/v1/datasets/{id} | Dataset metadata |
| GET | /api/v1/datasets/{id}/preview?limit=10 | Preview rows |
| GET | /api/v1/datasets/{id}/summary | Numeric statistics |

Preview limit must be between 1 and 100. Uploads must be .csv files within the configured size limit and contain at least one data row.

## Run tests

From the repository root:

~~~powershell
pytest
~~~

The test fixture creates a separate in-memory SQLite database for each test. Tests cover health, CSV upload, preview, Pandas summary, invalid file type, and missing dataset behavior.

## Code explanation
- app/main.py: creates the FastAPI app, database tables, and health endpoint.
- app/api/routes.py: HTTP endpoints and database dependency.
- app/core/config.py: environment-based configuration.
- app/core/database.py: SQLAlchemy engine, session factory, and declarative base.
- app/models.py: SQLAlchemy Dataset table.
- app/schemas/datasets.py: Pydantic response schemas.
- app/services/analytics.py: CSV validation/parsing and Pandas summary calculations.
- tests/conftest.py: isolated test database and dependency override.
- tests/test_api.py: API tests.
- sample_data/sales.csv: sample dataset for upload and analytics.

## Limitations and production considerations
This learning project does not include authentication, per-user dataset isolation, or asynchronous processing for large datasets. Dataset records are stored as JSON in the SQL database. Before production, add authentication and authorization, upload quotas, robust schema/data-type policies, background processing, observability, and retention controls. Uploaded filenames are stored as metadata and are not used as filesystem paths.
