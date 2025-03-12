import pytest
from scapy.all import Ether, IP, TCP, DNS, TLS
from network.threat_detector import FeatureExtractor

@pytest.fixture
def extractor():
    return FeatureExtractor()

def test_tcp_port_scan_detection(extractor):
    # Symulacja skanowania portów
    packet = Ether()/IP(src="192.168.1.100")/TCP(dport=range(1,100))
    features = extractor.extract(packet)
    assert features['port_scan'] == 1

def test_dns_entropy_calculation(extractor):
    # Test DGA (wysoka entropia)
    packet = Ether()/IP()/DNS(qd=DNSQR(qname="xjkahd83jhdas.example.com"))
    features = {}
    extractor._analyze_dns(packet, features)
    assert features['dns_suspicious'] == 1

def test_ja3_hashing(extractor):
    # Test generowania hashy TLS
    tls_packet = Ether()/IP()/TCP()/TLS(version=0x0303)
    ja3 = extractor._generate_ja3(tls_packet[TLS])
    assert len(ja3) == 32  # Długość MD5