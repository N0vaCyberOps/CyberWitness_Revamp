import asyncio
import signal
import logging
import scapy.all as scapy
from network.advanced_traffic_monitor import AdvancedTrafficMonitor
from database.database_handler import DatabaseHandler
from alerts.alert_coordinator import AlertCoordinator
from datetime import datetime

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

class CyberWitness:
    def __init__(self):
        self.interface = self.detect_network_interface()
        if not self.interface:
            logger.error("Brak dostępnego interfejsu do nasłuchiwania!")
            exit(1)

        self.db = DatabaseHandler()
        self.alert_coordinator = AlertCoordinator(self.db)
        self.monitor = AdvancedTrafficMonitor(self.db, self.alert_coordinator, self.interface)

    def detect_network_interface(self):
        """ Wykrywa interfejs sieciowy i wybiera najlepszy. """
        try:
            interfaces = scapy.get_if_list()  # Pobiera listę interfejsów
            logger.info(f"Dostępne interfejsy: {interfaces}")

            # Priorytetowe nazwy interfejsów
            preferowane = ["Wi-Fi", "Ethernet", "Intel", "wlan", "eth"]

            # Przeszukujemy dostępne interfejsy i wybieramy najlepszy
            for iface in interfaces:
                if any(p in iface for p in preferowane):
                    logger.info(f"Wybrany interfejs: {iface}")
                    return iface

            # Jeśli żaden nie pasuje, wybierz pierwszy dostępny
            logger.warning("Nie znaleziono pasującego interfejsu. Używanie pierwszego dostępnego.")
            return interfaces[0] if interfaces else None
        except Exception as e:
            logger.error(f"Błąd detekcji interfejsu: {e}")
            return None

    async def generate_report(self):
        """ Tworzy plik raportu z przechwyconymi danymi. """
        filename = f"cyberwitness_report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        with open(filename, "w", encoding="utf-8") as report:
            report.write("==== Raport CyberWitness ====\n")
            report.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            report.write(f"Interfejs: {self.interface}\n")
            report.write("\n--- Wykryte pakiety ---\n")

            # Pobranie logów z monitorowania
            logs = self.monitor.get_captured_packets()
            for log in logs:
                report.write(log + "\n")

        logger.info(f"Zapisano raport: {filename}")

    async def graceful_shutdown(self, sig):
        """ Obsługuje zamykanie aplikacji. """
        logger.info(f"Otrzymano sygnał {sig.name}, zatrzymywanie aplikacji...")
        await self.monitor.stop()
        await self.db.close()
        await self.generate_report()
        logger.info("Zakończono działanie CyberWitness.")

async def async_main():
    cw = CyberWitness()

    loop = asyncio.get_event_loop()

    # Obsługa zamknięcia programu (Windows/Linux)
    if hasattr(signal, "SIGTERM"):
        loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(cw.graceful_shutdown(signal.SIGTERM)))
    if hasattr(signal, "SIGINT"):
        loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(cw.graceful_shutdown(signal.SIGINT)))

    await cw.monitor.start()

def main():
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        logger.info("Zatrzymano ręcznie przez użytkownika.")

if __name__ == "__main__":
    main()
