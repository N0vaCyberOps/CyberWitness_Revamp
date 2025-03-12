from scapy.all import IP, TCP, UDP, ICMP, Ether
from utils.log_event import log_event
from typing import Dict, Any

def analyze_packet(packet) -> Dict[str, Any]:
    """
    Analizuje pakiet sieciowy i zwraca szczegóły w formacie słownikowym.
    
    Args:
        packet: Przechwycony pakiet sieciowy
        
    Returns:
        Słownik z kluczami:
        - type (str): Typ pakietu (TCP/UDP/ICMP/Non-IP/Unknown/Error)
        - src_ip (str): Adres IP źródłowy (jeśli dostępny)
        - dst_ip (str): Adres IP docelowy (jeśli dostępny)
        - src_port (int): Port źródłowy (dla TCP/UDP)
        - dst_port (int): Port docelowy (dla TCP/UDP)
        - error (str): Komunikat błędu (w przypadku wyjątku)
    """
    result = {
        "type": "Unknown",
        "src_ip": None,
        "dst_ip": None,
        "src_port": None,
        "dst_port": None
    }

    try:
        # Analiza warstwy Ethernet
        if packet.haslayer(Ether):
            result.update({
                "src_mac": packet[Ether].src,
                "dst_mac": packet[Ether].dst
            })

        # Analiza warstwy IP
        if packet.haslayer(IP):
            ip_layer = packet[IP]
            result.update({
                "src_ip": ip_layer.src,
                "dst_ip": ip_layer.dst,
                "protocol": ip_layer.proto
            })

            # Analiza protokołów warstwy transportowej
            if packet.haslayer(TCP):
                result.update({
                    "type": "TCP",
                    "src_port": packet[TCP].sport,
                    "dst_port": packet[TCP].dport,
                    "flags": str(packet[TCP].flags)
                })
            elif packet.haslayer(UDP):
                result.update({
                    "type": "UDP",
                    "src_port": packet[UDP].sport,
                    "dst_port": packet[UDP].dport
                })
            elif packet.haslayer(ICMP):
                result.update({
                    "type": "ICMP",
                    "icmp_type": packet[ICMP].type,
                    "icmp_code": packet[ICMP].code
                })
            else:
                result["type"] = "Other-IP"
        else:
            result["type"] = "Non-IP"

        return result

    except Exception as e:
        error_msg = f"Packet analysis failed: {str(e)}"
        log_event("ERROR", error_msg)
        return {
            "type": "Error",
            "error": error_msg,
            "raw_packet": str(packet)[:100]  # Zwróć fragment pakietu do debugowania
        }