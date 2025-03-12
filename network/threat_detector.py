from scapy.config import conf
from scapy.all import TCP, UDP, DNS, IP
from scapy.contrib.tls import TLS, TLSClientHello  # Nowy prawidłowy import
import numpy as np
from collections import defaultdict, deque
import hashlib

# Wymuś ładowanie warstwy TLS
conf.load_layers.append("tls")
class FeatureExtractor:
    def __init__(self):
        self.window_size = 100
        self.packet_sequence = deque(maxlen=self.window_size)
        self.port_scan_threshold = 10
        self.port_counter = defaultdict(int)

    def extract(self, packet):
        features = {
            'protocol': self._get_protocol(packet),
            'payload_length': len(packet.payload) if packet.payload else 0,
            'port_scan': 0,
            'dns_suspicious': 0,
            'tls_anomaly': 0
        }
        
        self._analyze_port_scan(packet, features)
        
        if DNS in packet:
            self._analyze_dns(packet, features)
            
        if TLS in packet:
            tls_features = self._analyze_tls(packet)
            features.update(tls_features)
            
        return features

    def _get_protocol(self, packet):
        if TCP in packet:
            return "TCP"
        elif UDP in packet:
            return "UDP"
        return "Other"

    def _analyze_port_scan(self, packet, features):
        if IP in packet and (TCP in packet or UDP in packet):
            src_ip = packet[IP].src
            dst_port = packet[TCP].dport if TCP in packet else packet[UDP].dport
            
            key = (src_ip, dst_port)
            self.port_counter[key] += 1
            
            if self.port_counter[key] > self.port_scan_threshold:
                features['port_scan'] = 1

    def _analyze_dns(self, packet, features):
        try:
            dns_layer = packet[DNS]
            if dns_layer.qd:
                query = dns_layer.qd.qname.decode('utf-8', errors='ignore')
                entropy = self._calculate_entropy(query)
                features.update({
                    'dns_query': query,
                    'dns_entropy': entropy,
                    'dns_suspicious': 1 if entropy > 4.5 else 0
                })
        except Exception as e:
            print(f"DNS analysis error: {e}")

    def _analyze_tls(self, packet):
        try:
            tls_layer = packet[TLS]
            ja3_hash = self._generate_ja3(tls_layer)
            
            return {
                'tls_version': tls_layer.version,
                'cipher_suite': tls_layer.ciphersuite[0] if tls_layer.ciphersuite else None,
                'ja3_hash': ja3_hash,
                'tls_anomaly': 0  # Placeholder for anomaly detection
            }
        except Exception as e:
            print(f"TLS analysis error: {e}")
            return {}

    def _calculate_entropy(self, data):
        if not data:
            return 0.0
        counts = defaultdict(int)
        for char in data:
            counts[char] += 1
        probs = [count / len(data) for count in counts.values()]
        return -sum(p * np.log2(p) for p in probs)

    def _generate_ja3(self, tls_packet):
        try:
            if TLSClientHello in tls_packet:
                client_hello = tls_packet[TLSClientHello]
                parts = [
                    str(client_hello.version),
                    ','.join(map(str, client_hello.ciphers)),
                    ','.join(map(str, client_hello.comp)),
                    ','.join(map(str, client_hello.extensions))
                ]
                ja3_str = '-'.join(parts)
                return hashlib.md5(ja3_str.encode()).hexdigest()
            return None
        except Exception as e:
            print(f"JA3 generation error: {e}")
            return None