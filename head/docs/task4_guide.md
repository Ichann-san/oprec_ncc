========================================================
LOGPULSE MINI SIEM — TASK 4 DOCUMENTATION
Frontend Dashboard + WebSocket Streaming
========================================================

TABLE OF CONTENTS
--------------------------------------------------------
1. Task Overview
2. Requirements
3. Frontend Architecture
4. WebSocket Workflow
5. Dashboard Features
6. File Breakdown
7. Frontend Setup Tutorial
8. WebSocket Connection Flow
9. Log Rendering Pipeline
10. Severity Color System
11. Testing with Sample Logs
12. Screenshots

========================================================
1. TASK OVERVIEW
========================================================

Task 4 implements the real-time monitoring dashboard:
  - HTML/CSS/JS frontend (no framework)
  - WebSocket client for live log streaming
  - Severity-based color coding
  - Real-time counters and filters
  - Alert toast notifications
  - Auto-reconnect on disconnection

Key deliverables:
  - Functional dashboard (index.html + style.css + app.js)
  - Real-time WebSocket log feed
  - Severity badges (INFO=blue, WARNING=yellow, ERROR=red)
  - Connection status indicator
  - Log counters (total, errors, warnings, info, alerts)
  - Sample log files for testing

========================================================
2. REQUIREMENTS
========================================================

  - A modern web browser (Chrome, Firefox, Edge)
  - LogPulse backend running (port 8000)
  - No additional software needed

Tech Stack:
  - HTML5 (semantic structure)
  - Vanilla CSS (dark theme, glassmorphism)
  - Vanilla JavaScript (WebSocket API, DOM manipulation)
  - Google Fonts (Inter, JetBrains Mono)

========================================================
3. FRONTEND ARCHITECTURE
========================================================

  index.html
      │
      ├── Header
      │   ├── Logo (LogPulse Mini SIEM)
      │   ├── WebSocket Status Indicator
      │   ├── Clear Button
      │   └── Auto-Scroll Toggle
      │
      ├── Stats Bar (6 cards)
      │   ├── Total Logs
      │   ├── Errors (red)
      │   ├── Warnings (yellow)
      │   ├── Info (blue)
      │   ├── WS Clients
      │   └── Alerts
      │
      ├── Filter Bar
      │   ├── Severity Dropdown (All/Error/Warning/Info)
      │   ├── Search Input (keyword filter)
      │   ├── WebSocket URL Input
      │   └── Connect Button
      │
      ├── Log Feed (scrollable container)
      │   └── Log Entries (dynamic)
      │       ├── Timestamp
      │       ├── Severity Badge
      │       ├── Source
      │       ├── Message
      │       └── Rule Description
      │
      └── Toast Container (alert popups)

  style.css
      │
      ├── CSS Variables (design tokens)
      ├── Dark theme base
      ├── Glassmorphism cards
      ├── Severity color system
      ├── Animations (fadeInSlide, alertGlow, pulse)
      └── Responsive breakpoints (900px, 600px)

  app.js
      │
      ├── WebSocket client (connect, disconnect, reconnect)
      ├── Log event handler
      ├── DOM rendering (log entries)
      ├── Counter management
      ├── Filtering (severity + keyword)
      ├── Toast notifications
      └── Stats polling (GET /stats every 3s)

