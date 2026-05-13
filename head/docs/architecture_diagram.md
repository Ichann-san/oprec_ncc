========================================================
LOGPULSE MINI SIEM — HEAD DOCUMENTATION
Complete Project Architecture & Workflow
========================================================

TABLE OF CONTENTS
--------------------------------------------------------
1. Project Overview
2. System Architecture
3. Component Map
4. Data Flow
5. Docker Network Topology
6. Port Mapping
7. Task Breakdown & Connections
8. Directory Structure
9. Configuration Quick Reference
10. How Everything Connects

========================================================
1. PROJECT OVERVIEW
========================================================

LogPulse Mini SIEM is a real-time security information
and event management system that:

  - Receives log events from applications/users
  - Parses severity using a keyword-based rule engine
  - Stores events persistently in SQLite
  - Broadcasts events in real-time via WebSocket
  - Exposes Prometheus-compatible metrics
  - Visualizes metrics in Grafana dashboards
  - Automates build/deploy via Jenkins CI/CD
  - Validates code quality via SonarQube
  - Deploys to Azure VPS with Nginx reverse proxy

Tech Stack:
  Backend       → Python FastAPI
  Realtime      → Native WebSocket (FastAPI)
  Database      → SQLite (aiosqlite)
  Monitoring    → Prometheus + Grafana
  CI/CD         → Jenkins + SonarQube
  Container     → Docker + Docker Compose
  Reverse Proxy → Nginx
  Deployment    → Azure VPS (Ubuntu)

========================================================
2. SYSTEM ARCHITECTURE
========================================================

                    ┌─────────────────────┐
                    │   Client Browser    │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Nginx (port 80)   │
                    │   Reverse Proxy     │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
     ┌────────▼───────┐  ┌────▼────┐  ┌────────▼───────┐
     │ Static Files   │  │ API     │  │ WebSocket      │
     │ (Frontend)     │  │ Routes  │  │ /ws            │
     │ index.html     │  │ /logs   │  │ (upgrade)      │
     └────────────────┘  │ /health │  └────────┬───────┘
                         │ /metrics│           │
                         └────┬────┘           │
                              │                │
                    ┌─────────▼────────────────▼┐
                    │     FastAPI Backend        │
                    │     (port 8000)            │
                    │                            │
                    │  ┌──────────────────────┐  │
                    │  │ Log Parser            │  │
                    │  │ + Rule Engine         │  │
                    │  └──────────┬───────────┘  │
                    │             │               │
                    │  ┌──────────▼───────────┐  │
                    │  │ Services Layer        │  │
                    │  │ ├─ parser_service     │  │
                    │  │ ├─ metrics_service    │  │
                    │  │ └─ websocket_service  │  │
                    │  └──────────┬───────────┘  │
                    │             │               │
                    │  ┌──────────▼───────────┐  │
                    │  │ SQLite Database       │  │
                    │  │ logpulse.db           │  │
                    │  └──────────────────────┘  │
                    └──────────────┬──────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │ Prometheus (port 9090)      │
                    │ Scrapes /metrics every 10s  │
                    │ Evaluates alert_rules.yml   │
                    └─────────────┬──────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │ Grafana (port 3000)         │
                    │ 8-panel dashboard           │
                    │ PromQL queries              │
                    └────────────────────────────┘

  Parallel Systems:
  ┌──────────────────────┐  ┌──────────────────────┐
  │ Jenkins (port 8080)  │  │ SonarQube (port 9000)│
  │ CI/CD Pipeline       │  │ Code Quality         │
  │ 8-stage Jenkinsfile  │  │ Quality Gate         │
  └──────────────────────┘  └──────────────────────┘

========================================================
3. COMPONENT MAP
========================================================

Task 1 — Backend + Docker + Nginx
  Purpose: Core application, containerization, reverse proxy
  Contains:
    - FastAPI application (app/)
    - Dockerfile (multi-stage build)
    - docker-compose.yml (all 5 services)
    - Nginx reverse proxy config
  Connects to: Task 3 (metrics), Task 4 (WebSocket)

Task 2 — CI/CD (Jenkins + SonarQube)
  Purpose: Automated build, test, analyze, deploy pipeline
  Contains:
    - Jenkinsfile (8 stages)
    - SonarQube scanner config
    - Build/Test/Deploy shell scripts
  Connects to: Task 1 (builds & deploys it)

