import pytest
import logging
from scapy.all import Ether, IP, TCP
from modules.network_analyzer import NetworkAnalyzer

@pytest.mark.asyncio
async def test_network_analyzer_capture(monkeypatch, caplog):
    caplog.set_level(logging.INFO)
    test_packet = Ether()/IP(src="1.1.1.1", dst="2.2.2.2")/TCP(sport=1234, dport=80)

    def mock_sniff(*args, **kwargs):
        kwargs['prn'](test_packet)

    monkeypatch.setattr("modules.network_analyzer.sniff", mock_sniff)
    analyzer = NetworkAnalyzer()

    await analyzer.capture_and_analyze(count=1)

    assert "TCP Packet: 1.1.1.1:1234 -> 2.2.2.2:80" in caplog.text
