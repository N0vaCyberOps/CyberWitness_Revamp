import unittest
import scapy.all as scapy
from network.packet_analyzer import analyze_packet  # Corrected import
import os
import sqlite3
import json

class TestPacketAnalyzer(unittest.IsolatedAsyncioTestCase):  # Use IsolatedAsyncioTestCase

    async def test_analyze_packet_tcp_syn_flood(self):
        # Stwórz pakiet TCP SYN (bez ACK)
        packet = scapy.IP(src="192.168.1.100", dst="192.168.1.200") / scapy.TCP(sport=12345, dport=80, flags="S")
        result = await analyze_packet(packet)
        self.assertIsNotNone(result)  # Sprawdź, czy wykryto zagrożenie
        self.assertGreater(result['threat_level'], 0.5)  # Sprawdź, czy threat_level jest wysoki
        self.assertEqual(result['protocol'], "TCP")


    async def test_analyze_packet_normal_tcp(self):
        # Stwórz "normalny" pakiet TCP
        packet = scapy.IP(src="192.168.1.100", dst="192.168.1.200") / scapy.TCP(sport=12345, dport=80, flags="A")  # ACK
        result = await analyze_packet(packet)
        self.assertIsNone(result)  # Nie powinno być zagrożenia


    async def test_analyze_packet_udp(self):
          packet = scapy.IP(src="192.168.1.100", dst="192.168.1.200") / scapy.UDP(sport=12345, dport=53)
          result = await analyze_packet(packet)
          self.assertIsNotNone(result)  # Sprawdź, czy wykryto zagrożenie (może być, ale niskie)

    async def test_analyze_packet_with_malware(self):
        packet = scapy.IP(src="192.168.1.100", dst="192.168.1.200") / scapy.TCP(sport=12345, dport=80, flags="PA") / b"This is some malware data"
        result = await analyze_packet(packet)
        self.assertIsNotNone(result)
        self.assertGreater(result['threat_level'], 0.7)
        self.assertIn("payload", result['details']) # Sprawdź, czy wykryto payload


if __name__ == '__main__':
    unittest.main()