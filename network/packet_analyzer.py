import scapy.all as scapy
import libinjection
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

class PacketAnalyzer:
    def __init__(self, db, alert_coordinator):
        self.db = db
        self.alert = alert_coordinator
        self.syn_counts = defaultdict(int)
        self.thresholds = {'SYN_FLOOD': 100}

    def process_packet(self, packet):
        if scapy.TCP in packet:
            self._check_syn_flood(packet)
            self._deep_packet_inspection(packet)

    def _check_syn_flood(self, packet):
        if packet[scapy.TCP].flags == 'S':
            src = packet[scapy.IP].src
            self.syn_counts[src] += 1
            if self.syn_counts[src] > self.thresholds['SYN_FLOOD']:
                self.alert.trigger_alert("SYN Flood", f"Source: {src}", "CRITICAL")
                self.syn_counts[src] = 0

    def _deep_packet_inspection(self, packet):
        if scapy.Raw in packet:
            payload = bytes(packet[scapy.Raw].load).decode(errors='replace')
            if libinjection.detect_sqli(payload):
                self.alert.trigger_alert("SQLi Attempt", payload[:100], "HIGH")
            elif any(pattern in payload for pattern in ("<script>", "onerror=")):
                self.alert.trigger_alert("XSS Attempt", payload[:100], "HIGH")