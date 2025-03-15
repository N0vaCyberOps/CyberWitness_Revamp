import scapy.all as scapy
import logging
import re
from collections import defaultdict
from datetime import datetime

logger = logging.getLogger(__name__)

class PacketAnalyzer:
    def __init__(self, db, alert_coordinator):
        self.db = db
        self.alert = alert_coordinator
        self.syn_counts = defaultdict(int)
        self.thresholds = {'SYN_FLOOD': 100}
        self.sql_regex = re.compile(r"(UNION SELECT|SELECT.+FROM|INSERT INTO|DROP TABLE|--)" , re.IGNORECASE)
        self.xss_pattern = re.compile(r"(<script.*?>.*?</script>|onerror=|onload=)", re.IGNORECASE)
        self.last_reset = datetime.now()

    def process_packet(self, packet):
        if scapy.TCP in packet:
            self._check_syn_flood(packet)
            self._deep_packet_inspection(packet)

        self._reset_counters_if_needed()

    def _check_syn_flood(self, packet):
        if packet[scapy.TCP].flags == 'S':
            src = packet[scapy.IP].src
            self.syn_counts[src] += 1
            if self.syn_counts[src] > self.thresholds['SYN_FLOOD']:
                self.alert.trigger_alert("SYN Flood", f"Source: {src}", "CRITICAL")
                self.syn_counts[src] = 0

    def _deep_packet_inspection(self, packet):
        payload = bytes(packet[scapy.Raw].load).decode(errors='ignore') if scapy.Raw in packet else ''

        # SQL Injection detection
        if self.sql_regex_search(payload=payload):
            src = packet[scapy.IP].src
            self.alert_coordinator.trigger_alert(
                title="SQL Injection Attempt",
                details=f"Malicious payload detected from {src}",
                severity="HIGH"
            )

        # XSS detection
        if self.xss_pattern.search(payload):
            src = packet[scapy.IP].src
            self.alert_coordinator.trigger_alert(
                title="XSS Attempt",
                details=f"Possible XSS attack detected from {src}",
                severity="HIGH"
            )

    def sql_injection_detected(self, payload: str) -> bool:
        return bool(self.sql_pattern.search(payload))

    def xss_detected(self, payload: str) -> bool:
        return bool(self.xss_pattern.search(payload))

    def _reset_counters(self):
        self.syn_counts = defaultdict(int)
        self.last_reset = datetime.now()
