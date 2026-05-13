# Task 4 — Frontend Dashboard + WebSocket Streaming

## Overview
Real-time monitoring dashboard that connects to the LogPulse backend via WebSocket to display live log events.

## Features
- **Live Log Feed** — Real-time log streaming with auto-scroll
- **Severity Badges** — Color-coded: INFO (blue), WARNING (yellow), ERROR (red)
- **WebSocket Status** — Visual indicator (connected/disconnected/connecting)
- **Real-time Counters** — Total logs, errors, warnings, info, alerts, WS clients
- **Filtering** — Filter by severity level and keyword search
- **Alert Toasts** — Pop-up notifications for alert events
- **Auto-Reconnect** — Reconnects automatically after disconnection

## Files
```
frontend/
├── index.html    # Dashboard HTML
├── style.css     # Dark theme styles
└── app.js        # WebSocket client + rendering logic

sample_logs/
├── app.log       # Sample application logs
└── system.log    # Sample system logs

websocket_flow/
└── architecture.txt  # WebSocket flow documentation
```

## How to Use
1. Start the backend (see Task 1 README)
2. Open `index.html` in a browser
3. Enter the WebSocket URL (default: `ws://localhost:8000/ws`)
4. Click **Connect**
5. Send logs via `POST /logs` — they appear in real-time

## Testing with curl
```bash
curl -X POST http://localhost:8000/logs \
  -H "Content-Type: application/json" \
  -d '{"message": "User login failed - invalid credentials", "source": "auth-service"}'
```
