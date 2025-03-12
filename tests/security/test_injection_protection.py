# tests/security/test_injection_protection.py
import pytest
from scapy.all import DNSQR, DNS, IP, TCP
from network.threat_detector import FeatureExtractor

@pytest.mark.security
class TestSecurityScenarios:
    @pytest.fixture
    def extractor(self):
        return FeatureExtractor()

    def test_sql_injection_in_dns(self, extractor):
        malicious_dns = "example.com'; DROP TABLE users;--" 
        packet = DNS(qd=DNSQR(qname=malicious_dns))
        
        features = extractor.extract(packet)
        assert features['dns_suspicious'] == 1

    def test_buffer_overflow_simulation(self, extractor):
        oversized_payload = b'A' * 10_000  # Usunięto nieprawidłowy znak
        packet = IP()/TCP()/oversized_payload
        
        features = extractor.extract(packet)
        assert features['oversized_payload'] == 1