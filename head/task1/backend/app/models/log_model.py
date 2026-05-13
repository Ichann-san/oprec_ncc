"""
LogPulse Mini SIEM - Pydantic Models
Defines data schemas for log ingestion and responses.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class LogInput(BaseModel):
    """Schema for incoming log messages via POST /logs."""
    message: str = Field(..., description="Raw log message text")
    source: Optional[str] = Field(default="unknown", description="Log source identifier")


class LogEvent(BaseModel):
    """Internal representation of a parsed log event."""
    id: Optional[int] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    severity: str = Field(default="INFO", description="Log severity: INFO, WARNING, ERROR")
    source: str = Field(default="unknown")
    message: str
    rule_matched: Optional[str] = Field(default=None, description="Rule description if matched")
    is_alert: bool = Field(default=False, description="Whether this event triggered an alert")


class LogResponse(BaseModel):
    """Response schema after log ingestion."""
    status: str = "received"
    event: LogEvent


class LogSearchParams(BaseModel):
    """Query parameters for searching logs."""
    severity: Optional[str] = None
    source: Optional[str] = None
    keyword: Optional[str] = None
    limit: int = Field(default=100, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)
