"""
LogPulse Mini SIEM — WebSocket Route
Handles real-time WebSocket connections for live log streaming.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from oprec_ncc.head.task1.backend.app.services.websocket_service import ws_manager
from oprec_ncc.head.task1.backend.app.services.metrics_service import metrics
import logging

logger = logging.getLogger("logpulse.ws_route")
router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time log streaming.
    - Accepts client connection
    - Tracks active clients in metrics
    - Keeps connection alive until client disconnects
    - Broadcasts are handled by the WebSocket service when new logs arrive
    """
    await ws_manager.connect(websocket)
    metrics.set_value("logpulse_websocket_clients", ws_manager.client_count)

    try:
        while True:
            # Keep the connection alive by waiting for any incoming messages
            # Clients can send ping/pong or commands if needed
            data = await websocket.receive_text()
            logger.debug(f"Received from WebSocket client: {data}")
    except WebSocketDisconnect as e:
        ws_manager.disconnect(websocket)
        metrics.set_value("logpulse_websocket_clients", ws_manager.client_count)
        logger.info(f"WebSocket client disconnected gracefully. Code: {e.code}, Reason: {e.reason}")
    except Exception as e:
        ws_manager.disconnect(websocket)
        metrics.set_value("logpulse_websocket_clients", ws_manager.client_count)
        logger.error(f"WebSocket error: {e}")
