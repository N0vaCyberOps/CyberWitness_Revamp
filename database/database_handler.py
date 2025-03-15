import aiosqlite
import os
import threading
from datetime import datetime, timedelta
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class DatabaseHandler:
    def __init__(self, path="cyber_witness.db"):
        self.db_path = path
        self.lock = threading.Lock()
        asyncio.create_task(self._init_db())  # Inicjalizacja asynchroniczna
        asyncio.create_task(self._schedule_cleanup())  # Cleanup jako zadanie asynchroniczne

    async def _init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                severity TEXT,
                source_ip TEXT,
                description TEXT
            )''')
            await db.commit()

    async def _schedule_cleanup(self):
        while True:
            cutoff = datetime.now() - timedelta(days=30)
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('DELETE FROM alerts WHERE timestamp < ?', (cutoff,))
                await db.commit()
            await asyncio.sleep(86400)  # Czekaj 24 godziny

    async def log_alert(self, severity: str, source_ip: str, description: str) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''INSERT INTO alerts 
                    (timestamp, severity, source_ip, description)
                    VALUES (?, ?, ?, ?)''',
                    (datetime.now(), severity, source_ip, description))
                await db.commit()
            except Exception as e:
                logger.error(f"Error logging alert: {str(e)}")
                raise

    async def log_alert_batch(self, alerts: List[Dict]) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.executemany('''INSERT INTO alerts 
                    (timestamp, severity, source_ip, description)
                    VALUES (?, ?, ?, ?)''',
                    [(datetime.now(), a['severity'], a['source_ip'], a['description']) for a in alerts])
                await db.commit()
            except Exception as e:
                logger.error(f"Batch insert failed: {str(e)}")
                raise

    async def close(self):
        pass  # aiosqlite zamyka połączenia automatycznie