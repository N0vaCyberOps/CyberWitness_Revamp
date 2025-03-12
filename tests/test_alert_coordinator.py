import pytest
from unittest.mock import AsyncMock
from network.alert_coordinator import AlertCoordinator

@pytest.mark.asyncio
async def test_handle_alert_database_error():
    mock_db = AsyncMock()
    mock_db.save_alert = AsyncMock(side_effect=Exception("Simulated error"))

    coordinator = AlertCoordinator(mock_db)
    test_data = {
        "timestamp": "2024-07-28 11:00:00",
        "source_ip": "192.168.1.100",
        "threat_level": 0.8
    }

    with pytest.raises(Exception, match="Simulated error"):  # ✅ Oczekujemy wyjątku
        await coordinator.handle_alert(test_data)
