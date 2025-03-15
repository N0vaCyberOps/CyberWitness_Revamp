import aiosqlite
import asyncio
from datetime import datetime, timedelta
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class DatabaseHandler:
    def __init__(self, path="cyber_witness.db"):
        self.db_path = path
        self.db = None

    async def _init_db(self):
        self.db = await aiosqlite.connect(self.db_path)
        await self.db.execute('''CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            severity TEXT,
            source_ip TEXT,
            description TEXT
        )''')
        await self.db.commit()
        asyncio.create_task(self._schedule_cleanup())

    async def _schedule_cleanup(self):
        while True:
            cutoff = datetime.now() - timedelta(days=30)
            await self.db.execute('DELETE FROM alerts WHERE timestamp < ?', (cutoff,))
            await self.db.commit()
            await asyncio.sleep(86400)

    async def log_alert(self, severity: str, source_ip: str, description: str):
        await self.db.execute('''INSERT INTO alerts 
            (timestamp, severity, source_ip, description)
            VALUES (?, ?, ?, ?)''',
            (datetime.now(), severity, source_ip, description))
        await self.db.commit()

    async def log_alert_batch(self, alerts: List[Dict]):
        await self.db.executemany('''INSERT INTO alerts 
            (timestamp, severity, source_ip, description)
            VALUES (?, ?, ?, ?)''',
            [(datetime.now(), a['severity'], a['source_ip'], a['description']) for a in alerts])
        await self.db.commit()

    async def close(self):
        if self.db:
            await self.db.close()

