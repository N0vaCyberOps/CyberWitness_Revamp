import aiosqlite
import logging

class DatabaseHandler:
    def __init__(self, config):
        self.database_file = config["database_file"]

    async def _connect(self):
        return await aiosqlite.connect(self.database_file)

    async def get_recent_alerts(self, limit=10):  # ✅ Dodano brakującą metodę
        async with self._connect() as conn:
            cursor = await conn.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT ?", (limit,))
            alerts = await cursor.fetchall()
            return alerts
