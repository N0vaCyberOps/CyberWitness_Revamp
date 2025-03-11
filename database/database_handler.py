import aiosqlite
from utils.log_event import log_event

class DatabaseHandler:
    """Klasa obsługująca bazę danych dla Cyber Witness."""

    def __init__(self, database_file="cyber_witness.db"):
        self.database_file = database_file

    async def _connect(self):
        """Łączy się z bazą danych."""
        return await aiosqlite.connect(self.database_file)

    async def init_db(self):
        """Inicjalizuje strukturę bazy danych."""
        try:
            async with self._connect() as conn:
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS threats (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        source_ip TEXT,
                        destination_ip TEXT,
                        protocol TEXT,
                        threat_level REAL,
                        details TEXT
                    )
                """)
                await conn.execute("""
                   CREATE TABLE IF NOT EXISTS alerts (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       timestamp TEXT NOT NULL,
                       alert_type TEXT,
                       alert_data TEXT
                   )
               """)
                await conn.commit()
                log_event("INFO", "✅ Baza danych zainicjalizowana.")
        except Exception as e:
            log_event("ERROR", f"Błąd inicjalizacji bazy danych: {e}")

    async def save_alert(self, alert_data):
        """Zapisuje alert do bazy danych."""
        try:
            async with self._connect() as conn:
                await conn.execute(
                    "INSERT INTO alerts (timestamp, alert_type, alert_data) VALUES (?, ?, ?)",
                    (alert_data["timestamp"], alert_data["alert_type"], alert_data["alert_data"])
                )
                await conn.commit()
                log_event("INFO", f"🔔 Alert zapisany: {alert_data}")
        except Exception as e:
            log_event("ERROR", f"Błąd zapisu alertu: {e}")

    async def get_recent_alerts(self, limit=10):
        """Pobiera ostatnie alerty z bazy."""
        async with self._connect() as conn:
            cursor = await conn.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT ?", (limit,))
            return await cursor.fetchall()
