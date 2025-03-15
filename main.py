import asyncio
import logging
import os
from datetime import datetime
from network.advanced_traffic_monitor import AdvancedTrafficMonitor
from database.database_handler import DatabaseHandler
from alerts.alert_coordinator import AlertCoordinator

# Tworzenie katalogu na logi, jeśli nie istnieje
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Nazwa pliku logów na podstawie daty i czasu uruchomienia aplikacji
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = os.path.join(LOG_DIR, f"cyber_witness_{timestamp}.txt")

# Konfiguracja logowania do pliku i konsoli
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_filename, mode="w"),  # Logi zapisywane do pliku
        logging.StreamHandler()  # Logi wyświetlane w konsoli
    ]
)

logger = logging.getLogger(__name__)

class CyberWitness:
    def __init__(self, interface="Ethernet", fallback_interface="Wi-Fi"):
        self.db = DatabaseHandler()
        self.alert_coordinator = AlertCoordinator(self.db)
        self.monitor = AdvancedTrafficMonitor(self.db, self.alert_coordinator, interface, fallback_interface)
        self.running = True

    async def run(self):
        try:
            logger.info("Cyber Witness is starting...")
            await self.monitor.start()
            while self.running:
                await asyncio.sleep(10)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            await self.shutdown()

    async def shutdown(self):
        logger.info("Shutting down Cyber Witness...")
        self.running = False
        await self.monitor.stop()
        await self.db.close()
        logger.info(f"Log file saved: {log_filename}")

async def async_main():
    cw = CyberWitness()
    await cw.run()

def main():
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
