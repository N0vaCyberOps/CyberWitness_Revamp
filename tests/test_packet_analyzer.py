import unittest
from scapy.all import Ether, IP, TCP, UDP, ICMP, DNS, Raw
from network.packet_analyzer import analyze_packet

class TestPacketAnalyzer(unittest.TestCase):
    def test_analyze_packet_tcp(self):
        """Test analizy pakietu TCP"""
        packet = Ether()/IP(src="192.168.1.1", dst="192.168.1.2")/TCP(sport=1234, dport=80)
        result = analyze_packet(packet)
        
        self.assertEqual(result["type"], "TCP")
        self.assertEqual(result["src_ip"], "192.168.1.1")
        self.assertEqual(result["dst_ip"], "192.168.1.2")
        self.assertEqual(result["src_port"], 1234)
        self.assertEqual(result["dst_port"], 80)

    def test_analyze_packet_icmp(self):
        """Test analizy pakietu ICMP"""
        packet = Ether()/IP(src="10.0.0.1", dst="10.0.0.2")/ICMP()
        result = analyze_packet(packet)
        
        self.assertEqual(result["type"], "ICMP")
        self.assertEqual(result["src_ip"], "10.0.0.1")
        self.assertEqual(result["dst_ip"], "10.0.0.2")

    def test_analyze_packet_udp(self):
        """Test analizy pakietu UDP"""
        packet = Ether()/IP(src="172.16.0.1", dst="172.16.0.2")/UDP(sport=5353, dport=53)
        result = analyze_packet(packet)
        
        self.assertEqual(result["type"], "UDP")
        self.assertEqual(result["src_port"], 5353)
        self.assertEqual(result["dst_port"], 53)

    def test_analyze_packet_unknown(self):
        """Test analizy nieznanego pakietu"""
        packet = Ether()/TCP()  # Brak warstwy IP
        result = analyze_packet(packet)
        self.assertEqual(result["type"], "Non-IP")

    def test_dns_analysis(self):
        """Test analizy pakietów DNS"""
        packet = Ether()/IP()/UDP()/DNS()
        result = analyze_packet(packet)
        self.assertEqual(result["type"], "UDP")

    def test_http_analysis(self):
        """Test analizy pakietów HTTP"""
        packet = Ether()/IP()/TCP()/Raw(load="GET / HTTP/1.1")
        result = analyze_packet(packet)
        self.assertEqual(result["type"], "TCP")

if __name__ == '__main__':
    unittest.main()