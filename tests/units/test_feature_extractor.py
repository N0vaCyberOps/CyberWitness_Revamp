import pytest
import numpy as np
from scapy.all import Ether, IP, TCP, UDP, DNS, DNSQR
from scapy.layers.tls.all import TLS, TLSVersion
from network.threat_detector import FeatureExtractor

@pytest.fixture
def dga_packet():
    return Ether()/IP(src="192.168.1.66")/UDP()/DNS(
        qd=DNSQR(qname="xb91fh30dajk38hfd0j4.example.com")
    )

@pytest.fixture
def tls_packet():
    return Ether()/IP()/TCP()/TLS(
        version=TLSVersion.TLS_1_2,
        cipher=[0x009C, 0x009D]
    )

def test_dga_detection(dga_packet):
    extractor = FeatureExtractor()
    features = extractor.extract(dga_packet)
    
    assert features['dns_entropy'] > 4.5
    assert features['dns_suspicious'] == 1
    assert features['category'] == 'suspicious'

def test_tls_fingerprinting(tls_packet):
    extractor = FeatureExtractor()
    features = extractor.extract(tls_packet)
    
    assert features['ja3_hash'] is not None
    assert len(features['ja3_hash']) == 32
    assert features['tls_version'] == TLSVersion.TLS_1_2