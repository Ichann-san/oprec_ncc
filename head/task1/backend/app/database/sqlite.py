"""
LogPulse Mini SIEM - SQLite Database Module
Handles database initialization and CRUD operations for log events.
"""

import aiosqlite
import os
from typing import List, Optional, Dict, Any

# Database file path — configurable via environment variable
DB_PATH = os.getenv("LOGPULSE_DB_PATH", "logpulse.db")


async def init_db():
    """Initialize the SQLite database and create the logs table if it doesn't exist."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                severity TEXT NOT NULL DEFAULT 'INFO',
                source TEXT NOT NULL DEFAULT 'unknown',
                message TEXT NOT NULL
            )
        """)
        await db.commit()


async def insert_log(timestamp: str, severity: str, source: str, message: str) -> int:
    """
    Insert a new log event into the database.
    Returns the ID of the inserted row.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO logs (timestamp, severity, source, message) VALUES (?, ?, ?, ?)",
            (timestamp, severity, source, message)
        )
        await db.commit()
        return cursor.lastrowid


async def get_logs(
    severity: Optional[str] = None,
    source: Optional[str] = None,
    keyword: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Retrieve log events with optional filtering.
    Supports filtering by severity, source, and keyword search.
    """
    query = "SELECT id, timestamp, severity, source, message FROM logs WHERE 1=1"
    params = []

    if severity:
        query += " AND severity = ?"
        params.append(severity.upper())

    if source:
        query += " AND source = ?"
        params.append(source)

    if keyword:
        query += " AND message LIKE ?"
        params.append(f"%{keyword}%")

    query += " ORDER BY id DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(query, params)
        rows = await cursor.fetchall()
        return [
            {
                "id": row["id"],
                "timestamp": row["timestamp"],
                "severity": row["severity"],
                "source": row["source"],
                "message": row["message"],
            }
            for row in rows
        ]


async def get_log_count() -> int:
    """Get total number of logs stored."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM logs")
        row = await cursor.fetchone()
        return row[0] if row else 0
