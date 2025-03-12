def test_malformed_packets():
    """Test analizy uszkodzonych pakietów"""
    malformed_packet = MagicMock()
    malformed_packet.haslayer.side_effect = Exception("Corrupted packet")
    
    result = analyze_packet(malformed_packet)
    assert "error" in result
    assert "Corrupted packet" in result["error"]

def test_vlan_handling():
    """Test obsługi pakietów VLAN"""
    from scapy.all import Dot1Q
    packet = Ether()/Dot1Q()/IP()/TCP()
    
    result = analyze_packet(packet)
    assert result["src_ip"] == packet[IP].src
    assert "vlan" not in result  # Sprawdź czy nie ma błędów parsowania