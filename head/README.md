# LogPulse Mini SIEM

> Real-time log monitoring and security event management system

## Overview
LogPulse is a Mini SIEM (Security Information and Event Management) system that receives logs, parses severity levels, broadcasts events in real-time via WebSocket, stores events in a database, exposes metrics for Prometheus, and visualizes data in Grafana.

## Architecture
```
Client Browser
    |
    v
Frontend Dashboard (HTML + JS + CSS)
    |
    v
WebSocket Connection
    |
    v
FastAPI Backend
    |
    +---- Log Parser + Rule Engine
    |
    +---- SQLite Database
    |
    +---- Metrics Exporter → Prometheus → Grafana
    |
    +---- Alert System → Discord Webhook
    |
    +---- Jenkins CI/CD → SonarQube
    |
    v
Docker Container → Azure VPS
```

## Project Structure

| Folder | Description |
|--------|-------------|
| `task1/` | Backend (FastAPI + WebSocket + Metrics + Docker) |
| `task2/` | CI/CD (Jenkins + SonarQube) |
| `task3/` | Monitoring (Prometheus + Grafana + Alerts) |
| `task4/` | Frontend Dashboard + Sample Logs |
| `docs/` | Architecture & deployment documentation |

## Quick Start

### 1. Backend
```bash
cd head/task1/backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 2. Frontend
Open `head/task4/frontend/index.html` in a browser and connect to `ws://localhost:8000/ws`.

### 3. Test Log Ingestion
```bash
curl -X POST http://localhost:8000/logs \
  -H "Content-Type: application/json" \
  -d '{"message": "User login failed", "source": "auth"}'
```

### 4. Docker Compose (Full Stack)
```bash
cd head/task1/backend
docker-compose up -d
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/logs` | Ingest log |
| GET | `/logs` | Search logs |
| WS | `/ws` | Real-time stream |
| GET | `/metrics` | Prometheus metrics |
| GET | `/stats` | JSON stats |

## Public URLs (After Deployment)

| Service | URL |
|---------|-----|
| Dashboard | `http://SERVER_IP/` |
| Backend Health | `http://SERVER_IP/health` |
| Grafana | `http://SERVER_IP:3000` |
| Prometheus | `http://SERVER_IP:9090` |
| Jenkins | `http://SERVER_IP:8080` |
| SonarQube | `http://SERVER_IP:9000` |

## Tech Stack
- **Backend**: Python FastAPI
- **Realtime**: Native WebSocket (FastAPI)
- **Database**: SQLite
- **Monitoring**: Prometheus + Grafana
- **CI/CD**: Jenkins + SonarQube
- **Container**: Docker + Docker Compose
- **Reverse Proxy**: Nginx
- **Deployment**: Azure VPS (Ubuntu)
