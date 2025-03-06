import json
import time
import scapy.all as scapy
from utils.logging import log_error, log_info  # Correct import
import asyncio
# Removed init_db import and call - it's now done in main.py
from database.database_handler import DatabaseHandler  # Import DatabaseHandler


async def analyze_packet(packet, threshold=0.7):
    """Analizuje pakiet i wykrywa zagrożenia."""

    threat_score = 0.0
    protocol = "Unknown"
    details = {}

    if scapy.TCP in packet:
        protocol = "TCP"
        if packet[scapy.TCP].dport in [22, 3389]:
            threat_score += 0.5
            details['ports'] = f"Potencjalnie niebezpieczne porty: {packet[scapy.TCP].dport}"
        if packet[scapy.TCP].flags & 0x12:  # SYN-ACK
            threat_score += 0.4
            details['flags'] = "Nietypowe flagi SYN-ACK"
        if packet[scapy.TCP].flags & 0x02 and not packet[scapy.TCP].flags & 0x10:  # SYN bez ACK
            threat_score += 0.6
            details['flags'] = "Możliwy atak SYN flood"
        if packet[scapy.TCP].flags & 0x29 > 0:  # XMAS scan (URG, PSH, FIN)
            threat_score += 0.7
            details['flags'] = "Wykryto skanowanie XMAS"
        if packet[scapy.TCP].flags == 0:  # NULL scan
            threat_score += 0.7
            details['flags'] = "Wykryto skanowanie NULL"

    elif scapy.UDP in packet:
        protocol = "UDP"
        if packet[scapy.UDP].dport == 53:
            threat_score += 0.2
            details['dns'] = 'Ruch DNS'


    elif scapy.ICMP in packet:
        protocol = "ICMP"
        threat_score += 0.2
        details['icmp'] = 'Ruch ICMP'

    if scapy.Raw in packet:
        payload = packet[scapy.Raw].load
        if b"malware" in payload.lower():
            threat_score += 0.8
            details['payload'] = 'Podejrzana zawartość'

    if threat_score > threshold:
        threat_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "source_ip": packet.get("IP", {}).get("src", "Unknown"),
            "destination_ip": packet.get("IP", {}).get("dst", "Unknown"),
            "protocol": protocol,
            "threat_level": float(threat_score),
            "details": json.dumps(details)
        }
        return threat_data  # Return the threat data *without* saving to DB here

    return None