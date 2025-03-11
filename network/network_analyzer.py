from scapy.all import sniff, IP, TCP, UDP
from prometheus_client import Counter
from utils.log_event import log_event

packets_analyzed = Counter("packets_analyzed", "Liczba przechwyconych pakietów")

class NetworkAnalyzer:
    """Przechwytuje i analizuje ruch sieciowy."""

    def analyze_packet(self, packet):
        """Analizuje pakiet i loguje jego dane."""
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            log_event("INFO", f"📡 Pakiet: {src_ip} -> {dst_ip}")
            packets_analyzed.inc()

    def capture_and_analyze(self, count=10):
        """Przechwytuje pakiety i analizuje je."""
        log_event("INFO", f"📡 Rozpoczynam przechwytywanie {count} pakietów...")
        sniff(prn=self.analyze_packet, count=count, store=False)
