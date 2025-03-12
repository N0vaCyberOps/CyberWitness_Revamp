# alert_manager.py
import unittest
import asyncio
import os
import json
import pytest
from alerts.alert_manager import AlertManager

class TestAlertManager(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.am = AlertManager(config_path="test_config.ini")
        await self.am.init_db()

    async def test_send_alert(self):
        test_alert = {
            "source_ip": "192.168.1.2",
            "destination_ip": "10.0.0.1",
            "protocol": "TCP",
            "threat_level": 0.9
        }
        
        await self.am.send_alert("THREAT_DETECTED", test_alert)
        alerts = await self.am.get_latest_alerts(limit=1)

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["alert_type"], "THREAT_DETECTED")
        self.assertEqual(json.loads(alerts[0]["details"]), test_alert)  # Bezpieczniejsze parsowanie

    async def asyncTearDown(self):
        if self.am and os.path.exists(self.am.db_path):
            await self.am.close()  # Zamknięcie połączenia z bazą
            os.remove(self.am.db_path)