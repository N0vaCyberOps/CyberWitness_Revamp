# database/database_handler.py
import aiosqlite
import json
from utils.logging import log_info, log_error
import asyncio


async def init_db(database_file):
    """Inicjalizuje bazę danych SQLite."""
    try:
        async with aiosqlite.connect(database_file) as conn:
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
            log_info("✅ Baza danych zainicjalizowana.")
    except aiosqlite.Error as e:
        log_error(f"❌ Błąd inicjalizacji bazy: {e}")


class DatabaseHandler:
    """Obsługuje interakcje z bazą danych."""

    def __init__(self, config):
        """
        Inicjalizuje DatabaseHandler.
        :param config: Sekcja 'database' z pliku konfiguracyjnego.
        """
        self.database_file = config['database_file']
        self.conn = None  # Połączenie będzie ustanawiane asynchronicznie

    async def _connect(self):
        """Nawiązuje połączenie z bazą danych."""
        try:
            self.conn = await aiosqlite.connect(self.database_file)
            self.conn.row_factory = aiosqlite.Row  # Używaj aiosqlite.Row
            log_info("Połączono z bazą danych.")

        except aiosqlite.Error as e:
            log_error(f"Błąd połączenia z bazą danych: {e}")
            raise

    async def save_alert(self, alert_data):
        """Asynchronicznie zapisuje alert do bazy danych."""
        if self.conn is None:
            await self._connect()
        try:
            alert_data_json = json.dumps(alert_data['alert_data'])
            async with self.conn.cursor() as cursor:
                await cursor.execute("""
                    INSERT INTO alerts (timestamp, alert_type, alert_data)
                    VALUES (?, ?, ?)
                """, (alert_data['timestamp'], alert_data.get('alert_type', 'Unknown'), alert_data_json))
                await self.conn.commit()
            log_info(f"💾 Alert zapisany do bazy danych: {alert_data}")
        except aiosqlite.Error as e:
            log_error(f"❌ Błąd zapisu alertu do bazy danych: {e}")
            raise
        except Exception as e:
            log_error(f"❌ Nieoczekiwany błąd przy zapisie alertu: {e}")
            raise

    async def save_threat(self, threat_data):
        """Asynchronicznie zapisuje informacje o zagrożeniu do bazy danych."""
        if self.conn is None:
            await self._connect()
        try:
            async with self.conn.cursor() as cursor:
                await cursor.execute("""
                    INSERT INTO threats (timestamp, source_ip, destination_ip, protocol, threat_level, details)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (threat_data['timestamp'], threat_data['source_ip'], threat_data['destination_ip'],
                      threat_data['protocol'], threat_data['threat_level'], threat_data['details']))
                await self.conn.commit()
            log_info(f"💾 Zapisano zagrożenie do bazy danych: {threat_data}")
        except aiosqlite.Error as e:
            log_error(f"❌ Błąd zapisu do bazy danych: {e}")
            raise
        except Exception as e:
            log_error(f"❌ Nieoczekiwany błąd przy zapisie zagrożenia: {e}")
            raise

    async def get_recent_threats(self, limit=10):
        """Asynchronicznie pobiera ostatnie zagrożenia z bazy danych."""
        if self.conn is None:
            await self._connect()
        try:
            async with self.conn.cursor() as cursor:
                await cursor.execute("SELECT * FROM threats ORDER BY timestamp DESC LIMIT ?", (limit,))
                rows = await cursor.fetchall()
                threats = [dict(row) for row in rows]  # Konwersja na słowniki
                return threats
        except aiosqlite.Error as e:
            log_error(f"Błąd podczas pobierania zagrożeń: {e}")
            return []
        except Exception as e:
            log_error(f"Nieoczekiwany błąd: {e}")
            return []

    async def get_recent_alerts(self, limit=10):
        """Asynchronicznie pobiera ostatnie alerty z bazy danych."""
        if self.conn is None:
            await self._connect()
        try:
            async with self.conn.cursor() as cursor:
                await cursor.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT ?", (limit,))
                rows = await cursor.fetchall()
                alerts = []
                for row in rows:
                    alert = dict(row)
                    try:
                        alert['alert_data'] = json.loads(alert['alert_data'])
                    except json.JSONDecodeError:
                        log_error(f"Błąd dekodowania JSON dla alertu ID {alert['id']}")
                        alert['alert_data'] = {}
                    alerts.append(alert)
                return alerts
        except aiosqlite.Error as e:
            log_error(f"Błąd podczas pobierania alertów z bazy: {e}")
            return []
        except Exception as e:
            log_error(f"Nieoczekiwany błąd: {e}")
            return []
    async def close(self):
        """Zamyka połączenie z bazą danych."""
        if self.conn:
            await self.conn.close()
            log_info("Zamknięto połączenie z bazą danych.")