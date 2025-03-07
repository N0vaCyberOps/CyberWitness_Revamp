import unittest
from unittest.mock import AsyncMock, MagicMock
from alerts.alert_coordinator import AlertCoordinator
from database.database_handler import DatabaseHandler


class TestAlertCoordinator(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        """Set up for each test."""
        self.mock_db_handler = AsyncMock(spec=DatabaseHandler)
        self.coordinator = AlertCoordinator(self.mock_db_handler)

    async def test_handle_alert_success(self):
        """Test successful handling of an alert."""
        alert_data = {
            'timestamp': '2024-07-28 11:00:00',
            'source_ip': '192.168.1.1',
            'destination_ip': '10.0.0.1',
            'protocol': 'TCP',
            'threat_level': 'high',
            'details': 'Possible port scan'
        }
        await self.coordinator.handle_alert(alert_data)
        self.mock_db_handler.save_alert.assert_awaited_once_with(alert_data)

    async def test_handle_alert_invalid_input_type(self):
        """Test handling an alert with invalid input type."""
        with self.assertRaises(TypeError):
            await self.coordinator.handle_alert("invalid input")

    async def test_handle_alert_missing_keys(self):
        """Test handling an alert with missing keys."""
        alert_data = {'timestamp': '2024-07-28 11:00:00'}  # Missing keys
        with self.assertRaises(ValueError):
            await self.coordinator.handle_alert(alert_data)

    async def test_handle_alert_database_error(self):
        """Test handling a database error."""
        self.mock_db_handler.save_alert.side_effect = Exception("Simulated database error")
        alert_data = {
            'timestamp': '2024-07-28 11:00:00',
            'source_ip': '192.168.1.1',
            'destination_ip': '10.0.0.1',
            'protocol': 'TCP',
            'threat_level': 'high',
            'details': 'Possible port scan'
        }
        with self.assertRaises(Exception) as context:
            await self.coordinator.handle_alert(alert_data)
        self.assertEqual(str(context.exception), "Simulated database error")
        self.mock_db_handler.save_alert.assert_awaited_once_with(alert_data)

    def test_invalid_db_handler_initialization(self):
        """Test initialization with an invalid db_handler type."""
        with self.assertRaises(TypeError):
            AlertCoordinator("not a db handler")


if __name__ == '__main__':
    unittest.main()