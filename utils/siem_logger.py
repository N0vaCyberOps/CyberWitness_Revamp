import requests
import json
from utils.log_event import log_event
import os

SIEM_URL = os.getenv("SIEM_URL", "http://localhost:9200/threat_logs/_doc/")

def send_to_siem(event_type, src_ip, dst_ip, protocol):
    """
    Wysyła zdarzenie o zagrożeniu do systemu SIEM.

    Args:
        event_type (str): Typ zdarzenia.
        src_ip (str): Adres IP źródłowy.
        dst_ip (str): Adres IP docelowy.
        protocol (str): Protokół ruchu sieciowego.
    """
    event_data = {
        "event_type": event_type,
        "source_ip": src_ip,
        "destination_ip": dst_ip,
        "protocol": protocol
    }

    try:
        response = requests.post(SIEM_URL, json=event_data, headers={"Content-Type": "application/json"})
        if response.status_code == 201:
            log_event("SIEM_LOGGED", f"Zdarzenie {event_type} wysłane do SIEM.")
        else:
            log_event("SIEM_ERROR", f"Błąd wysyłania do SIEM: {response.text}", severity="ERROR")
    except Exception as e:
        log_event("SIEM_EXCEPTION", f"Wyjątek przy wysyłaniu do SIEM: {str(e)}", severity="ERROR")
