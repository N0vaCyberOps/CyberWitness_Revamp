import pytest
from scapy.all import IP, UDP, DNS, DNSQR, TCP, Raw
from scapy.layers.tls.handshake import TLSClientHello

@pytest.mark.security
class TestSecurityScenarios:
    @pytest.fixture
    def extractor(self):
        from network.threat_detector import FeatureExtractor
        return FeatureExtractor()

    def test_sql_injection_in_dns(self, extractor):
        malicious_query = "example.com'; DROP TABLE users;--"
        packet = IP(dst="8.8.8.8")/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=malicious_query))
        
        features = extractor.extract(packet)
        
        assert features['dns_suspicious'] == 1
        assert features['dns_entropy'] > 4.5

    def test_buffer_overflow_in_tcp(self, extractor):
        malicious_payload = b"A" * 10000 + b"\x90" * 500
        packet = IP()/TCP(dport=80)/Raw(load=malicious_payload)
        
        features = extractor.extract(packet)
        assert features['payload_length'] == len(malicious_payload)

    def test_malicious_tls_handshake(self, extractor):
        from scapy.layers.tls import TLS
        from scapy.layers.tls.handshake import TLSClientHello
        
        malicious_hello = TLSClientHello(ciphers=[0x0000])
        packet = IP()/TCP()/TLS()/malicious_hello
        
        features = extractor.extract(packet)
        assert features.get('ja3_hash') is not None