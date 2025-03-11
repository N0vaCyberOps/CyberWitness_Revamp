from scapy.all import sniff, IP, TCP, UDP
import logging

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class NetworkAnalyzer:
    """Moduł do przechwytywania i analizy pakietów sieciowych."""

    def __init__(self, log_file: str = None):
        """Inicjalizacja analizatora z opcjonalnym plikiem logowania."""
        self.log_file = log_file
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.INFO)
            logging.getLogger().addHandler(file_handler)

    def analyze_packet(self, packet):
        """Analizuje pojedynczy pakiet sieciowy."""
        try:
            if IP in packet:
                ip_src = packet[IP].src
                ip_dst = packet[IP].dst
                protocol = packet[IP].proto
                logging.info(f"IP Packet: {ip_src} -> {ip_dst}, Protocol: {protocol}")

                if TCP in packet:
                    tcp_sport = packet[TCP].sport
                    tcp_dport = packet[TCP].dport
                    logging.info(f"TCP Packet: {ip_src}:{tcp_sport} -> {ip_dst}:{tcp_dport}")
                elif UDP in packet:
                    udp_sport = packet[UDP].sport
                    udp_dport = packet[UDP].dport
                    logging.info(f"UDP Packet: {ip_src}:{udp_sport} -> {ip_dst}:{udp_dport}")
        except Exception as e:
            logging.error(f"Błąd podczas analizy pakietu: {e}")

    def capture_and_analyze(self, count: int = 10):
        """Przechwytuje pakiety i analizuje je."""
        try:
            sniff(prn=self.analyze_packet, count=count, store=False)
        except Exception as e:
            logging.error(f"Błąd podczas przechwytywania pakietów: {e}")

if __name__ == "__main__":
    analyzer = NetworkAnalyzer(log_file="network_analysis.log")
    analyzer.capture_and_analyze()
