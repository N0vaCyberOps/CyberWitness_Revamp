import pytest
from unittest.mock import AsyncMock
from alerts.alert_coordinator import AlertCoordinator

class TestAlertCoordinator:
    @pytest.mark.asyncio
    async def test_handle_alert_database_error(self):
        """Test obsługi błędu bazy danych przy zapisie alertu."""
        mock_db_handler = AsyncMock()
        mock_db_handler.save_alert.side_effect = Exception("Simulated database error")
        alert_coordinator = AlertCoordinator(mock_db_handler)

        alert_data = {
            "timestamp": "2024-07-28 11:00:00",
            "source_ip": "192.168.1.100",
            "destination_ip": "192.168.1.200",
            "protocol": "TCP",
            "threat_level": 0.8,
            "details": "Test alert"
        }

        with pytest.raises(Exception, match="Simulated database error"):
            await alert_coordinator.handle_alert(alert_data)
