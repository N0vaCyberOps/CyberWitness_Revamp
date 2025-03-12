import pytest
from unittest.mock import AsyncMock
from network.threat_detector import ThreatDetector

@pytest.mark.asyncio
async def test_full_detection_flow():
    mock_intel = AsyncMock()
    mock_logger = AsyncMock()
    detector = ThreatDetector(mock_intel, mock_logger)
    
    # Symulacja złośliwego pakietu
    malicious_packet = Ether()/IP()/TCP(flags="S")  # SYN scan
    
    await detector.process_packet(malicious_packet)
    
    # Weryfikacja czy logowanie zostało wywołane
    mock_logger.log_event.assert_awaited()
    assert "syn_scan" in mock_logger.log_event.call_args[0][0]