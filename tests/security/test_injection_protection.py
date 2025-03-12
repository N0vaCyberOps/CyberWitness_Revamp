import pytest
from scapy.all import IP, UDP, DNS, DNSQR, TCP, Raw
from network.threat_detector import FeatureExtractor

@pytest.mark.security
class TestSecurityScenarios:
    @pytest.fixture
    def extractor(self):
        return FeatureExtractor()

    def test_sql_injection_in_dns(self, extractor):
        malicious_query = "example.com'; DROP TABLE users;--"
        packet = IP(dst="8.8.8.8")/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=malicious_query))
        
        features = extractor.extract(packet)
        
        assert features['dns_suspicious'] == 1
        assert features['dns_entropy'] > 4.5
        assert "DROP TABLE" in features.get('dns_query', '')

    def test_buffer_overflow_in_tcp(self, extractor):
        malicious_payload = b"A" * 10000 + b"\x90" * 500
        packet = IP()/TCP(dport=80)/Raw(load=malicious_payload)
        
        features = extractor.extract(packet)
        
        assert features['payload_length'] == 10500
        assert features['protocol'] == "TCP"

    def test_malicious_tls_handshake(self, extractor):
        from scapy.layers.tls import TLSClientHello
        malicious_hello = TLSClientHello(ciphers=[0x0000], comp=[0], ext=[])
        packet = IP()/TCP()/TLS()/malicious_hello
        
        features = extractor.extract(packet)
        
        assert features.get('ja3_hash') is not None
        assert features['tls_anomaly'] == 0  # Placeholder for real detection