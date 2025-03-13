import sys
import hashlib
import numpy as np
from collections import defaultdict, deque
from scapy.config import conf
from scapy.all import TCP, UDP, DNS, IP, Packet, Raw
from scapy.error import Scapy_Exception

# Ładowanie warstwy TLS
try:
    conf.load_layers.append("tls")
    from scapy.layers.tls.record import TLS
    from scapy.layers.tls.handshake import TLSClientHello
except ImportError as e:
    sys.exit(f"Błąd ładowania TLS: {e}\nWykonaj: pip install git+https://github.com/secdev/scapy.git")

class FeatureExtractor:
    def __init__(self):
        self.window_size = 100
        self.packet_sequence = deque(maxlen=self.window_size)
        self.port_scan_threshold = 10
        self.port_counter = defaultdict(int)
        self.entropy_threshold = 4.5

    def extract(self, packet: Packet) -> dict:
        """Główna metoda ekstrakcji cech z pakietu"""
        features = {
            'protocol': self._get_protocol(packet),
            'src_ip': packet[IP].src if IP in packet else None,
            'dst_ip': packet[IP].dst if IP in packet else None,
            'payload_length': self._get_payload_length(packet),
            'port_scan': 0,
            'dns_suspicious': 0,
            'tls_anomaly': 0,
            'ja3_hash': None
        }

        try:
            self._analyze_port_scan(packet, features)
            
            if DNS in packet:
                self._analyze_dns(packet, features)
                
            if TLS in packet:
                self._analyze_tls(packet, features)

        except Scapy_Exception as e:
            print(f"Błąd analizy pakietu: {e}")

        return features

    def _get_protocol(self, packet: Packet) -> str:
        """Identyfikacja protokołu warstwy transportowej"""
        if TCP in packet:
            return "TCP"
        elif UDP in packet:
            return "UDP"
        return "OTHER"

    def _get_payload_length(self, packet: Packet) -> int:
        """Pobierz długość ładunku aplikacji"""
        if Raw in packet:
            return len(packet[Raw])
        return 0

    def _analyze_port_scan(self, packet: Packet, features: dict):
        """Wykrywanie skanowania portów"""
        if IP in packet and (TCP in packet or UDP in packet):
            src_ip = packet[IP].src
            dst_port = packet[TCP].dport if TCP in packet else packet[UDP].dport
            key = (src_ip, dst_port)
            
            self.port_counter[key] += 1
            if self.port_counter[key] > self.port_scan_threshold:
                features['port_scan'] = 1

    def _analyze_dns(self, packet: Packet, features: dict):
        """Analiza podejrzanych zapytań DNS"""
        dns_layer = packet[DNS]
        if dns_layer.qd:
            try:
                query = dns_layer.qd.qname.decode('utf-8', errors='ignore')
                entropy = self._calculate_entropy(query)
                features.update({
                    'dns_query': query,
                    'dns_entropy': entropy,
                    'dns_suspicious': 1 if entropy > self.entropy_threshold else 0
                })
            except UnicodeDecodeError:
                features['dns_suspicious'] = 1

    def _analyze_tls(self, packet: Packet, features: dict):
        """Analiza parametrów TLS"""
        try:
            tls_layer = packet[TLS]
            if TLSClientHello in tls_layer:
                client_hello = tls_layer[TLSClientHello]
                ja3_hash = self._generate_ja3(client_hello)
                features.update({
                    'tls_version': tls_layer.version,
                    'cipher_suite': client_hello.ciphers[0] if client_hello.ciphers else None,
                    'ja3_hash': ja3_hash
                })
        except (IndexError, AttributeError) as e:
            features['tls_anomaly'] = 1
            print(f"Błąd analizy TLS: {e}")

    def _calculate_entropy(self, data: str) -> float:
        """Oblicz entropię Shannona dla ciągu znaków"""
        if not data:
            return 0.0
            
        counts = defaultdict(int)
        for char in data:
            counts[char] += 1
            
        probs = [count / len(data) for count in counts.values()]
        return -sum(p * np.log2(p) for p in probs if p > 0)

    def _generate_ja3(self, client_hello: TLSClientHello) -> str:
        """Generuj hash JA3 z klienta TLS Hello"""
        try:
            parts = [
                str(client_hello.version),
                ','.join(map(str, client_hello.ciphers)),
                ','.join(map(str, client_hello.comp)),
                ','.join(map(str, [e.type for e in client_hello.ext]))
            ]
            ja3_str = '-'.join(parts)
            return hashlib.md5(ja3_str.encode()).hexdigest()
        except Exception as e:
            print(f"Błąd generowania JA3: {e}")
            return "unknown"

if __name__ == "__main__":
    # Testowa implementacja
    from scapy.layers.inet import Ether
    extractor = FeatureExtractor()
    test_packet = Ether()/IP()/TCP()/TLS()/TLSClientHello()
    print(extractor.extract(test_packet))