Task 3 — Monitoring (Prometheus + Grafana + Alerting)
  Purpose: Collect metrics, visualize, alert
  Contains:
    - Prometheus scrape & alert config
    - Grafana dashboard JSON + provisioning
    - Discord webhook alert documentation
  Connects to: Task 1 (scrapes /metrics endpoint)

Task 4 — Frontend Dashboard + WebSocket
  Purpose: Real-time log visualization
  Contains:
    - HTML/CSS/JS dashboard
    - WebSocket client
    - Sample log files
  Connects to: Task 1 (via WebSocket /ws)

========================================================
4. DATA FLOW
========================================================

INGESTION FLOW:
  1. User/App sends POST /logs with message + source
  2. Nginx receives on port 80, proxies to backend:8000
  3. FastAPI /logs endpoint receives the request
  4. parser_service.py parses the message
  5. Rule engine matches keywords → assigns severity
  6. Log event stored in SQLite (database/sqlite.py)
  7. Metrics updated (metrics_service.py)
  8. Event broadcast to all WS clients (websocket_service.py)
  9. If ERROR → Discord webhook notification sent

MONITORING FLOW:
  1. Prometheus scrapes GET /metrics every 10 seconds
  2. Metrics stored in Prometheus time-series DB
  3. Alert rules evaluated every 15 seconds
  4. Grafana queries Prometheus via PromQL
  5. Dashboard auto-refreshes every 10 seconds
  6. If threshold exceeded → alert fires

CI/CD FLOW:
  1. Developer pushes code to GitHub
  2. GitHub webhook triggers Jenkins pipeline
  3. Jenkins: install deps → run tests → SonarQube scan
  4. Quality gate checked → pass or fail
  5. Docker image built → containers deployed
  6. Health check verifies deployment

REALTIME FLOW:
  1. Browser opens index.html
  2. JavaScript connects WebSocket to ws://SERVER_IP/ws
  3. Nginx upgrades HTTP to WebSocket protocol
  4. Backend registers client in WebSocketManager
  5. When new log arrives, backend broadcasts to all clients
  6. Browser renders log entry with severity badge
  7. Counters and filters update in real-time

========================================================
5. DOCKER NETWORK TOPOLOGY
========================================================

  Docker Network: logpulse-net (bridge)
  ┌─────────────────────────────────────────────┐
  │                                             │
  │  ┌─────────────┐    ┌──────────────────┐    │
  │  │ backend     │    │ prometheus       │    │
  │  │ :8000       │◄───│ :9090            │    │
  │  └─────────────┘    │ scrapes /metrics │    │
  │                     └────────┬─────────┘    │
  │                              │              │
  │                     ┌────────▼─────────┐    │
  │                     │ grafana          │    │
  │                     │ :3000            │    │
  │                     └──────────────────┘    │
  │                                             │
  │  ┌─────────────┐    ┌──────────────────┐    │
  │  │ sonarqube   │    │ jenkins          │    │
  │  │ :9000       │    │ :8080            │    │
  │  └─────────────┘    └──────────────────┘    │
  │                                             │
  └─────────────────────────────────────────────┘

  All containers communicate via Docker DNS:
    - prometheus → backend:8000
    - grafana → prometheus:9090
    - jenkins → sonarqube:9000

========================================================
6. PORT MAPPING
========================================================

  Port  │ Service     │ Purpose
  ──────┼─────────────┼──────────────────────────
  80    │ Nginx       │ Reverse proxy (public entry)
  8000  │ Backend     │ FastAPI application
  9090  │ Prometheus  │ Metrics collection
  3000  │ Grafana     │ Dashboard visualization
  8080  │ Jenkins     │ CI/CD pipeline
  9000  │ SonarQube   │ Code quality analysis
  50000 │ Jenkins     │ Agent communication

========================================================
7. TASK BREAKDOWN & CONNECTIONS
========================================================

  Task 1 (Backend)
    │
    ├──► Task 3 (Prometheus scrapes /metrics)
    │
    ├──► Task 4 (Frontend connects via /ws)
    │
    └──► Task 2 (Jenkins builds & deploys Task 1)
              │
              └──► SonarQube (analyzes Task 1 code)

  All tasks are deployed together via:
    docker-compose.yml (in task1/backend/)

