/**
 * LogPulse Mini SIEM — Dashboard JavaScript
 * Handles WebSocket connection, log rendering, filtering, and counters.
 */

(function () {
    "use strict";

    // --- DOM Elements ---
    const logFeed = document.getElementById("log-feed");
    const wsStatus = document.getElementById("ws-status");
    const wsLabel = wsStatus.querySelector(".ws-label");
    const wsUrlInput = document.getElementById("ws-url");
    const btnConnect = document.getElementById("btn-connect");
    const btnClear = document.getElementById("btn-clear");
    const btnScrollToggle = document.getElementById("btn-scroll-toggle");
    const filterSeverity = document.getElementById("filter-severity");
    const filterSearch = document.getElementById("filter-search");
    const toastContainer = document.getElementById("toast-container");

    // Counters
    const counterTotal = document.getElementById("counter-total");
    const counterErrors = document.getElementById("counter-errors");
    const counterWarnings = document.getElementById("counter-warnings");
    const counterInfo = document.getElementById("counter-info");
    const counterClients = document.getElementById("counter-clients");
    const counterAlerts = document.getElementById("counter-alerts");

    // --- State ---
    let ws = null;
    let autoScroll = true;
    let counts = { total: 0, errors: 0, warnings: 0, info: 0, alerts: 0 };

    // --- WebSocket ---
    function connect() {
        const url = wsUrlInput.value.trim();
        if (!url) return;

        if (ws) {
            ws.close();
            ws = null;
        }

        setStatus("connecting");
        ws = new WebSocket(url);

        ws.onopen = function () {
            setStatus("connected");
            addSystemLog("Connected to " + url);
        };

        ws.onmessage = function (event) {
            try {
                const data = JSON.parse(event.data);
                handleLogEvent(data);
            } catch (e) {
                addSystemLog("Received non-JSON message: " + event.data);
            }
        };

        ws.onclose = function (event) {
            setStatus("disconnected");
            addSystemLog("WebSocket disconnected. Code: " + event.code + ", Reason: " + (event.reason || "None"));
            setTimeout(function () {
                if (!ws || ws.readyState === WebSocket.CLOSED) connect();
            }, 5000);
        };

        ws.onerror = function () {
            addSystemLog("WebSocket error occurred.");
        };
    }

    function setStatus(state) {
        wsStatus.className = "ws-status " + state;
        const labels = { connected: "Connected", disconnected: "Disconnected", connecting: "Connecting..." };
        wsLabel.textContent = labels[state] || state;
        btnConnect.textContent = state === "connected" ? "Disconnect" : "Connect";
    }

    // --- Log Events ---
    function handleLogEvent(data) {
        counts.total++;
        counterTotal.textContent = counts.total;

        if (data.severity === "ERROR") {
            counts.errors++;
            counterErrors.textContent = counts.errors;
        } else if (data.severity === "WARNING") {
            counts.warnings++;
            counterWarnings.textContent = counts.warnings;
        } else {
            counts.info++;
            counterInfo.textContent = counts.info;
        }

        if (data.is_alert) {
            counts.alerts++;
            counterAlerts.textContent = counts.alerts;
            showToast(data.severity, data.message);
        }

        addLogEntry(data);
    }

    function addLogEntry(data) {
        var entry = document.createElement("div");
        var sevClass = "severity-" + (data.severity || "info").toLowerCase();
        entry.className = "log-entry " + sevClass;
        if (data.is_alert) entry.classList.add("alert-entry");

        // Store data attributes for filtering
        entry.dataset.severity = (data.severity || "INFO").toUpperCase();
        entry.dataset.message = (data.message || "").toLowerCase();

        var time = "--:--:--";
        if (data.timestamp) {
            try {
                var d = new Date(data.timestamp);
                time = d.toLocaleTimeString();
            } catch (e) { /* use default */ }
        }

        var badgeClass = "badge-" + (data.severity || "info").toLowerCase();

        var html = '<span class="log-time">' + time + '</span>';
        html += '<span class="severity-badge ' + badgeClass + '">' + (data.severity || "INFO") + '</span>';
        html += '<span class="log-source">' + (data.source || "unknown") + '</span>';
        html += '<span class="log-message">' + escapeHtml(data.message || "") + '</span>';
        if (data.rule_matched) {
            html += '<span class="log-rule">' + escapeHtml(data.rule_matched) + '</span>';
        }

        entry.innerHTML = html;
        logFeed.appendChild(entry);

        applyFilterToEntry(entry);

        if (autoScroll) {
            logFeed.scrollTop = logFeed.scrollHeight;
        }
    }

    function addSystemLog(msg) {
        var entry = document.createElement("div");
        entry.className = "log-entry system-entry";
        entry.dataset.severity = "SYSTEM";
        entry.dataset.message = msg.toLowerCase();

        var now = new Date().toLocaleTimeString();
        entry.innerHTML =
            '<span class="log-time">' + now + '</span>' +
            '<span class="severity-badge badge-info">SYSTEM</span>' +
            '<span class="log-message">' + escapeHtml(msg) + '</span>';

        logFeed.appendChild(entry);
        if (autoScroll) logFeed.scrollTop = logFeed.scrollHeight;
    }

    // --- Filtering ---
    function applyFilters() {
        var entries = logFeed.querySelectorAll(".log-entry");
        entries.forEach(function (entry) { applyFilterToEntry(entry); });
    }

    function applyFilterToEntry(entry) {
        var sevFilter = filterSeverity.value;
        var searchFilter = filterSearch.value.toLowerCase();

        var sevMatch = sevFilter === "ALL" || entry.dataset.severity === sevFilter;
        var searchMatch = !searchFilter || (entry.dataset.message && entry.dataset.message.indexOf(searchFilter) !== -1);

        entry.style.display = (sevMatch && searchMatch) ? "" : "none";
    }

    // --- Toast ---
    function showToast(severity, message) {
        var toast = document.createElement("div");
        toast.className = "toast toast-" + severity.toLowerCase();
        toast.textContent = "[" + severity + "] " + (message.length > 120 ? message.substring(0, 120) + "..." : message);
        toastContainer.appendChild(toast);
        setTimeout(function () {
            if (toast.parentNode) toast.parentNode.removeChild(toast);
        }, 4500);
    }

    // --- Utilities ---
    function escapeHtml(str) {
        var div = document.createElement("div");
        div.appendChild(document.createTextNode(str));
        return div.innerHTML;
    }

    // --- Event Listeners ---
    btnConnect.addEventListener("click", function () {
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.close();
            ws = null;
            setStatus("disconnected");
        } else {
            connect();
        }
    });

    btnClear.addEventListener("click", function () {
        logFeed.innerHTML = "";
        counts = { total: 0, errors: 0, warnings: 0, info: 0, alerts: 0 };
        counterTotal.textContent = "0";
        counterErrors.textContent = "0";
        counterWarnings.textContent = "0";
        counterInfo.textContent = "0";
        counterAlerts.textContent = "0";
        addSystemLog("Log feed cleared.");
    });

    btnScrollToggle.addEventListener("click", function () {
        autoScroll = !autoScroll;
        btnScrollToggle.classList.toggle("active", autoScroll);
    });

    filterSeverity.addEventListener("change", applyFilters);
    filterSearch.addEventListener("input", applyFilters);

    // Fetch stats periodically
    function fetchStats() {
        var wsUrl = wsUrlInput.value.trim();
        if (!wsUrl) return;
        var baseUrl = wsUrl.replace("ws://", "http://").replace("wss://", "https://").replace("/ws", "");
        fetch(baseUrl + "/stats")
            .then(function (r) { return r.json(); })
            .then(function (data) {
                counterClients.textContent = data.logpulse_websocket_clients || 0;
            })
            .catch(function () { /* silently fail */ });
    }

    setInterval(fetchStats, 3000);
})();
