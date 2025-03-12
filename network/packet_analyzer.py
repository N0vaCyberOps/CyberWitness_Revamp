from scapy.all import IP, TCP, UDP, ICMP
from utils.log_event import log_event
from typing import Dict, Any

def analyze_packet(packet) -> Dict[str, Any]:
    result = {
        "type": "Unknown",
        "src_ip": None,
        "dst_ip": None,
        "src_port": None,
        "dst_port": None
    }

    try:
        if packet.haslayer(IP):
            ip_layer = packet[IP]
            result.update({
                "src_ip": ip_layer.src,
                "dst_ip": ip_layer.dst
            })

            if packet.haslayer(TCP):
                result.update({
                    "type": "TCP",
                    "src_port": packet[TCP].sport,
                    "dst_port": packet[TCP].dport
                })
            elif packet.haslayer(UDP):
                result.update({
                    "type": "UDP",
                    "src_port": packet[UDP].sport,
                    "dst_port": packet[UDP].dport
                })
            elif packet.haslayer(ICMP):
                result["type"] = "ICMP"
            else:
                result["type"] = "Other-IP"
        else:
            result["type"] = "Non-IP"

        return result
    except Exception as e:
        error_msg = f"Packet analysis error: {str(e)}"
        log_event("ERROR", error_msg)
        return {"type": "Error", "error": error_msg}