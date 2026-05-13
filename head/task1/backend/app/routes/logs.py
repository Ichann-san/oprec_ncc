"""
LogPulse Mini SIEM - Logs Route
Handles log ingestion (POST /logs) and log search (GET /logs).
Integrates parser, database, WebSocket broadcast, and metrics.
"""

from fastapi import APIRouter, HTTPException
from app.models.log_model import LogInput, LogEvent, LogResponse
from app.services.parser_service import parse_log
from app.services.metrics_service import metrics
from app.services.websocket_service import ws_manager
from app.database.sqlite import insert_log, get_logs
from typing import Optional
import logging
import os
import httpx

logger = logging.getLogger("logpulse.logs")
router = APIRouter()

# Discord webhook URL for alert notifications
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "YOUR_DISCORD_WEBHOOK_URL")


async def send_discord_alert(event: dict):
    """Send an alert notification to Discord via webhook."""
    if DISCORD_WEBHOOK_URL == "YOUR_DISCORD_WEBHOOK_URL":
        logger.debug("Discord webhook not configured, skipping notification")
        return

    severity_emoji = {
        "ERROR": "🟥",
        "WARNING": "🟨",
        "INFO": "🟦",
    }

    emoji = severity_emoji.get(event["severity"], "⬜")

    payload = {
        "embeds": [
            {
                "title": f"{emoji} LogPulse Alert — {event['severity']}",
                "description": event["message"],
                "color": {
                    "ERROR": 0xFF0000,
                    "WARNING": 0xFFAA00,
                    "INFO": 0x0099FF,
                }.get(event["severity"], 0x888888),
                "fields": [
                    {"name": "Source", "value": event["source"], "inline": True},
                    {"name": "Rule", "value": event.get("rule_matched") or "None", "inline": True},
                    {"name": "Timestamp", "value": event["timestamp"], "inline": False},
                ],
            }
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(DISCORD_WEBHOOK_URL, json=payload)
            if response.status_code == 204:
                logger.info("Discord alert sent successfully")
            else:
                logger.warning(f"Discord webhook returned status {response.status_code}")
    except Exception as e:
        logger.error(f"Failed to send Discord alert: {e}")


@router.post("/logs", response_model=LogResponse)
async def ingest_log(log_input: LogInput):
    """
    Ingest a log message:
    1. Parse the message (extract severity via rule engine)
    2. Store in SQLite database
    3. Broadcast to all WebSocket clients
    4. Update Prometheus metrics
    5. Send Discord alert if severity is ERROR
    """
    # Increment request counter
    metrics.increment("logpulse_request_count")

    # Parse the log message through the rule engine
    parsed = parse_log(log_input.message, log_input.source)

    # Store in database
    try:
        log_id = await insert_log(
            timestamp=parsed["timestamp"],
            severity=parsed["severity"],
            source=parsed["source"],
            message=parsed["message"],
        )
        parsed["id"] = log_id
    except Exception as e:
        logger.error(f"Failed to store log: {e}")
        raise HTTPException(status_code=500, detail="Failed to store log event")

    # Update metrics
    metrics.increment("logpulse_total_logs")
    if parsed["severity"] == "ERROR":
        metrics.increment("logpulse_error_logs")
    elif parsed["severity"] == "WARNING":
        metrics.increment("logpulse_warning_logs")
    elif parsed["severity"] == "INFO":
        metrics.increment("logpulse_info_logs")

    if parsed["is_alert"]:
        metrics.increment("logpulse_alert_count")

    # Broadcast to WebSocket clients
    await ws_manager.broadcast(parsed)

    # Send Discord alert for ERROR severity
    if parsed["severity"] == "ERROR":
        await send_discord_alert(parsed)

    # Build response
    event = LogEvent(
        id=parsed.get("id"),
        timestamp=parsed["timestamp"],
        severity=parsed["severity"],
        source=parsed["source"],
        message=parsed["message"],
        rule_matched=parsed["rule_matched"],
        is_alert=parsed["is_alert"],
    )

    logger.info(f"Log ingested: [{event.severity}] {event.message[:80]}")
    return LogResponse(status="received", event=event)


@router.get("/logs")
async def search_logs(
    severity: Optional[str] = None,
    source: Optional[str] = None,
    keyword: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
):
    """
    Search and retrieve stored log events.
    Supports filtering by severity, source, and keyword.
    """
    metrics.increment("logpulse_request_count")

    try:
        logs = await get_logs(
            severity=severity,
            source=source,
            keyword=keyword,
            limit=min(limit, 1000),
            offset=offset,
        )
        return {"status": "ok", "count": len(logs), "logs": logs}
    except Exception as e:
        logger.error(f"Failed to search logs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve logs")
