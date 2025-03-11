from scapy.all import IP, TCP, UDP, ICMP

def analyze_packet(packet):
    """Analizuje pakiet i zwraca jego opis."""
    if packet.haslayer(IP):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        if packet.haslayer(TCP):
            sport, dport = packet[TCP].sport, packet[TCP].dport
            return f"TCP Packet: {src_ip}:{sport} -> {dst_ip}:{dport}"
        elif packet.haslayer(UDP):
            sport, dport = packet[UDP].sport, packet[UDP].dport
            return f"UDP Packet: {src_ip}:{sport} -> {dst_ip}:{dport}"
        elif packet.haslayer(ICMP):
            return f"ICMP Packet: {src_ip} -> {dst_ip}"
    return "Unknown packet type"  # ✅ Teraz zawsze zwraca string
