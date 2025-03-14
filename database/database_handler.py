import sqlcipher3 as sqlite
import os
import threading
from datetime import datetime, timedelta
import logging
import asyncio

logger = logging.getLogger(__name__)

class DatabaseHandler:
    def __init__(self, path="cyber_witness.db"):
        self.conn = sqlite.connect(path, check_same_thread=False)
        self.conn.execute(f"PRAGMA key='{os.getenv('DB_KEY')}'")
        self.lock = threading.Lock()
        self.alert_queue = asyncio.Queue(maxsize=1000)
        self._init_db()
        self._schedule_cleanup()
        asyncio.create_task(self._process_alert_queue())

    def _init_db(self):
        with self.lock:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY,
                timestamp DATETIME,
                severity TEXT,
                source_ip TEXT,
                description TEXT)''')
            self.conn.execute('''CREATE INDEX IF NOT EXISTS idx_timestamp ON alerts (timestamp)''')
            self.conn.commit()

    async def _process_alert_queue(self):
        batch = []
        while True:
            try:
                alert = await asyncio.wait_for(self.alert_queue.get(), timeout=5.0)
                batch.append(alert)
                if len(batch) >= 100:
                    await self.log_alert_batch(batch)
                    batch = []
            except asyncio.TimeoutError:
                if batch:
                    await self.log_alert_batch(batch)
                    batch = []

    async def log_alert(self, severity, source_ip, description):
        await self.alert_queue.put({
            'severity': severity,
            'source_ip': source_ip,
            'description': description
        })

    async def log_alert_batch(self, alerts):
        with self.lock:
            try:
                self.conn.executemany('''INSERT INTO alerts 
                    (timestamp, severity, source_ip, description)
                    VALUES (?, ?, ?, ?)''',
                    [(datetime.now(), a['severity'], a['source_ip'], a['description']) for a in alerts])
                self.conn.commit()
            except Exception as e:
                logger.error(f"Batch insert failed: {e}")
                raise

    def _schedule_cleanup(self):
        def cleanup():
            cutoff = datetime.now() - timedelta(days=30)
            with self.lock:
                self.conn.execute('DELETE FROM alerts WHERE timestamp < ?', (cutoff,))
                self.conn.commit()
            threading.Timer(86400, cleanup).start()
        cleanup()

    async def close(self):
        self.conn.close()