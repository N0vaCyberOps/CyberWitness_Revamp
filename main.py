import asyncio
import signal
import logging
from network.advanced_traffic_monitor import AdvancedTrafficMonitor

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

class CyberWitness:
    def __init__(self, interface="Intel(R) Wi-Fi 6E AX211 160MHz"):
        self.monitor = AdvancedTrafficMonitor(interface=interface)
        self.running = True

    async def start(self):
        """Uruchamia nasłuchiwanie i obsługuje przerwania."""
        logger.info("CyberWitness uruchomiony.")
        try:
            await self.monitor.start_sniffing()
        except asyncio.CancelledError:
            pass
        finally:
            await self.shutdown()

    async def shutdown(self):
        """Zatrzymuje nasłuchiwanie i zapisuje raport."""
        if self.running:
            logger.info("Zatrzymywanie CyberWitness...")
            self.running = False
            await self.monitor.stop_sniffing()
            logger.info("CyberWitness zakończył działanie.")

def main():
    """Główna funkcja programu."""
    loop = asyncio.get_event_loop()
    cw = CyberWitness()

    # Obsługa sygnałów (Windows: KeyboardInterrupt)
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, lambda: asyncio.create_task(cw.shutdown()))
        except NotImplementedError:
            logger.warning("Obsługa sygnałów nie jest wspierana na tym systemie.")

    try:
        loop.run_until_complete(cw.start())
    except KeyboardInterrupt:
        logger.info("Przerwanie ręczne (Ctrl+C).")
    finally:
        loop.run_until_complete(cw.shutdown())
        loop.close()

if __name__ == "__main__":
    main()
