from scapy.all import sniff, IP, TCP, UDP
from utils.log_event import log_event

class NetworkAnalyzer:
    """Moduł do analizy pakietów sieciowych."""
    
    def analyze_packet(self, packet):
        """Analizuje pojedynczy pakiet sieciowy."""
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            log_event("NETWORK", f"Pakiet z {src_ip} do {dst_ip}")

            if TCP in packet:
                log_event("NETWORK", f"TCP: {src_ip}:{packet[TCP].sport} -> {dst_ip}:{packet[TCP].dport}")
            elif UDP in packet:
                log_event("NETWORK", f"UDP: {src_ip}:{packet[UDP].sport} -> {dst_ip}:{packet[UDP].dport}")

    def capture_and_analyze(self, count=10):
        """Przechwytuje pakiety i analizuje je."""
        sniff(prn=self.analyze_packet, count=count, store=False)
