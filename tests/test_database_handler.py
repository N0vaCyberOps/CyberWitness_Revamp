# tests/test_database_handler.py
import unittest
import sqlite3
import os
import json
import tempfile  # Import tempfile
from database.database_handler import DatabaseHandler, init_db
import asyncio

class TestDatabaseHandler(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        """Create a temporary database for testing."""
        self.temp_db_file = tempfile.NamedTemporaryFile(delete=False)  # Create a temporary file
        self.db_path = self.temp_db_file.name
        self.temp_db_file.close()  # Close the file handle so init_db can use it
        init_db(self.db_path)  # Initialize the database
        self.config = {'database_file': self.db_path}
        self.db_handler = DatabaseHandler(self.config)

    async def test_save_and_retrieve_threat(self):
        """Test saving and retrieving threat data."""
        threat_data = {
            'timestamp': '2024-01-01 12:00:00',
            'source_ip': '192.168.1.1',
            'destination_ip': '10.0.0.1',
            'protocol': 'TCP',
            'threat_level': 0.8,
            'details': json.dumps({'type': 'SYN flood'})
        }
        await self.db_handler.save_threat(threat_data)
        retrieved_threats = await self.db_handler.get_recent_threats()
        self.assertEqual(len(retrieved_threats), 1)
        retrieved_threat = retrieved_threats[0]

        # Compare each field individually (because of the ID)
        self.assertEqual(retrieved_threat['timestamp'], threat_data['timestamp'])
        self.assertEqual(retrieved_threat['source_ip'], threat_data['source_ip'])
        self.assertEqual(retrieved_threat['destination_ip'], threat_data['destination_ip'])
        self.assertEqual(retrieved_threat['protocol'], threat_data['protocol'])
        self.assertEqual(retrieved_threat['threat_level'], threat_data['threat_level'])
        self.assertEqual(retrieved_threat['details'], threat_data['details'])


    async def test_save_and_retrieve_alert(self):
        """Test saving and retrieving alert data."""
        alert_data = {
            'timestamp': '2024-01-01 13:00:00',
            'alert_type': 'Port Scan',
            'alert_data': {'source_ip': '192.168.1.2', 'ports': [22, 80, 443]}
        }

        await self.db_handler.save_alert(alert_data)
        retrieved_alerts = await self.db_handler.get_recent_alerts()
        self.assertEqual(len(retrieved_alerts), 1)
        retrieved_alert = retrieved_alerts[0]

        # Compare individual fields
        self.assertEqual(retrieved_alert['timestamp'], alert_data['timestamp'])
        self.assertEqual(retrieved_alert['alert_type'], alert_data['alert_type'])
        self.assertEqual(retrieved_alert['alert_data'], alert_data['alert_data'])

    async def test_get_recent_threats_limit(self):
        # Save multiple threats
        for i in range(5):
            threat_data = {
                'timestamp': f'2024-01-01 12:00:{i:02}',
                'source_ip': '192.168.1.1',
                'destination_ip': '10.0.0.1',
                'protocol': 'TCP',
                'threat_level': 0.8,
                'details': json.dumps({'type': 'SYN flood'})
            }
            await self.db_handler.save_threat(threat_data)

        # Retrieve only 3 recent threats
        retrieved_threats = await self.db_handler.get_recent_threats(limit=3)
        self.assertEqual(len(retrieved_threats), 3)


    async def test_get_recent_alerts_limit(self):
         # Save multiple alerts
         for i in range(5):
             alert_data = {
                 'timestamp': f'2024-01-01 13:00:{i:02}',
                 'alert_type': 'Port Scan',
                 'alert_data': {'source_ip': '192.168.1.2', 'ports': [22, 80, 443]}
             }
             await self.db_handler.save_alert(alert_data)
         retrieved_alerts = await self.db_handler.get_recent_alerts(limit=2)
         self.assertEqual(len(retrieved_alerts), 2)

    async def asyncTearDown(self):
        """Clean up the temporary database after each test."""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

if __name__ == '__main__':
    unittest.main()