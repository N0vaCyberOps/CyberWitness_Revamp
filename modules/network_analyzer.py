from scapy.all import sniff, IP, TCP, UDP, ICMP
from utils.log_event import log_event

class NetworkAnalyzer:
    def __init__(self):
        """Inicjalizacja analizatora sieciowego."""
        pass

    async def capture_and_analyze(self, count=10):
        """Przechwytuje i analizuje pakiety sieciowe."""
        packets = sniff(prn=self.analyze_packet, count=count, store=False)
        return packets  # ✅ Dodano return, aby uniknąć TypeError

    def analyze_packet(self, packet):
        """Analizuje pakiet i loguje wynik."""
        if packet.haslayer(IP):
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            if packet.haslayer(TCP):
                sport, dport = packet[TCP].sport, packet[TCP].dport
                log_event("NETWORK", f"TCP: {src_ip}:{sport} -> {dst_ip}:{dport}")
            elif packet.haslayer(UDP):
                sport, dport = packet[UDP].sport, packet[UDP].dport
                log_event("NETWORK", f"UDP: {src_ip}:{sport} -> {dst_ip}:{dport}")
            elif packet.haslayer(ICMP):
                log_event("NETWORK", f"ICMP: {src_ip} -> {dst_ip}")
            else:
                log_event("NETWORK", f"Unknown packet from {src_ip} to {dst_ip}")
