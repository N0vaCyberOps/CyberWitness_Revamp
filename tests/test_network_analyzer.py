import pytest
import asyncio
from unittest.mock import patch, MagicMock
from modules.network_analyzer import NetworkAnalyzer
from scapy.all import Ether, IP, TCP

@pytest.mark.asyncio
async def test_buffer_management():
    """Test przepełnienia bufora"""
    analyzer = NetworkAnalyzer(max_buffer_size=2)
    
    mock_packet1 = Ether()/IP(src="1.1.1.1", dst="2.2.2.2")/TCP()
    mock_packet2 = Ether()/IP(src="3.3.3.3", dst="4.4.4.4")/TCP()
    mock_packet3 = Ether()/IP(src="5.5.5.5", dst="6.6.6.6")/TCP()

    with patch("modules.network_analyzer.sniff") as mock_sniff:
        mock_sniff.side_effect = lambda *args, **kwargs: [
            kwargs['prn'](mock_packet1),
            kwargs['prn'](mock_packet2),
            kwargs['prn'](mock_packet3)
        ]
        
        result = await analyzer.capture_and_analyze(count=3)
        assert len(result) == 2
        assert result[0]["src_ip"] == "3.3.3.3"

@pytest.mark.asyncio
async def test_stop_capture():
    """Test przedwczesnego zatrzymania przechwytywania"""
    analyzer = NetworkAnalyzer()
    
    with patch("modules.network_analyzer.sniff") as mock_sniff:
        mock_sniff.side_effect = lambda *args, **kwargs: [
            kwargs['prn'](Ether()/IP()/TCP()) for _ in range(5)
        ]
        
        task = asyncio.create_task(analyzer.capture_and_analyze(count=10))
        await asyncio.sleep(0.1)
        analyzer.stop_capture()
        
        result = await task
        assert 0 < len(result) < 10

@pytest.mark.asyncio
async def test_non_ip_packets():
    """Test przechwytywania pakietów nie-IP"""
    analyzer = NetworkAnalyzer()
    
    mock_packet = Ether()/TCP()  # Brak warstwy IP
    
    with patch("modules.network_analyzer.sniff") as mock_sniff:
        mock_sniff.side_effect = lambda *args, **kwargs: [
            kwargs['prn'](mock_packet)
        ]
        
        result = await analyzer.capture_and_analyze(count=1)
        assert result[0]["type"] == "Non-IP"