========================================================
8. DIRECTORY STRUCTURE
========================================================

  head/
  │
  ├── task1/                    ← Backend + Docker + Nginx
  │   ├── backend/
  │   │   ├── app/
  │   │   │   ├── main.py
  │   │   │   ├── routes/       (health, logs, websocket)
  │   │   │   ├── services/     (parser, metrics, websocket)
  │   │   │   ├── models/       (log_model)
  │   │   │   ├── database/     (sqlite)
  │   │   │   └── rules/        (rules.json)
  │   │   ├── Dockerfile
  │   │   ├── docker-compose.yml
  │   │   ├── .dockerignore
  │   │   ├── .env
  │   │   └── requirements.txt
  │   ├── nginx/
  │   │   └── nginx.conf
  │   └── README.md
  │
  ├── task2/                    ← CI/CD
  │   ├── jenkins/
  │   │   ├── Jenkinsfile
  │   │   └── pipeline/         (stage docs)
  │   ├── sonarqube/
  │   │   └── sonar-project.properties
  │   ├── scripts/              (build, test, deploy)
  │   └── README.md
  │
  ├── task3/                    ← Monitoring
  │   ├── prometheus/
  │   │   ├── prometheus.yml
  │   │   └── alert_rules.yml
  │   ├── grafana/
  │   │   ├── dashboards/       (system_dashboard.json)
  │   │   └── provisioning/     (datasources, dashboards)
  │   ├── alerts/
  │   │   └── discord_webhook.txt
  │   └── README.md
  │
  ├── task4/                    ← Frontend
  │   ├── frontend/             (index.html, style.css, app.js)
  │   ├── sample_logs/          (app.log, system.log)
  │   ├── websocket_flow/       (architecture.txt)
  │   └── README.md
  │
  ├── docs/                     ← Documentation
  │   ├── architecture_diagram.txt  (this file — HEAD doc)
  │   ├── deployment_guide.txt      (Task 1 doc)
  │   ├── ci_cd_guide.txt           (Task 2 doc)
  │   ├── monitoring_guide.txt      (Task 3 doc)
  │   └── frontend_guide.txt        (Task 4 doc)
  │
  └── README.md

========================================================
9. CONFIGURATION QUICK REFERENCE
========================================================

  Backend (.env):
    LOGPULSE_DB_PATH=/app/data/logpulse.db
    DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/1440483607456882699/iF8bC7o2K8_o92L0yWk05243K94d79hH6qR5p0L44oG8sN9lP2eD4oD2qG3o0u7D8nE
    GRAFANA_ADMIN_USER=admin
    GRAFANA_ADMIN_PASSWORD=admin

  Prometheus (prometheus.yml):
    Scrape target: backend:8000/metrics
    Scrape interval: 10s

  Grafana (provisioning):
    Datasource: Prometheus at http://prometheus:9090
    Dashboard: auto-loaded from /var/lib/grafana/dashboards

  SonarQube (sonar-project.properties):
    Project key: logpulse-mini-siem
    Sources: app/

  Jenkins (Jenkinsfile):
    8-stage pipeline
    Triggers on: GitHub webhook push

========================================================
10. HOW EVERYTHING CONNECTS
========================================================

  Step 1: docker compose up -d
    → Starts 5 containers on logpulse-net

  Step 2: Backend starts on port 8000
    → Initializes SQLite database
    → Loads rule engine from rules.json
    → Exposes /health, /logs, /ws, /metrics, /stats

  Step 3: Prometheus starts on port 9090
    → Reads prometheus.yml config
    → Scrapes backend:8000/metrics every 10s
    → Evaluates alert_rules.yml every 15s

  Step 4: Grafana starts on port 3000
    → Auto-provisions Prometheus datasource
    → Auto-loads system_dashboard.json
    → 8 panels visualize live metrics

  Step 5: Jenkins starts on port 8080
    → Reads Jenkinsfile from repo
    → Triggers pipeline on GitHub push
    → Runs: build → test → scan → deploy

  Step 6: SonarQube starts on port 9000
    → Receives scan results from Jenkins
    → Evaluates quality gate
    → Reports code smells, duplication, security

  Step 7: Nginx routes traffic on port 80
    → / serves frontend dashboard
    → /logs, /health, /metrics → proxied to backend
    → /ws → WebSocket upgrade to backend

  Step 8: User opens browser
    → Dashboard connects via WebSocket
    → Logs appear in real-time
    → Metrics update on Grafana
    → Alerts fire when thresholds exceeded

========================================================
END OF HEAD DOCUMENTATION
========================================================
