import unittest
from unittest.mock import MagicMock
from network.packet_analyzer import analyze_packet
from scapy.all import IP, TCP, UDP

class TestPacketAnalyzer(unittest.TestCase):

    def test_analyze_packet_tcp(self):
        """Testuje analizę pakietu TCP."""
        mock_packet = MagicMock()
        mock_packet.haslayer.side_effect = [True, True, False, False]
        mock_packet[IP].src = "192.168.1.1"
        mock_packet[IP].dst = "192.168.1.2"
        mock_packet[TCP].sport = 1234
        mock_packet[TCP].dport = 80

        result = analyze_packet(mock_packet)
        self.assertEqual(result, "TCP Packet: 192.168.1.1:1234 -> 192.168.1.2:80")

    def test_analyze_packet_udp(self):
        """Testuje analizę pakietu UDP."""
        mock_packet = MagicMock()
        mock_packet.haslayer.side_effect = [True, False, True, False]
        mock_packet[IP].src = "192.168.1.1"
        mock_packet[IP].dst = "192.168.1.2"
        mock_packet[UDP].sport = 5353
        mock_packet[UDP].dport = 53

        result = analyze_packet(mock_packet)
        self.assertEqual(result, "UDP Packet: 192.168.1.1:5353 -> 192.168.1.2:53")

    def test_analyze_packet_icmp(self):
        """Testuje analizę pakietu ICMP."""
        mock_packet = MagicMock()
        mock_packet.haslayer.side_effect = [True, False, False, True]
        mock_packet[IP].src = "192.168.1.1"
        mock_packet[IP].dst = "192.168.1.2"

        result = analyze_packet(mock_packet)
        self.assertEqual(result, "ICMP Packet: 192.168.1.1 -> 192.168.1.2")

    def test_analyze_packet_unknown(self):
        """Testuje analizę nieznanego pakietu."""
        mock_packet = MagicMock()
        mock_packet.haslayer.return_value = False

        result = analyze_packet(mock_packet)
        self.assertEqual(result, "Unknown packet type")
