from scapy.all import sniff, IP, TCP, UDP
import logging
from utils.ai_analyzer import AIAnalyzer
from utils.siem_logger import SIEMLogger
from utils.geolocation import GeoLocation
from utils.mitre_attack import MITREAttack
from prometheus_client import Counter, start_http_server

# Inicjalizacja modułów
ai_analyzer = AIAnalyzer()
ai_analyzer.train_model()
siem_logger = SIEMLogger()
geo_locator = GeoLocation()
mitre_attack = MITREAttack()

# Prometheus - licznik anomalii
anomalies_detected = Counter('anomalies_detected', 'Total number of detected network anomalies')

def analyze_packet(packet):
    """Analizuje pakiety sieciowe i wykrywa anomalie."""
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        summary = f"Packet: {ip_src} -> {ip_dst}"

        # Geolokalizacja atakującego
        geo_info = geo_locator.get_location(ip_src)

        # Mapowanie do MITRE ATT&CK
        attack_tactic = mitre_attack.map_threat("DDoS Attack")  # Testowe przypisanie

        if ai_analyzer.detect_anomaly(summary):
            logging.warning(f"🔴 Wykryto anomalię: {summary} | Lokalizacja: {geo_info} | MITRE: {attack_tactic}")
            anomalies_detected.inc()
            siem_logger.log_event("network_anomaly", f"Anomaly detected: {summary}", {
                "src_ip": ip_src, "dst_ip": ip_dst, "location": geo_info, "mitre_tactic": attack_tactic
            })
        else:
            logging.info(f"🟢 Normalny pakiet: {summary}")

if __name__ == "__main__":
    start_http_server(8000)  # Endpoint Prometheus
    sniff(prn=analyze_packet, count=100)
