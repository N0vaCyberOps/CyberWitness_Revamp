import logging
import os
import asyncio
from datetime import datetime
from advanced_traffic_monitor import AdvancedTrafficMonitor

# Tworzenie katalogu na logi
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Tworzenie pliku logów dla każdej sesji
log_filename = os.path.join(log_dir, f"cyberwitness_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

# Konfiguracja loggera
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

async def main():
    """Główna funkcja uruchamiająca nasłuchiwanie na interfejsie sieciowym"""
    interface = "eth0"  # Zmień na swój interfejs sieciowy, np. "wlan0" lub "Wi-Fi"
    monitor = AdvancedTrafficMonitor(interface)

    # Uruchomienie sniffingu w tle
    sniffing_task = asyncio.create_task(monitor.start_sniffing())

    # Sniffowanie trwa przez 30 sekund, potem zatrzymanie
    await asyncio.sleep(30)
    await monitor.stop_sniffing()

    # Zatrzymanie procesu sniffingu
    sniffing_task.cancel()
    try:
        await sniffing_task
    except asyncio.CancelledError:
        logging.info("Proces sniffingu został zatrzymany.")

if __name__ == "__main__":
    asyncio.run(main())
