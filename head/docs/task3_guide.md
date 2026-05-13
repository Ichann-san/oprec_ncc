========================================================
LOGPULSE MINI SIEM — TASK 3 DOCUMENTATION
Monitoring (Prometheus + Grafana + Alerting)
========================================================

TABLE OF CONTENTS
--------------------------------------------------------
1. Task Overview
2. Requirements
3. Monitoring Architecture
4. Prometheus Configuration
5. Prometheus Setup Tutorial
6. Alert Rules Explained
7. Grafana Configuration
8. Grafana Setup Tutorial
9. Dashboard Panels Explained
10. Discord Alerting Setup
11. PromQL Query Reference
12. Screenshots

========================================================
1. TASK OVERVIEW
========================================================

Task 3 implements the complete monitoring stack:
  - Prometheus collects metrics from the backend
  - Grafana visualizes metrics in a custom dashboard
  - Alert rules trigger when thresholds are exceeded
  - Discord webhook sends real-time notifications

Key deliverables:
  - Prometheus scrape configuration (prometheus.yml)
  - 5 alert rules (alert_rules.yml)
  - Grafana auto-provisioned datasource
  - Custom 8-panel Grafana dashboard
  - Discord webhook alert integration

========================================================
2. REQUIREMENTS
========================================================

Services (running via docker-compose):
  - Prometheus (port 9090)
  - Grafana (port 3000)
  - LogPulse Backend (port 8000) — provides /metrics

No additional software to install — all runs in Docker.

========================================================
3. MONITORING ARCHITECTURE
========================================================

  LogPulse Backend
      │
      │ GET /metrics (every 10s)
      │
      ▼
  Prometheus
      │
      ├── Stores time-series data
      ├── Evaluates alert_rules.yml (every 15s)
      │
      │ PromQL queries
      │
      ▼
  Grafana
      │
      ├── 8-panel dashboard
      ├── Auto-refresh every 10s
      │
      ▼
  Browser (Dashboard Visualization)

  Alert Flow:
  Prometheus Alert Rule → (if threshold exceeded) →
    Discord Webhook → Notification in channel

========================================================
4. PROMETHEUS CONFIGURATION
========================================================

File: task3/prometheus/prometheus.yml

Global Settings:
  scrape_interval: 15s
  evaluation_interval: 15s
  scrape_timeout: 10s

Scrape Jobs:

  Job: logpulse-backend
    Target: backend:8000
    Path: /metrics
    Interval: 10s
    Labels: service=logpulse, environment=production

  Job: prometheus (self-monitoring)
    Target: localhost:9090

Rule Files:
  - alert_rules.yml

========================================================
5. PROMETHEUS SETUP TUTORIAL
========================================================

Prometheus is auto-configured via docker-compose and
prometheus.yml. No manual setup needed.

STEP 1: Verify Prometheus is Running
  1. Open http://SERVER_IP:9090
  2. You should see the Prometheus UI

  [INSERT SCREENSHOT: Prometheus main page]

STEP 2: Check Targets
  1. Go to Status → Targets
  2. You should see two targets:
     - logpulse-backend (State: UP)
     - prometheus (State: UP)
  3. If backend shows "DOWN", verify:
     - Backend container is running
     - Both are on the same Docker network

  [INSERT SCREENSHOT: Prometheus targets page — both UP]

STEP 3: Test a Query
  1. On the main page, type in the query box:
     logpulse_total_logs
  2. Click "Execute"
  3. Switch to "Graph" tab to see the time series
  4. Try other queries:
     logpulse_error_logs
     logpulse_websocket_clients
     rate(logpulse_request_count[1m])

  [INSERT SCREENSHOT: Prometheus query result]
  [INSERT SCREENSHOT: Prometheus graph view]

STEP 4: Check Alert Rules
  1. Go to Status → Rules
  2. You should see the "logpulse_alerts" group
  3. All 5 rules should be listed with their status

  [INSERT SCREENSHOT: Prometheus alert rules page]

