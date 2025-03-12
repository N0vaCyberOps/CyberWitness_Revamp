import unittest
from unittest.mock import MagicMock
from scapy.all import IP, TCP, UDP, ICMP  # DODANE IMPORTY
from network.packet_analyzer import analyze_packet

class TestPacketAnalyzer(unittest.TestCase):
    def test_analyze_packet_tcp(self):
        """Testuje analizę pakietu TCP."""
        mock_packet = MagicMock()
        mock_packet.haslayer.side_effect = lambda x: {
            IP: True,
            TCP: True,
            UDP: False,
            ICMP: False
        }[x]
        mock_packet[IP].src = "192.168.1.1"
        mock_packet[IP].dst = "192.168.1.2"
        mock_packet[TCP].sport = 1234
        mock_packet[TCP].dport = 80

        result = analyze_packet(mock_packet)
        self.assertEqual(result["type"], "TCP")
        self.assertEqual(result["src_ip"], "192.168.1.1")
        self.assertEqual(result["dst_ip"], "192.168.1.2")
        self.assertEqual(result["src_port"], 1234)
        self.assertEqual(result["dst_port"], 80)

    def test_analyze_packet_icmp(self):
        """Testuje analizę pakietu ICMP."""
        mock_packet = MagicMock()
        mock_packet.haslayer.side_effect = lambda x: {
            IP: True,
            TCP: False,
            UDP: False,
            ICMP: True
        }[x]
        mock_packet[IP].src = "192.168.1.1"
        mock_packet[IP].dst = "192.168.1.2"

        result = analyze_packet(mock_packet)
        self.assertEqual(result["type"], "ICMP")
        self.assertEqual(result["src_ip"], "192.168.1.1")
        self.assertEqual(result["dst_ip"], "192.168.1.2")

    def test_analyze_packet_udp(self):
        """Testuje analizę pakietu UDP."""
        mock_packet = MagicMock()
        mock_packet.haslayer.side_effect = lambda x: {
            IP: True,
            TCP: False,
            UDP: True,
            ICMP: False
        }[x]
        mock_packet[IP].src = "192.168.1.1"
        mock_packet[IP].dst = "192.168.1.2"
        mock_packet[UDP].sport = 5353
        mock_packet[UDP].dport = 53

        result = analyze_packet(mock_packet)
        self.assertEqual(result["type"], "UDP")
        self.assertEqual(result["src_port"], 5353)
        self.assertEqual(result["dst_port"], 53)

    def test_analyze_packet_unknown(self):
        """Testuje analizę nieznanego pakietu."""
        mock_packet = MagicMock()
        mock_packet.haslayer.return_value = False

        result = analyze_packet(mock_packet)
        self.assertEqual(result["type"], "Non-IP")