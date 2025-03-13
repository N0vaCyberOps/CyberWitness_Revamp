# Utwórz plik test_scapy_tls.py
from scapy.layers.tls.all import TLS, TLSClientHello
from scapy.all import sniff

print("TLS layer available:", hasattr(TLS, "version"))
print("TLSClientHello exists:", TLSClientHello is not None)