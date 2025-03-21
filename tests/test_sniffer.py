import pytest
from unittest.mock import MagicMock, patch
import asyncio
from network.advanced_traffic_monitor import AdvancedTrafficMonitor

@pytest.mark.asyncio
async def test_sniffer_lifecycle():
    """Test pełnego cyklu życia monitora ruchu"""
    mock_config = {
        "interface": "eth0",
        "filter": "tcp port 80"
    }
    
    mock_analyzer = MagicMock()
    monitor = AdvancedTrafficMonitor(mock_config, mock_analyzer)

    # Poprawiony target mocka
    with patch("network.advanced_traffic_monitor.AsyncSniffer") as mock_sniffer:
        mock_instance = mock_sniffer.return_value
        mock_instance.start = MagicMock()

        # Test uruchomienia
        await monitor.start_monitoring()
        await asyncio.sleep(0.1)  # Opóźnienie dla operacji asynchronicznych

        # Weryfikacje
        assert monitor._running is True
        mock_sniffer.assert_called_once_with(
            iface="eth0",
            filter="tcp port 80",
            prn=mock_analyzer,
            store=False
        )
        mock_instance.start.assert_called_once()

        # Test zatrzymania
        await monitor.stop_monitoring()
        await asyncio.sleep(0.1)
        assert monitor._running is False
        mock_instance.stop.assert_called_once()

@pytest.mark.asyncio
async def test_sniffer_error_handling():
    """Test obsługi błędów inicjalizacji"""
    mock_config = {"interface": "invalid_interface"}
    monitor = AdvancedTrafficMonitor(mock_config, lambda x: x)

    # Poprawiony target mocka
    with patch("network.advanced_traffic_monitor.AsyncSniffer.start", side_effect=Exception("Test error")):
        with pytest.raises(Exception, match="Test error"):
            await monitor.start_monitoring()
        await asyncio.sleep(0.1)
        assert monitor._running is False