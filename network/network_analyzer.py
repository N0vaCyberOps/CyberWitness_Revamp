from scapy.all import IP, TCP, UDP, ICMP, Ether
from typing import Dict, Any
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

@lru_cache(maxsize=1024)
def _parse_ip_header(packet) -> Dict[str, Any]:
    """Optymalizacja: Cache'owanie nagłówków IP"""
    return {
        "src_ip": packet[IP].src,
        "dst_ip": packet[IP].dst,
        "protocol": packet[IP].proto
    }

def analyze_packet(packet) -> Dict[str, Any]:
    result = {
        "type": "Unknown",
        "src_ip": None,
        "dst_ip": None,
        "src_port": None,
        "dst_port": None
    }

    try:
        # Szybsze wykrywanie warstw przez dispatch zamiast wielokrotnych if-ów
        layer_checks = (
            (Ether, lambda: result.update({"src_mac": packet[Ether].src, "dst_mac": packet[Ether].dst})),
            (IP, lambda: result.update(_parse_ip_header(packet))),
            (TCP, lambda: result.update({
                "type": "TCP",
                "src_port": packet[TCP].sport,
                "dst_port": packet[TCP].dport
            })),
            (UDP, lambda: result.update({
                "type": "UDP",
                "src_port": packet[UDP].sport,
                "dst_port": packet[UDP].dport
            })),
            (ICMP, lambda: result.update({"type": "ICMP"}))
        )

        for layer, updater in layer_checks:
            if packet.haslayer(layer):
                updater()

        if not packet.haslayer(IP):
            result["type"] = "Non-IP"

        return result

    except Exception as e:
        logger.error("Packet analysis failed", exc_info=True)
        return {"type": "Error", "error": str(e)}