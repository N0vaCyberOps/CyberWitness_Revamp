import sys
import os
import asyncio
import logging
from datetime import datetime

# 🔹 Ustawienie poprawnej ścieżki do `network`
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "network"))
from advanced_traffic_monitor import AdvancedTrafficMonitor  # ✅ Teraz import działa!

# 🔹 Konfiguracja katalogu logów
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# 🔹 Tworzenie unikalnej nazwy pliku logu
log_filename = os.path.join(log_dir, f"cyber_witness_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

# 🔹 Konfiguracja logowania (UTF-8 dla Windows!)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_filename, encoding="utf-8"),  # ✅ Poprawione kodowanie
        logging.StreamHandler(sys.stdout)  # ✅ Obsługuje Windows UTF-8
    ]
)

async def main():
    """Główna funkcja uruchamiająca monitor ruchu sieciowego."""
    interface = "WiFi"  # ✅ Windows-friendly interfejs!

    monitor = AdvancedTrafficMonitor(interface)
    
    try:
        sniff_task = asyncio.create_task(monitor.start_sniffing())
        await asyncio.sleep(30)  # 🔹 Sniffowanie przez 30 sekund
        await monitor.stop_sniffing()
        await sniff_task
    except Exception as e:
        logging.error(f"Błąd główny: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
