import asyncio
import signal
import logging
from network.advanced_traffic_monitor import TrafficMonitor
from database.database_handler import DatabaseHandler
from alerts.alert_coordinator import AlertCoordinator

logger = logging.getLogger(__name__)

class CyberWitness:
    def __init__(self):
        self.db = DatabaseHandler()
        self.alert_coordinator = None
        self.monitor = None
        self.queue = asyncio.Queue(maxsize=1000)
        self.running = False
        self.sniffer_alive = asyncio.Event()

    async def initialize_components(self):
        await self.db.initialize()
        self.alert_coordinator = AlertCoordinator(self.db)
        self.monitor = TrafficMonitor(self.db, self.alert_coordinator)

    async def packet_processing(self):
        self.running = True
        self.sniffer_alive.set()
        while self.running:
            try:
                packet = await asyncio.wait_for(self.queue.get(), timeout=1.0)
                await asyncio.to_thread(self.monitor.analyze_packet, packet)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Błąd przetwarzania pakietu: {e}", exc_info=True)
                await self.restart_sniffer()

    async def watchdog(self):
        while self.running:
            await asyncio.sleep(30)
            if not self.sniffer_alive.is_set():
                logger.warning("Sniffer nieaktywny, restart...")
                await self.restart_sniffer()

    async def restart_sniffer(self):
        backoff = 2
        for attempt in range(5):
            try:
                await self.monitor.restart()
                self.sniffer_alive.set()
                logger.info(f"Sniffer zrestartowany (próba {attempt + 1})")
                return
            except Exception as e:
                logger.error(f"Restart nieudany: {e}")
                await asyncio.sleep(backoff)
                backoff *= 2
        logger.critical("Krytyczna awaria sniffera")
        await self.graceful_shutdown()

    async def graceful_shutdown(self, sig=None):
        self.running = False
        self.sniffer_alive.clear()
        await self.monitor.stop()
        await self.db.close()
        logger.info(f"System zamknięty ({sig.name if sig else 'ręcznie'})")

async def async_main():
    cw = CyberWitness()
    await cw.initialize_components()
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(cw.graceful_shutdown(sig)))

    await asyncio.gather(
        cw.watchdog(),
        cw.packet_processing()
    )

def main():
    logging.basicConfig(level=logging.INFO)
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