STEP 5: Check Active Alerts
  1. Go to Alerts
  2. Shows currently firing or pending alerts
  3. If no thresholds are exceeded, all alerts show "inactive"

  [INSERT SCREENSHOT: Prometheus alerts page]

========================================================
6. ALERT RULES EXPLAINED
========================================================

File: task3/prometheus/alert_rules.yml

Rule 1: HighErrorRate
  Expression: logpulse_error_logs > 50
  Duration: 1 minute
  Severity: critical
  Meaning: More than 50 error logs have been recorded.
           Something is seriously wrong with the system.

Rule 2: HighAlertCount
  Expression: logpulse_alert_count > 100
  Duration: 1 minute
  Severity: warning
  Meaning: Over 100 alerts triggered. Possible attack
           or system malfunction.

Rule 3: NoWebSocketClients
  Expression: logpulse_websocket_clients == 0
  Duration: 5 minutes
  Severity: warning
  Meaning: No dashboard is connected for monitoring.
           The system is running unobserved.

Rule 4: BackendDown
  Expression: up{job="logpulse-backend"} == 0
  Duration: 1 minute
  Severity: critical
  Meaning: Prometheus cannot reach the backend.
           The service is down.

Rule 5: HighRequestRate
  Expression: logpulse_request_count > 1000
  Duration: 2 minutes
  Severity: warning
  Meaning: High traffic volume detected.
           Possible DoS or unusual activity.

========================================================
7. GRAFANA CONFIGURATION
========================================================

Datasource Provisioning:
  File: grafana/provisioning/datasources/datasource.yml
  Auto-connects Grafana to Prometheus at:
    http://prometheus:9090

Dashboard Provisioning:
  File: grafana/provisioning/dashboards/dashboard.yml
  Auto-loads all JSON files from:
    /var/lib/grafana/dashboards

Dashboard JSON:
  File: grafana/dashboards/system_dashboard.json
  Contains 8 panels with PromQL queries.

========================================================
8. GRAFANA SETUP TUTORIAL
========================================================

Grafana is auto-provisioned — datasource and dashboard
are loaded automatically. Follow these steps to verify.

STEP 1: Access Grafana
  1. Open http://SERVER_IP:3000
  2. Login with:
     Username: admin
     Password: admin (or whatever you set in .env)
  3. Grafana will ask to change password — you can skip

  [INSERT SCREENSHOT: Grafana login page]

STEP 2: Verify Datasource
  1. Go to Connections → Data sources (left sidebar)
  2. You should see "Prometheus" listed
  3. Click on it → click "Test" button
  4. Should show "Data source is working"

  [INSERT SCREENSHOT: Grafana datasource — Prometheus connected]

STEP 3: Open the Dashboard
  1. Go to Dashboards (left sidebar)
  2. Open the "LogPulse" folder
  3. Click "LogPulse Mini SIEM Dashboard"
  4. You should see 8 panels

  [INSERT SCREENSHOT: Grafana dashboard with all 8 panels]

