import aiosqlite
import json
from typing import Dict, Any, List
from utils.log_event import log_event

class DatabaseHandler:
    def __init__(self, config: Dict[str, Any]):
        self.database_file = config["database_file"]
        self._pool = None

    async def _get_connection(self) -> aiosqlite.Connection:
        try:
            conn = await aiosqlite.connect(self.database_file)
            conn.row_factory = aiosqlite.Row
            return conn
        except Exception as e:
            log_event("CRITICAL", f"Database connection failed: {e}")
            raise

    async def initialize(self) -> None:
        conn = await self._get_connection()
        try:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    alert_type TEXT NOT NULL,
                    alert_data TEXT NOT NULL,
                    source_ip TEXT,
                    threat_level REAL
                )
            """)
            await conn.commit()
        finally:
            await conn.close()

    async def save_alert(self, alert_data: Dict[str, Any]) -> bool:
        required_keys = {"timestamp", "alert_type", "alert_data"}
        if missing := required_keys - alert_data.keys():
            log_event("ERROR", f"Missing required keys: {missing}")
            return False

        conn = await self._get_connection()
        try:
            await conn.execute(
                """INSERT INTO alerts 
                (timestamp, alert_type, alert_data, source_ip, threat_level)
                VALUES (?, ?, ?, ?, ?)""",
                (
                    alert_data["timestamp"],
                    alert_data["alert_type"],
                    json.dumps(alert_data["alert_data"]),
                    alert_data.get("source_ip"),
                    alert_data.get("threat_level", 0.0)
                )
            )
            await conn.commit()
            return True
        except Exception as e:
            log_event("ERROR", f"Alert save failed: {e}")
            return False
        finally:
            await conn.close()

    async def get_recent_alerts(self, limit: int = 10) -> List[Dict]:
        conn = await self._get_connection()
        try:
            cursor = await conn.execute(
                "SELECT * FROM alerts ORDER BY id DESC LIMIT ?",
                (limit,)
            )
            return [dict(row) for row in await cursor.fetchall()]
        finally:
            await conn.close()