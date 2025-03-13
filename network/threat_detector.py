# Lokalizacja: CyberWitness_Revamp/network/threat_detector.py
import numpy as np
from scapy.all import Ether, IP, TCP, UDP, DNS
from scapy.config import conf
from scapy.layers.tls.all import TLS, TLSClientHello, TLSVersion
from collections import defaultdict, deque
import hashlib

# Wymuś ładowanie modułu TLS
conf.contribs['tls'] = {'load_module': True}

class FeatureExtractor:
    def __init__(self):
        self.port_history = defaultdict(lambda: deque(maxlen=100))
        self.dns_cache = defaultdict(lambda: {'count': 0, 'entropy': 0.0})

    def extract(self, packet):
        features = {'category': 'normal'}
        self._analyze_transport(packet, features)
        self._analyze_dns(packet, features)
        self._analyze_tls(packet, features)
        return features

    def _analyze_transport(self, packet, features):
        if packet.haslayer(TCP):
            ports = packet[TCP].dport
            if isinstance(ports, (int, np.integer)):
                self._check_port_scan(ports, features)

    def _check_port_scan(self, port, features):
        self.port_history['tcp'].append(port)
        if len(set(self.port_history['tcp'])) > 50:
            features.update({
                'port_scan': 1,
                'category': 'suspicious'
            })

    def _analyze_dns(self, packet, features):
        if packet.haslayer(DNS):
            dns = packet[DNS]
            if dns.qr == 0:  # Query
                qname = dns.qd.qname.decode('utf-8', errors='ignore')
                entropy = self._calculate_entropy(qname)
                
                features.update({
                    'dns_entropy': entropy,
                    'dns_suspicious': 1 if entropy > 4.5 else 0,
                    'dns_query_no_answer': 1 if len(dns.an) == 0 else 0
                })

    def _calculate_entropy(self, string):
        prob = [float(string.count(c)) / len(string) for c in set(string)]
        return -sum(p * np.log(p) for p in prob) if prob else 0.0

    def _analyze_tls(self, packet, features):
        if packet.haslayer(TLS):
            try:
                ja3_hash = self._generate_ja3(packet[TLS])
                features.update({
                    'ja3_hash': ja3_hash,
                    'tls_version': packet[TLS].version
                })
            except AttributeError:
                pass

    def _generate_ja3(self, tls_pkt):
        try:
            ja3_str = f"{tls_pkt.version},{','.join(map(str, tls_pkt.cipher))}"
            return hashlib.md5(ja3_str.encode()).hexdigest()
        except AttributeError:
            return None