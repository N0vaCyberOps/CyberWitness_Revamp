import aiosqlite
import json

class DatabaseHandler:
    def __init__(self, config):
        """Initializes the database handler."""
        self.database_file = config["database_file"]
        self._pool = None

    async def connect(self):
        """Creates a connection pool if not already initialized."""
        if not self._pool:
            self._pool = await aiosqlite.connect(self.database_file)
        return self._pool

    async def close(self):
        """Closes the connection pool when the app shuts down."""
        if self._pool:
            await self._pool.close()
            self._pool = None

    async def save_alert(self, alert_data):
        """Inserts an alert into the database using a connection pool."""
        conn = await self.connect()
        try:
            async with conn.execute(
                "INSERT INTO alerts (timestamp, alert_type, alert_data) VALUES (?, ?, ?)",
                (alert_data["timestamp"], alert_data["alert_type"], json.dumps(alert_data["alert_data"]))
            ):
                await conn.commit()
        except aiosqlite.DatabaseError as e:
            print(f"Database error: {e}")  # Replace with log_event("ERROR", f"Database error: {e}")
            return False
        return True
