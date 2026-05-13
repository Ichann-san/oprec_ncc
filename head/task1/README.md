# Task 1 — Backend (FastAPI + WebSocket + Metrics)

## Overview
The LogPulse backend is built with **FastAPI** and provides:
- Health check endpoint
- Log ingestion with rule-based severity classification
- Real-time WebSocket broadcasting
- Prometheus-compatible metrics endpoint
- SQLite storage for persistent log events

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check — returns status + timestamp |
| POST | `/logs` | Ingest a log message |
| GET | `/logs` | Search/filter stored logs |
| WS | `/ws` | WebSocket real-time log stream |
| GET | `/metrics` | Prometheus text exposition metrics |
| GET | `/stats` | JSON metrics summary |

## POST /logs Request Body
```json
{
    "message": "Database connection failed - timeout",
    "source": "backend-api"
}
```

## Rule Engine
Rules are defined in `app/rules/rules.json`. Each rule maps a keyword to a severity level. When a log message matches a rule keyword, the system:
1. Assigns the matched severity
2. Increments alert counters
3. Broadcasts an alert via WebSocket
4. Optionally sends a Discord notification

## Project Structure
```
backend/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── routes/
│   │   ├── health.py        # GET /health
│   │   ├── logs.py          # POST/GET /logs
│   │   └── websocket.py     # WS /ws
│   ├── services/
│   │   ├── parser_service.py    # Log parser + rule engine
│   │   ├── metrics_service.py   # Prometheus metrics
│   │   └── websocket_service.py # WS connection manager
│   ├── models/
│   │   └── log_model.py     # Pydantic schemas
│   ├── database/
│   │   └── sqlite.py        # SQLite operations
│   └── rules/
│       └── rules.json       # Rule definitions
└── requirements.txt
```

## How to Run
```bash
cd head/task1/backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
