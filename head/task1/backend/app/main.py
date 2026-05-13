"""
LogPulse Mini SIEM - FastAPI Main Application
Entry point for the backend service.
Configures routes, middleware, static files, and startup events.
"""

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
import os

from app.routes import websocket
from app.services.metrics_service import metrics
from app.database.sqlite import init_db
from app.routes import health, logs

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger("logpulse")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: initialize resources on startup, cleanup on shutdown."""
    # Startup
    logger.info("LogPulse Mini SIEM starting up...")
    await init_db()
    logger.info("Database initialized")
    yield
    # Shutdown
    logger.info("LogPulse Mini SIEM shutting down...")


# Create FastAPI application
app = FastAPI(
    title="LogPulse Mini SIEM",
    description="Real-time log monitoring and security event management system",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware — allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include route modules
app.include_router(health.router, tags=["Health"])
app.include_router(logs.router, tags=["Logs"])
app.include_router(websocket.router, tags=["WebSocket"])


@app.get("/metrics")
async def prometheus_metrics():
    """
    Prometheus metrics endpoint.
    Returns metrics in Prometheus text exposition format.
    """
    metrics.increment("logpulse_request_count")
    return Response(
        content=metrics.generate_prometheus_text(),
        media_type="text/plain; version=0.0.4; charset=utf-8",
    )


@app.get("/stats")
async def stats():
    """Quick stats endpoint returning current metrics as JSON."""
    return metrics.get_all()


# Mount static files directory if it exists
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
