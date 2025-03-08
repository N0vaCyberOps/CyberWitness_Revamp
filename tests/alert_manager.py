import unittest
import asyncio
import os
from alerts.alert_manager import AlertManager

class TestAlertManager(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        """Tworzy instancję AlertManager przed każdym testem."""
        self.am = AlertManager(config_path="test_config.ini")
        await self.am.init_db()  # Tworzy testową bazę

    async def test_send_alert(self):
        """Testuje wysyłanie alertu i zapis do bazy."""
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
        self.assertEqual(eval(alerts[0]["details"]), test_alert)  # Bez eval()!

    async def asyncTearDown(self):
        """Usuwa testową bazę danych po każdym teście."""
        if os.path.exists(self.am.db_path):
            os.remove(self.am.db_path)

if __name__ == '__main__':
    unittest.main()
