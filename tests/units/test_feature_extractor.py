# tests/unit/test_feature_extractor.py
import pytest
from scapy.all import *
from network.threat_detector import FeatureExtractor

@pytest.fixture
def malicious_dns_packet():
    """Pakiet z podejrzanym zapytaniem DNS (wysoka entropia)"""
    return Ether()/IP(src="192.168.1.66")/UDP()/DNS(
        qd=DNSQR(qname="d3b1gweb1bhwqj3jkg1brj.example.com")
    )

def test_dga_detection(malicious_dns_packet):
    extractor = FeatureExtractor()
    features = extractor.extract(malicious_dns_packet)
    
    # Sprawdź czy system wykrył:
    # - Wysoką entropię w nazwie domeny
    # - Brak odpowiedzi DNS
    # - Podejrzany ruch DNS
    assert features['dns_entropy'] > 4.5
    assert features['dns_suspicious'] == 1
    assert features['dns_query_no_answer'] == 1

def test_tls_fingerprinting():
    """Test generowania odcisku JA3 dla różnych wersji TLS"""
    tls12_pkt = TLS(version=0x0303, cipher=0x009C)
    tls13_pkt = TLS(version=0x0304, cipher=0x1301)
    
    extractor = FeatureExtractor()
    ja3_tls12 = extractor._generate_ja3(tls12_pkt)
    ja3_tls13 = extractor._generate_ja3(tls13_pkt)
    
    # Sprawdź czy różne wersje TLS generują różne hashe
    assert ja3_tls12 != ja3_tls13
    assert len(ja3_tls12) == 32  # MD5 hash length