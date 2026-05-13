"""
LogPulse Mini SIEM — WebSocket Service
Manages WebSocket connections: connect, disconnect, broadcast.
Supports multiple concurrent clients.
"""

from fastapi import WebSocket
from typing import List
import json
import logging

logger = logging.getLogger("logpulse.websocket")


class WebSocketManager:
    """Manages active WebSocket connections and broadcasts events."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection and add to active list."""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Active clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection from the active list."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket client disconnected. Active clients: {len(self.active_connections)}")

    async def broadcast(self, data: dict):
        """
        Broadcast a message to all active WebSocket connections.
        Disconnects clients that fail to receive.
        """
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(data))
            except Exception:
                disconnected.append(connection)
                logger.warning("Failed to send to a WebSocket client, marking for disconnect")

        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)

    @property
    def client_count(self) -> int:
        """Return the number of active WebSocket connections."""
        return len(self.active_connections)


# Singleton instance used across the application
ws_manager = WebSocketManager()
