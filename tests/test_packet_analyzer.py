import unittest
from unittest.mock import MagicMock, patch
from network.packet_analyzer import analyze_packet

class TestPacketAnalyzer(unittest.TestCase):
    def test_analyze_packet_tcp(self):
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
        self.assertEqual(result["src_port"], 1234)
        self.assertEqual(result["dst_port"], 80)

    def test_analyze_packet_icmp(self):
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

    # Analogiczne poprawki dla pozostałych testów