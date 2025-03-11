# test_sniffer.py
from network.advanced_traffic_monitor import AdvancedTrafficMonitor
from unittest.mock import MagicMock, patch

def test_advanced_traffic_monitor_init():
    """Test inicjalizacji monitora ruchu z weryfikacją konfiguracji."""
    mock_config = {
        "monitoring_interval": 5,
        "interface": "eth0",
        "max_packets": 1000
    }
    mock_analyzer = MagicMock()
    
    with patch("network.advanced_traffic_monitor.AsyncSniffer") as mock_sniffer:
        monitor = AdvancedTrafficMonitor(mock_config, mock_analyzer)
        
        assert monitor.config == mock_config
        assert monitor.analyzer == mock_analyzer
        mock_sniffer.assert_called_once_with(
            iface="eth0",
            prn=monitor.process_packet,
            count=1000
        )