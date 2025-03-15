import logging
import os
from datetime import datetime

# Tworzenie katalogu na raporty, jeśli nie istnieje
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Tworzenie unikalnej nazwy pliku dla każdej sesji
log_filename = os.path.join(log_dir, f"cyber_witness_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

# Konfiguracja loggera
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_filename),  # Zapisywanie logów do pliku
        logging.StreamHandler()  # Wyświetlanie logów w konsoli
    ]
)

def log_packet(packet_info):
    """Zapisuje przechwycony pakiet do logów."""
    logging.info(f"Przechwycono pakiet: {packet_info}")

# Przykładowe użycie w kodzie sniffowania:
# log_packet("Ether / IP / UDP 192.168.1.1:12345 > 192.168.1.2:80 / Raw")
