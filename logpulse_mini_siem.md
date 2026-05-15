# LogPulse Mini SIEM

> A Real-Time Security Information and Event Management (SIEM) system built for logging, monitoring, and analyzing security events efficiently.

## Overview

LogPulse Mini SIEM is a comprehensive log management platform that receives logs from multiple sources, parses severity levels dynamically, and broadcasts events in real-time via WebSocket. It features a complete monitoring stack with Prometheus and Grafana, robust code quality checks via SonarQube, and automated deployments using Jenkins and Docker.

## Features

- **Real-Time Streaming** — WebSocket-based live log feed for instantaneous event visibility.
- **Dynamic Rule Engine** — Automatically evaluates incoming logs to assign severity levels and trigger alerts.
- **Metrics & Observability** — Built-in Prometheus exporter with a pre-configured Grafana dashboard for system analytics.
- **Alerting System** — Integrated Discord Webhook notifications for critical system events.
- **Automated CI/CD** — Jenkins pipeline with integrated SonarQube quality gates.
- **Containerized Architecture** — Optimized Docker deployments with multi-stage builds and health checks.

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python (FastAPI) | Core backend framework and WebSocket server |
| SQLite | Lightweight, persistent log storage |
| Prometheus | Metrics aggregation and alerting |
| Grafana | Real-time monitoring and visualization |
| Jenkins | Continuous Integration & Deployment pipeline |
| SonarQube | Static code analysis and quality gate |
| Docker & Compose | Containerization and orchestration |
| HTML/JS/CSS | Real-time frontend dashboard |

## Architecture & How It Works

LogPulse follows a modular, decoupled architecture optimized for real-time data streaming and observability.

### Core Workflow
1. **Ingestion & Parsing:** The FastAPI backend receives logs via a REST API endpoint. The parser extracts key metadata like the log source and raw message.
2. **Rule Engine:** Logs are passed through a custom Rule Engine (configured via JSON/YAML) to assign a dynamic severity level (e.g., `INFO`, `WARNING`, `ERROR`).
3. **Storage & Broadcasting:** Parsed logs are persistently stored in an SQLite database and immediately broadcasted to all active connected clients via WebSocket.
4. **Metrics Export:** The system tracks the number of logs, active WebSocket clients, and error rates, exposing them on a `/metrics` endpoint.

### System Connections
- **Frontend ↔ Backend:** Bi-directional real-time communication via Native WebSocket.
- **Backend → Database:** Synchronous writes to SQLite for data persistence.
- **Prometheus → Backend:** Prometheus periodically scrapes the `/metrics` endpoint.
- **Grafana → Prometheus:** Grafana queries Prometheus using PromQL to populate the system dashboard.

## Build & Optimization

The deployment lifecycle is highly optimized:
- **Multi-Stage Docker Builds:** Ensures the final production image contains only the compiled application and its runtime dependencies, keeping the image size minimal.
- **`.dockerignore`:** Prevents unnecessary files (like `venv`, `.git`, or tests) from inflating the Docker context.
- **Docker Healthchecks:** Configured to automatically verify the backend's `/health` status, enabling restart policies to handle unexpected crashes.
- **Quality Gates:** Jenkins relies on SonarQube analysis to block deployments if the code contains security vulnerabilities, high duplication, or code smells.

## Getting Started

To run LogPulse locally, you can use the provided Docker Compose configuration.

```bash
# Navigate to the backend directory containing docker-compose.yml
cd head/task1/backend

# Start the full stack (Backend, Prometheus, Grafana, Jenkins, SonarQube)
docker-compose up -d
```

### Manual Backend Setup

If you prefer to run the backend natively for development:

```bash
cd head/task1/backend
python -m venv venv
# On Windows
venv\\Scripts\\activate
# On Linux/Mac
# source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open `head/task4/frontend/index.html` in your browser to view the real-time dashboard.

## Final Result & Public URLs

Once deployed to an Azure VPS, the system becomes publicly accessible across different ports. The platform provides a seamless, unified view of system health and security events.

| Service | Endpoint |
|---------|----------|
| Dashboard | `http://SERVER_IP/` |
| API Health | `http://SERVER_IP/health` |
| Grafana | `http://SERVER_IP:3000` |
| Prometheus | `http://SERVER_IP:9090` |
| Jenkins | `http://SERVER_IP:8080` |
| SonarQube | `http://SERVER_IP:9000` |
