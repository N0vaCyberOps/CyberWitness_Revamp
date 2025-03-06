import unittest
from unittest.mock import AsyncMock
from alerts.alert_coordinator import AlertCoordinator
from database.database_handler import DatabaseHandler  # Import DatabaseHandler


class TestAlertCoordinator(unittest.IsolatedAsyncioTestCase):  # Use IsolatedAsyncioTestCase

    async def test_handle_alert_success(self):
        """Test successful handling of an alert."""
        mock_db_handler = AsyncMock(spec=DatabaseHandler)  # Use spec to ensure correct interface
        alert_coordinator = AlertCoordinator(mock_db_handler)
        alert_data = {
            'timestamp': '2024-07-28 11:00:00',
            'alert_type': 'Test',
            'alert_data': {'message': 'Test alert'}
        }
        await alert_coordinator.handle_alert(alert_data)
        mock_db_handler.save_alert.assert_awaited_once_with(alert_data)

    async def test_handle_alert_invalid_input_type(self):
        """Test handling an alert with invalid input type."""
        mock_db_handler = AsyncMock(spec=DatabaseHandler)
        alert_coordinator = AlertCoordinator(mock_db_handler)
        with self.assertRaises(TypeError):
            await alert_coordinator.handle_alert("invalid input")  # Pass a string instead of a dict

    async def test_handle_alert_missing_keys(self):
        """Test handling an alert with missing keys in the data."""
        mock_db_handler = AsyncMock(spec=DatabaseHandler)
        alert_coordinator = AlertCoordinator(mock_db_handler)
        alert_data = {'timestamp': '2024-07-28 11:00:00'}  # Missing 'alert_type' and 'alert_data'
        with self.assertRaises(ValueError):
            await alert_coordinator.handle_alert(alert_data)

    async def