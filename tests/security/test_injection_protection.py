# tests/security/test_sql_injection.py
def test_sql_injection_through_dns():
    malicious_query = "'; DROP TABLE alerts;--" 
    packet = Ether()/IP()/UDP()/DNS(
        qd=DNSQR(qname=malicious_query)
    )
    
    extractor = FeatureExtractor()
    features = extractor.extract(packet)
    
    # System powinien:
    # - Traktować jako normalne zapytanie DNS
    # - Nie wywoływać żadnych wyjątków
    # - Oznaczyć jako podejrzane ze względu na specjalne znaki
    assert features['dns_suspicious'] == 1
    assert features['category'] == 'suspicious'