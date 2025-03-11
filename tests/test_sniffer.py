import pytest
from unittest.mock import MagicMock
from network.advanced_traffic_monitor import AdvancedTrafficMonitor

@pytest.fixture
def mock_analyzer():
    return MagicMock()

@pytest.fixture
def mock_config():
    return {"monitoring_interval": 5}

def test_advanced_traffic_monitor_init(mock_config, mock_analyzer):
    monitor = AdvancedTrafficMonitor(mock_config, mock_analyzer)
    assert monitor.config == mock_config
