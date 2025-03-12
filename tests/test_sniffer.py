import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from network.advanced_traffic_monitor import AdvancedTrafficMonitor

@pytest.mark.asyncio
async def test_sniffer_lifecycle():
    """Test pełnego cyklu życia monitora ruchu."""
    mock_config = {
        "interface": "eth0",
        "filter": "tcp port 80",
        "monitoring_interval": 1
    }
    
    mock_analyzer = MagicMock()
    monitor = AdvancedTrafficMonitor(mock_config, mock_analyzer)

    with patch("scapy.all.AsyncSniffer") as mock_sniffer:
        # Test uruchomienia
        await monitor.start_monitoring()
        assert monitor._running is True
        mock_sniffer.assert_called_once_with(
            iface="eth0",
            filter="tcp port 80",
            prn=mock_analyzer,
            store=False
        )

        # Test zatrzymania
        await monitor.stop_monitoring()
        assert monitor._running is False
        mock_sniffer.return_value.stop.assert_called_once()

@pytest.mark.asyncio
async def test_sniffer_error_handling():
    """Test obsługi błędów podczas uruchamiania."""
    mock_config = {"interface": "invalid_interface"}
    monitor = AdvancedTrafficMonitor(mock_config, lambda x: x)

    with patch("scapy.all.AsyncSniffer.start", side_effect=Exception("Test error")):
        with pytest.raises(Exception, match="Test error"):
            await monitor.start_monitoring()
        assert monitor._running is False