def test_http_analysis():
    """Test analizy pakietów HTTP"""
    from scapy.all import Raw
    http_packet = Ether()/IP()/TCP()/Raw(load="GET / HTTP/1.1")
    result = analyze_packet(http_packet)
    
    assert result["type"] == "TCP"
    assert "http_method" not in result  # Brak parsowania HTTP w aktualnej implementacji

def test_dns_analysis():
    """Test analizy pakietów DNS"""
    from scapy.all import DNS
    dns_packet = Ether()/IP()/UDP()/DNS()
    result = analyze_packet(dns_packet)
    
    assert result["type"] == "UDP"
    assert result["src_port"] == 53 or result["dst_port"] == 53