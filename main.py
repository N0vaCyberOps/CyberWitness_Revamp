import asyncio
import signal
import logging
import datetime
from network.advanced_traffic_monitor import AdvancedTrafficMonitor
from database.database_handler import DatabaseHandler
from alerts.alert_coordinator import AlertCoordinator
import scapy.all as scapy

# Ustawienia logowania
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Automatyczna nazwa pliku z logami
now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"packet_log_{now}.txt"

class CyberWitness:
    def __init__(self):
        # Sprawdź dostępne interfejsy
        self.interface = self.detect_network_interface()
        logger.info(f"Używany interfejs: {self.interface}")

        # Inicjalizacja komponentów
        self.db = DatabaseHandler()
        self.alert_coordinator = AlertCoordinator(self.db)
        self.monitor = AdvancedTrafficMonitor(self.db, self.alert_coordinator, self.interface)

    def detect_network_interface(self):
        """Automatycznie wykrywa poprawną nazwę interfejsu."""
        interfaces = {iface.name for iface in scapy.get_if_list()}
        logger.info(f"Dostępne interfejsy: {interfaces}")

        possible_interfaces = [
            "Intel(R) Wi-Fi 6E AX211 160MHz",
            "VMware Virtual Ethernet Adapter for VMnet8",
            "Wi-Fi",
            "Ethernet"
        ]

        for iface in possible_interfaces:
            if iface in interfaces:
                return iface

        logger.warning("Nie znaleziono pasującego interfejsu! Używanie domyślnego.")
        return list(interfaces)[0] if interfaces else "lo"

    async def start(self):
        """Uruchamia nasłuchiwanie ruchu sieciowego."""
        await self.monitor.start()

    async def graceful_shutdown(self, sig=None):
        """Zamknięcie programu."""
        logger.info(f"Zamykanie aplikacji ({sig.name if sig else 'manual'})...")
        await self.monitor.stop()
        await self.db.close()
        logger.info("Zamknięto poprawnie.")

async def async_main():
    """Główna funkcja asynchroniczna."""
    cw = CyberWitness()

    # Obsługa sygnałów zamknięcia
    loop = asyncio.get_event_loop()
    if hasattr(signal, "SIGINT"):
        loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(cw.graceful_shutdown(signal.SIGINT)))

    await cw.start()

def main():
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
