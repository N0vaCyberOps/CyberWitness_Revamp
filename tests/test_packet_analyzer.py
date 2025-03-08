import unittest
from unittest.mock import patch
from network.packet_analyzer import analyze_packet
import scapy.all as scapy

class TestPacketAnalyzer(unittest.IsolatedAsyncioTestCase):

    async def test_analyze_packet_tcp_syn_flood(self):
        """Test wykrywania ataku SYN Flood."""
        packet = scapy.IP(src="192.168.1.100", dst="192.168.1.200") / scapy.TCP(sport=12345, dport=80, flags="S")
        
        with patch("network.packet_analyzer.detect_attack", return_value="SYN_FLOOD") as mock_detect:
            result = await analyze_packet(packet)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["alert_type"], "SYN_FLOOD")
        mock_detect.assert_called_once()

    async def test_analyze_packet_udp(self):
        """Test analizy pakietu UDP."""
        packet = scapy.IP(src="192.168.1.100", dst="192.168.1.200") / scapy.UDP(sport=12345, dport=53)
        
        with patch("network.packet_analyzer.detect_attack", return_value=None) as mock_detect:
            result = await analyze_packet(packet)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["protocol"], "UDP")
        mock_detect.assert_called_once()

if __name__ == "__main__":
    unittest.main()
