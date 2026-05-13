# Task 3 — Monitoring (Prometheus + Grafana + Alerting)

## Overview
Complete monitoring stack for the LogPulse Mini SIEM system using Prometheus for metric collection, Grafana for visualization, and Discord for alert notifications.

## Architecture
```
LogPulse Backend (/metrics)
        |
        v
  Prometheus (scrapes every 10s)
        |
        +---- Alert Rules (alert_rules.yml)
        |
        v
  Grafana (visualizes via PromQL)
        |
        v
  Dashboard (8 custom panels)
```

## Components

### Prometheus
| File | Purpose |
|------|---------|
| `prometheus/prometheus.yml` | Scrape configuration — targets backend:8000/metrics |
| `prometheus/alert_rules.yml` | 5 alert rules for critical conditions |

### Grafana
| File | Purpose |
|------|---------|
| `grafana/dashboards/system_dashboard.json` | Custom dashboard with 8 panels |
| `grafana/provisioning/datasources/datasource.yml` | Auto-configures Prometheus datasource |
| `grafana/provisioning/dashboards/dashboard.yml` | Auto-loads dashboard JSON files |

### Alerts
| File | Purpose |
|------|---------|
| `alerts/discord_webhook.txt` | Discord webhook setup guide |

## Dashboard Panels
1. **Total Logs** — Stat panel with color thresholds
2. **Error Logs** — Stat panel (green→amber→red)
3. **Warning Logs** — Stat panel
4. **Requests Per Minute** — Time series with smooth line
5. **WebSocket Active Users** — Gauge (0–50 range)
6. **Alerts Triggered** — Time series (red fill)
7. **Log Severity Breakdown** — Donut pie chart
8. **System Overview** — Combined time series of all metrics

## Alert Rules
| Alert | Condition | Severity |
|-------|-----------|----------|
| HighErrorRate | `logpulse_error_logs > 50` for 1m | Critical |
| HighAlertCount | `logpulse_alert_count > 100` for 1m | Warning |
| NoWebSocketClients | `logpulse_websocket_clients == 0` for 5m | Warning |
| BackendDown | `up{job="logpulse-backend"} == 0` for 1m | Critical |
| HighRequestRate | `logpulse_request_count > 1000` for 2m | Warning |

## Accessing Services
| Service | URL | Default Credentials |
|---------|-----|-------------------|
| Prometheus | http://localhost:9090 | — |
| Grafana | http://localhost:3000 | admin / admin |
