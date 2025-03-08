# tests/test_database_handler.py
import unittest
import os
import json
import tempfile
import asyncio
from database.database_handler import DatabaseHandler, init_db

class TestDatabaseHandler(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        """Tworzy tymczasową bazę danych do testów."""
        self.temp_db_file = tempfile.NamedTemporaryFile(delete=False)  
        self.db_path = self.temp_db_file.name
        self.temp_db_file.close()  
        await init_db(self.db_path)  
        self.config = {'database_file': self.db_path}
        self.db_handler = DatabaseHandler(self.config)
        await self.db_handler._connect() 

        self.test_alert_data = {
            'timestamp': '2024-04-27 12:00:00',
            'alert_type': 'Test Alert',
            'alert_data': {'source_ip': '192.168.1.2', 'ports': [22, 80, 443]}
        }
        self.test_threat_data = {
            'timestamp': '2024-04-27 13:00:00',
            'source_ip': '192.168.1.3',
            'destination_ip': '10.0.0.1',
            'protocol': 'TCP',
            'threat_level': 0.8,
            'details': 'Possible port scan'
        }

    async def test_save_and_retrieve_alert(self):
        """Testuje zapisywanie i pobieranie alertu."""
        await self.db_handler.save_alert(self.test_alert_data)
        retrieved_alerts = await self.db_handler.get_recent_alerts(limit=1)
        self.assertEqual(len(retrieved_alerts), 1)
        retrieved_alert = retrieved_alerts[0]

        self.assertEqual(retrieved_alert['timestamp'], self.test_alert_data['timestamp'])
        self.assertEqual(retrieved_alert['alert_type'], self.test_alert_data['alert_type'])
        self.assertEqual(retrieved_alert['alert_data'], self.test_alert_data['alert_data'])

    async def test_save_and_retrieve_threat(self):
        """Testuje zapisywanie i pobieranie zagrożenia."""
        await self.db_handler.save_threat(self.test_threat_data)
        retrieved_threats = await self.db_handler.get_recent_threats(limit=1)
        self.assertEqual(len(retrieved_threats), 1)
        retrieved_threat = retrieved_threats[0]

        self.assertEqual(retrieved_threat['timestamp'], self.test_threat_data['timestamp'])
        self.assertEqual(retrieved_threat['source_ip'], self.test_threat_data['source_ip'])
        self.assertEqual(retrieved_threat['destination_ip'], self.test_threat_data['destination_ip'])
        self.assertEqual(retrieved_threat['protocol'], self.test_threat_data['protocol'])
        self.assertEqual(retrieved_threat['threat_level'], self.test_threat_data['threat_level'])
        self.assertEqual(retrieved_threat['details'], self.test_threat_data['details'])

    async def test_get_recent_alerts_limit(self):
        """Testuje pobieranie alertów z limitem."""
        for i in range(5):
            alert_data = {
                'timestamp': f'2024-01-01 13:00:{i:02}',
                'alert_type': 'Port Scan',
                'alert_data': {'source_ip': f'192.168.1.{i}', 'ports': [22, 80, 443]}
            }
            await self.db_handler.save_alert(alert_data)

        limited_alerts = await self.db_handler.get_recent_alerts(limit=3)
        self.assertEqual(len(limited_alerts), 3)

    async def test_get_recent_alerts_empty(self):
        """Testuje pobieranie alertów, gdy baza jest pusta."""
        alerts = await self.db_handler.get_recent_alerts()
        self.assertEqual(alerts, [])

    async def asyncTearDown(self):
        """Czyści bazę danych po każdym teście."""
        await self.db_handler.close()
        os.remove(self.db_path)

if __name__ == '__main__':
    unittest.main()
