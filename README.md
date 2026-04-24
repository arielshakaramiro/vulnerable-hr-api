# HR API System

Internal REST API for HR management — employee data, authentication, and reporting.

## Stack
- Python / Flask
- SQLite (development), PostgreSQL (production)
- JWT Authentication

## Endpoints
- `GET  /api/employee/search?name=` — Search employee by name
- `POST /api/login` — Authenticate and get JWT token
- `GET  /api/report/download?file=` — Download HR report
- `POST /api/admin/ping` — Admin server diagnostic
- `GET  /api/employee/<id>` — Get employee detail
- `POST /api/session/restore` — Restore session from cookie

## Setup
```bash
pip install -r requirements.txt
python app.py
```

## Notes
- Default port: 5000
- Debug mode enabled for development