========================================================
4. WEBSOCKET WORKFLOW
========================================================

  CONNECTION:
  1. User enters WS URL (default: ws://localhost:8000/ws)
  2. User clicks "Connect"
  3. JavaScript creates new WebSocket(url)
  4. ws.onopen fires → status turns green
  5. Dashboard displays "Connected to [url]"

  MESSAGE RECEPTION:
  1. Backend broadcasts JSON event via WebSocket
  2. ws.onmessage fires → data parsed as JSON
  3. handleLogEvent() updates counters
  4. addLogEntry() renders the log in the feed
  5. If is_alert=true → showToast() displays popup

  DISCONNECTION:
  1. ws.onclose fires with event code
  2. Status turns red with close code
  3. Auto-reconnect scheduled (5 seconds)
  4. After 5s → connect() called again
  5. If server is back → reconnects automatically

  DATA FORMAT (received from backend):
  {
    "id": 42,
    "timestamp": "2026-05-12T10:00:01.000000",
    "severity": "ERROR",
    "source": "auth-service",
    "message": "Authentication failed for user admin",
    "rule_matched": "Failure detected in log message",
    "is_alert": true
  }

========================================================
5. DASHBOARD FEATURES
========================================================

Feature 1: Live Log Feed
  - New logs appear at the bottom
  - Each entry shows: time, severity badge, source, message
  - Entries animate in with fadeInSlide
  - ERROR entries have red background + left border
  - WARNING entries have yellow background
  - INFO entries have blue left border

Feature 2: Severity Badges
  INFO    → Blue badge    (#3b82f6)
  WARNING → Yellow badge  (#f59e0b)
  ERROR   → Red badge     (#ef4444)

Feature 3: Connection Status
  Connected    → Green dot + "Connected"
  Disconnected → Red dot + "Disconnected"
  Connecting   → Yellow dot + "Connecting..."
  Dot pulses with animation

Feature 4: Real-time Counters
  6 stat cards update instantly on each log:
  - Total Logs: all logs received
  - Errors: ERROR severity count
  - Warnings: WARNING severity count
  - Info: INFO severity count
  - WS Clients: fetched from /stats every 3s
  - Alerts: triggered alert count

Feature 5: Filtering
  Severity filter: dropdown (All/Error/Warning/Info)
  Keyword search: text input, filters in real-time
  Both filters work simultaneously
  Applied to existing and new log entries

Feature 6: Alert Toasts
  Pop-up notification for alert events
  Shows: [SEVERITY] message (truncated to 120 chars)
  Auto-dismisses after 4.5 seconds
  Slides in from right, slides out

Feature 7: Auto-Scroll
  When enabled: feed scrolls to bottom on new log
  Toggle via "Auto-Scroll" button in header
  Active state shown with blue highlight

Feature 8: Clear
  Clears all log entries from the feed
  Resets all counters to 0
  Adds system message "Log feed cleared"

========================================================
6. FILE BREAKDOWN
========================================================

frontend/index.html (Dashboard Structure)
  Lines: ~90
  Contains: All HTML structure, linked CSS + JS
  Loads: Google Fonts (Inter, JetBrains Mono)
  Meta: viewport, description, title

frontend/style.css (Styling)
  Lines: ~240
  Design: Dark theme (#0a0e1a background)
  Features:
    - CSS custom properties (design tokens)
    - Glassmorphism (backdrop-filter: blur)
    - Gradient logo text
    - Severity color system (3 levels)
    - 4 animations (fadeInSlide, alertGlow, pulse, toast)
    - Responsive (900px, 600px breakpoints)
    - Custom scrollbar styling

frontend/app.js (Logic)
  Lines: ~240
  Pattern: IIFE (Immediately Invoked Function Expression)
  Functions:
    - connect()         → Create WebSocket connection
    - setStatus()       → Update connection indicator
    - handleLogEvent()  → Process incoming log data
    - addLogEntry()     → Render log in DOM
    - addSystemLog()    → Add system message
    - applyFilters()    → Filter all visible entries
    - showToast()       → Show alert popup
    - escapeHtml()      → Prevent XSS
    - fetchStats()      → Poll /stats for WS client count

sample_logs/app.log
  15 sample application logs with mixed severities

sample_logs/system.log
  15 sample system/syslog format logs

websocket_flow/architecture.txt
  WebSocket flow documentation (connection, message, disconnect)

========================================================
7. FRONTEND SETUP TUTORIAL
========================================================

OPTION A: Direct File (Local Development)
  1. Start the backend:
     cd head/task1/backend
     uvicorn app.main:app --host 0.0.0.0 --port 8000
  2. Open index.html in your browser:
     Double-click: head/task4/frontend/index.html
     URL should show: file:///C:/Users/.../index.html
  3. WebSocket URL: ws://localhost:8000/ws
  4. Click Connect

  NOTE: Do NOT use VS Code Live Server or any auto-reload
  extension. It will refresh the page on file changes and
  disconnect the WebSocket.

OPTION B: Via Nginx (Production/Docker)
  1. Start all services: docker compose up -d
  2. Frontend files are served by Nginx on port 80
  3. Open: http://SERVER_IP/
  4. WebSocket URL: ws://SERVER_IP/ws
  5. Click Connect

  [INSERT SCREENSHOT: Dashboard connected and showing logs]

========================================================
8. WEBSOCKET CONNECTION FLOW
========================================================

  Browser                    Server
    │                           │
    │──── WS Handshake ────────►│
    │     GET /ws               │
    │     Upgrade: websocket    │
    │                           │
    │◄── 101 Switching ────────│
    │    Protocols              │
    │                           │
    │    Connection OPEN        │
    │                           │
    │◄── JSON Event ───────────│ (on new log)
    │◄── JSON Event ───────────│ (on new log)
    │◄── JSON Event ───────────│ (on new log)
    │         ...               │
    │                           │
    │──── Close Frame ─────────►│ (user disconnects)
    │◄── Close ACK ────────────│
    │                           │
    │    Connection CLOSED      │
    │    (auto-reconnect 5s)    │

========================================================
9. LOG RENDERING PIPELINE
========================================================

  ws.onmessage receives data
      │
      ▼
  JSON.parse(event.data)
      │
      ▼
  handleLogEvent(data)
      │
      ├── Increment total counter
      ├── Increment severity counter (error/warning/info)
      ├── If is_alert → increment alert counter + toast
      │
      ▼
  addLogEntry(data)
      │
      ├── Create <div class="log-entry severity-{level}">
      ├── Format timestamp → toLocaleTimeString()
      ├── Create severity badge with color class
      ├── Add source label
      ├── Add message (XSS-escaped)
      ├── Add rule description (if matched)
      ├── Set data attributes for filtering
      ├── Apply current filters
      │
      ▼
  Append to log feed
      │
      ▼
  If auto-scroll → scroll to bottom

========================================================
10. SEVERITY COLOR SYSTEM
========================================================

  Severity │ Badge Color │ Entry Background │ Border
  ─────────┼─────────────┼──────────────────┼────────
  ERROR    │ #ef4444     │ rgba(239,68,68,  │ Red
           │ (red)       │  0.12)           │
  WARNING  │ #f59e0b     │ rgba(245,158,11, │ Yellow
           │ (amber)     │  0.12)           │
  INFO     │ #3b82f6     │ transparent      │ Blue
           │ (blue)      │                  │

  CSS classes:
    .badge-error   → red badge
    .badge-warning → yellow badge
    .badge-info    → blue badge
    .severity-error   → red background entry
    .severity-warning → yellow background entry
    .severity-info    → blue border entry

========================================================
11. TESTING WITH SAMPLE LOGS
========================================================

Send logs from PowerShell to test all severities:

  # INFO
  Invoke-RestMethod -Method POST `
    -Uri http://localhost:8000/logs `
    -ContentType "application/json" `
    -Body '{"message":"Application started successfully","source":"app"}'

  # WARNING
  Invoke-RestMethod -Method POST `
    -Uri http://localhost:8000/logs `
    -ContentType "application/json" `
    -Body '{"message":"Access denied for admin user","source":"auth"}'

  # ERROR (triggers alert + toast)
  Invoke-RestMethod -Method POST `
    -Uri http://localhost:8000/logs `
    -ContentType "application/json" `
    -Body '{"message":"Database connection failed","source":"db"}'

Expected Behavior:
  - INFO log: blue badge, no toast, info counter +1
  - WARNING log: yellow badge + background, alert counter +1
  - ERROR log: red badge + background, toast popup,
    error counter +1, alert counter +1

========================================================
12. SCREENSHOTS
========================================================

Insert your screenshots below:

[INSERT SCREENSHOT: Dashboard initial state (empty, disconnected)]
[INSERT SCREENSHOT: Dashboard connected (green status)]
[INSERT SCREENSHOT: Dashboard with mixed logs (INFO/WARNING/ERROR)]
[INSERT SCREENSHOT: ERROR log with red badge and alert glow]
[INSERT SCREENSHOT: Toast notification for ERROR alert]
[INSERT SCREENSHOT: Severity filter applied (showing only ERRORs)]
[INSERT SCREENSHOT: Stats bar with populated counters]
[INSERT SCREENSHOT: Dashboard via Nginx on production (http://SERVER_IP)]

========================================================
END OF TASK 4 DOCUMENTATION
========================================================
