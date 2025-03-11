from scapy.all import sniff, IP, TCP, UDP, ICMP
from utils.log_event import log_event

class PacketAnalyzer:
    """Klasa do analizy pakietów sieciowych."""

    def analyze_packet(self, packet):
        """Analizuje pojedynczy pakiet sieciowy."""
        try:
            if IP in packet:
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst

                if TCP in packet:
                    src_port = packet[TCP].sport
                    dst_port = packet[TCP].dport
                    log_event("INFO", f"📦 TCP Packet: {src_ip}:{src_port} -> {dst_ip}:{dst_port}")
                    return f"TCP Packet: {src_ip}:{src_port} -> {dst_ip}:{dst_port}"
                
                elif UDP in packet:
                    src_port = packet[UDP].sport
                    dst_port = packet[UDP].dport
                    log_event("INFO", f"📦 UDP Packet: {src_ip}:{src_port} -> {dst_ip}:{dst_port}")
                    return f"UDP Packet: {src_ip}:{src_port} -> {dst_ip}:{dst_port}"
                
                elif ICMP in packet:
                    log_event("INFO", f"📦 ICMP Packet: {src_ip} -> {dst_ip}")
                    return f"ICMP Packet: {src_ip} -> {dst_ip}"
                
                else:
                    log_event("WARNING", f"Nieznany pakiet: {src_ip} -> {dst_ip}")
                    return f"IP Packet: {src_ip} -> {dst_ip}"

        except Exception as e:
            log_event("ERROR", f"Błąd analizy pakietu: {e}")
            return "Error analyzing packet"

    def capture_packets(self, count=10):
        """Przechwytuje i analizuje pakiety."""
        log_event("INFO", f"📡 Rozpoczynam przechwytywanie {count} pakietów...")
        sniff(prn=self.analyze_packet, count=count, store=False)
