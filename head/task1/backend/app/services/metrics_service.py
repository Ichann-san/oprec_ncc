"""
LogPulse Mini SIEM — Metrics Service
Provides Prometheus-compatible metrics in text exposition format.
Thread-safe counters for monitoring system health.
"""

import threading


class MetricsService:
    """Manages Prometheus-style counters for the LogPulse system."""

    def __init__(self):
        self._lock = threading.Lock()
        self._counters = {
            "logpulse_total_logs": 0,
            "logpulse_error_logs": 0,
            "logpulse_warning_logs": 0,
            "logpulse_info_logs": 0,
            "logpulse_websocket_clients": 0,
            "logpulse_request_count": 0,
            "logpulse_alert_count": 0,
        }

    def increment(self, metric: str, value: int = 1):
        """Increment a counter metric by the given value."""
        with self._lock:
            if metric in self._counters:
                self._counters[metric] += value

    def decrement(self, metric: str, value: int = 1):
        """Decrement a counter metric by the given value (min 0)."""
        with self._lock:
            if metric in self._counters:
                self._counters[metric] = max(0, self._counters[metric] - value)

    def set_value(self, metric: str, value: int):
        """Set a metric to a specific value."""
        with self._lock:
            if metric in self._counters:
                self._counters[metric] = value

    def get(self, metric: str) -> int:
        """Get the current value of a metric."""
        with self._lock:
            return self._counters.get(metric, 0)

    def get_all(self) -> dict:
        """Get all metrics as a dictionary."""
        with self._lock:
            return dict(self._counters)

    def generate_prometheus_text(self) -> str:
        """
        Generate Prometheus text exposition format.
        This is what Prometheus scrapes from /metrics.
        """
        with self._lock:
            lines = []
            for metric, value in self._counters.items():
                # Add HELP and TYPE annotations
                if metric == "logpulse_total_logs":
                    lines.append(f"# HELP {metric} Total number of log events received")
                    lines.append(f"# TYPE {metric} counter")
                elif metric == "logpulse_error_logs":
                    lines.append(f"# HELP {metric} Total number of ERROR severity logs")
                    lines.append(f"# TYPE {metric} counter")
                elif metric == "logpulse_warning_logs":
                    lines.append(f"# HELP {metric} Total number of WARNING severity logs")
                    lines.append(f"# TYPE {metric} counter")
                elif metric == "logpulse_info_logs":
                    lines.append(f"# HELP {metric} Total number of INFO severity logs")
                    lines.append(f"# TYPE {metric} counter")
                elif metric == "logpulse_websocket_clients":
                    lines.append(f"# HELP {metric} Number of active WebSocket clients")
                    lines.append(f"# TYPE {metric} gauge")
                elif metric == "logpulse_request_count":
                    lines.append(f"# HELP {metric} Total number of HTTP requests")
                    lines.append(f"# TYPE {metric} counter")
                elif metric == "logpulse_alert_count":
                    lines.append(f"# HELP {metric} Total number of alerts triggered")
                    lines.append(f"# TYPE {metric} counter")

                lines.append(f"{metric} {value}")
                lines.append("")  # blank line between metrics

            return "\n".join(lines)


# Singleton instance used across the application
metrics = MetricsService()
