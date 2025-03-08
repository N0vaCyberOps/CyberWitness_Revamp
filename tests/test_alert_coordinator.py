import unittest
from unittest.mock import AsyncMock, patch
from alerts.alert_coordinator import AlertCoordinator
from database.database_handler import DatabaseHandler

class TestAlertCoordinator(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        """Konfiguracja testowa."""
        self.mock_db_handler = AsyncMock(spec=DatabaseHandler)
        self.alert_coordinator = AlertCoordinator(self.mock_db_handler)

    async def test_handle_alert_database_error(self):
        """Test obsługi błędu bazy danych przy zapisie alertu."""
        self.mock_db_handler.save_alert.side_effect = Exception("Simulated database error")

        alert_data = {
            "timestamp": "2024-07-28 11:00:00",
            "source_ip": "192.168.1.100",
            "destination_ip": "192.168.1.200",
            "protocol": "TCP",
            "threat_level": 0.8,
            "details": "Test alert"
        }

        with self.assertRaises(Exception) as context:
            await self.alert_coordinator.handle_alert(alert_data)

        self.assertEqual(str(context.exception), "Simulated database error")

    async def test_handle_alert_success(self):
        """Test poprawnego przetwarzania alertu."""
        alert_data = {
            "timestamp": "2024-07-28 11:00:00",
            "source_ip": "192.168.1.100",
            "destination_ip": "192.168.1.200",
            "protocol": "TCP",
            "threat_level": 0.8,
            "details": "Test alert"
        }

        await self.alert_coordinator.handle_alert(alert_data)
        self.mock_db_handler.save_alert.assert_called_once_with(alert_data)

if __name__ == "__main__":
    unittest.main()
