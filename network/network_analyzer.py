@pytest.mark.asyncio
async def test_network_analyzer_non_ip_packet(monkeypatch, caplog):
    """Tests handling of packets without an IP layer."""
    caplog.set_level(logging.INFO)
    test_packet = Ether()  # No IP

    def mock_sniff(*args, **kwargs):
        kwargs['prn'](test_packet)

    monkeypatch.setattr("modules.network_analyzer.sniff", mock_sniff)
    analyzer = NetworkAnalyzer()

    captured_packets = await analyzer.capture_and_analyze(count=1)

    assert "Non-IP packet" in caplog.text
    assert captured_packets[0]["type"] == "Non-IP"

@pytest.mark.asyncio
async def test_network_analyzer_capture_error(monkeypatch, caplog):
    """Simulates a failure in sniffing packets."""
    caplog.set_level(logging.INFO)

    def mock_sniff(*args, **kwargs):
        raise Exception("Sniffing failed")

    monkeypatch.setattr("modules.network_analyzer.sniff", mock_sniff)
    analyzer = NetworkAnalyzer()

    captured_packets = await analyzer.capture_and_analyze(count=1)

    assert "Packet capture failed" in caplog.text
    assert captured_packets == []
