import aiosqlite
import json
from typing import Dict, Any, List, AsyncIterator
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger(__name__)

class DatabaseHandler:
    def __init__(self, config: Dict[str, Any]):
        self.database_file = config["database_file"]
        self._connection_pool = None

    # Poprawiony kontekstowy menadżer połączeń
    @asynccontextmanager
    async def _get_connection(self) -> AsyncIterator[aiosqlite.Connection]:
        """Poprawione zarządzanie pulą połączeń"""
        if not self._connection_pool:
            self._connection_pool = await aiosqlite.connect(self.database_file)
            self._connection_pool.row_factory = aiosqlite.Row
            
        async with self._connection_pool:
            yield self._connection_pool

    async def initialize(self):
        """Poprawiona inicjalizacja z prawidłowym użyciem transakcji"""
        async with self._get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("""
                    CREATE TABLE IF NOT EXISTS alerts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        alert_type TEXT NOT NULL,
                        alert_data TEXT NOT NULL
                    )  -- Usunięto STRICT dla kompatybilności
                """)
            await conn.commit()

    async def batch_save_alerts(self, alerts: List[Dict[str, Any]]):
        """Poprawiony batch insert z transakcją"""
        async with self._get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.executemany(
                    "INSERT INTO alerts (timestamp, alert_type, alert_data) VALUES (?, ?, ?)",
                    [(a["timestamp"], a["alert_type"], json.dumps(a["alert_data"])) for a in alerts]
                )
            await conn.commit()

    async def get_recent_alerts(self, limit: int = 100) -> List[Dict]:
        """Poprawione pobieranie danych z prawidłowym zakresem blokowania"""
        async with self._get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "SELECT * FROM alerts ORDER BY id DESC LIMIT ?",
                    (limit,)
                )
                return [dict(row) for row in await cursor.fetchall()]

    async def close(self):
        """Nowa metoda do bezpiecznego zamykania połączeń"""
        if self._connection_pool:
            await self._connection_pool.close()
            self._connection_pool = None