STEP 4: Generate Data
  Send some logs to populate the dashboard:

  # From PowerShell:
  Invoke-RestMethod -Method POST `
    -Uri http://SERVER_IP:8000/logs `
    -ContentType "application/json" `
    -Body '{"message":"Test error log","source":"test"}'

  Wait 15 seconds, then check the dashboard — panels
  should update with new data.

  [INSERT SCREENSHOT: Dashboard showing live data]

STEP 5: Explore Panels
  Click on any panel → "Edit" to see the PromQL query.
  Modify time range using the picker (top right).
  Use "Last 15 minutes" for recent activity.

  [INSERT SCREENSHOT: Editing a panel — showing PromQL query]

========================================================
9. DASHBOARD PANELS EXPLAINED
========================================================

Panel 1: Total Logs (Stat)
  Query: logpulse_total_logs
  Shows: Total count of all ingested logs
  Colors: Green (<500), Amber (500-1000), Red (>1000)

Panel 2: Error Logs (Stat)
  Query: logpulse_error_logs
  Shows: Count of ERROR severity logs
  Colors: Green (<10), Amber (10-50), Red (>50)

Panel 3: Warning Logs (Stat)
  Query: logpulse_warning_logs
  Shows: Count of WARNING severity logs
  Colors: Green (<20), Amber (20-100), Red (>100)

Panel 4: Requests Per Minute (Time Series)
  Query: rate(logpulse_request_count[1m]) * 60
  Shows: Request rate over time (smooth line)
  Type: Line graph with fill

Panel 5: WebSocket Active Users (Gauge)
  Query: logpulse_websocket_clients
  Shows: Number of connected dashboard clients
  Range: 0–50
  Colors: Red (0), Amber (1-2), Green (3+)

Panel 6: Alerts Triggered (Time Series)
  Query: logpulse_alert_count
  Shows: Alert count over time
  Color: Red line with fill

Panel 7: Log Severity Breakdown (Pie Chart)
  Queries: logpulse_error_logs, warning_logs, info_logs
  Shows: Distribution of log severities
  Type: Donut chart
  Colors: Red (Error), Amber (Warning), Blue (Info)

Panel 8: System Overview (Time Series)
  Queries: All 5 metrics combined
  Shows: Complete system overview over time
  Type: Multi-line chart with table legend

========================================================
10. DISCORD ALERTING SETUP
========================================================

The backend sends Discord notifications for ERROR logs.
See: task3/alerts/discord_webhook.txt for full guide.

STEP 1: Create Discord Webhook
  1. Open Discord
  2. Go to your server → Channel Settings
  3. Click Integrations → Webhooks → New Webhook
  4. Name: LogPulse Alerts
  5. Select the channel for alerts
  6. Copy the Webhook URL

  [INSERT SCREENSHOT: Discord webhook creation]

STEP 2: Configure the Backend
  1. Edit .env file:
     DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
  2. Restart the backend:
     docker compose restart backend

STEP 3: Test
  Send an ERROR log:

  Invoke-RestMethod -Method POST `
    -Uri http://SERVER_IP:8000/logs `
    -ContentType "application/json" `
    -Body '{"message":"Critical database failure","source":"db"}'

  Check your Discord channel — you should see an embed
  with red color, the error message, source, and timestamp.

  [INSERT SCREENSHOT: Discord alert notification received]

========================================================
11. PROMQL QUERY REFERENCE
========================================================

Basic Queries:
  logpulse_total_logs         → Total log count
  logpulse_error_logs         → Error log count
  logpulse_warning_logs       → Warning log count
  logpulse_info_logs          → Info log count
  logpulse_websocket_clients  → Active WS connections
  logpulse_request_count      → Total HTTP requests
  logpulse_alert_count        → Total alerts fired

Rate Queries:
  rate(logpulse_request_count[1m])   → Requests per second
  rate(logpulse_total_logs[5m])      → Logs per second (5m avg)
  rate(logpulse_error_logs[5m])      → Errors per second

Ratio Queries:
  logpulse_error_logs / logpulse_total_logs
    → Error rate as percentage

Threshold Queries:
  logpulse_error_logs > 50           → True if errors > 50
  up{job="logpulse-backend"} == 0    → True if backend down

========================================================
12. SCREENSHOTS
========================================================

Insert your screenshots below:

[INSERT SCREENSHOT: Prometheus targets — all UP]
[INSERT SCREENSHOT: Prometheus query — logpulse_total_logs]
[INSERT SCREENSHOT: Prometheus alert rules page]
[INSERT SCREENSHOT: Grafana login]
[INSERT SCREENSHOT: Grafana datasource test — working]
[INSERT SCREENSHOT: Full Grafana dashboard with 8 panels]
[INSERT SCREENSHOT: Individual panel edit — PromQL visible]
[INSERT SCREENSHOT: Discord alert notification]

========================================================
END OF TASK 3 DOCUMENTATION
========================================================
