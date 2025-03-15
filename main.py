import asyncio
import logging
import signal
from network.advanced_traffic_monitor import TrafficMonitor
from database.database_handler import DatabaseHandler
from alerts.alert_coordinator import AlertCoordinator

logger = logging.getLogger(__name__)

class CyberWitness:
    def __init__(self, interface='Ethernet', fallback_interface='Wi-Fi'):
        self.db = DatabaseHandler()
        self.alert_coordinator = AlertCoordinator(self.db)
        self.monitor = TrafficMonitor(self.db, self.alert_coordinator, interface, fallback_interface)
        self.queue = asyncio.Queue(maxsize=1000)
        self.running = True

    async def initialize_components(self):
        await self.db._init_db()
        await self.monitor.start()

    async def packet_processing(self):
        while self.running:
            try:
                packet = await asyncio.wait_for(self.queue.get(), timeout=1.0)
                await asyncio.to_thread(self.monitor.analyze_packet, packet)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Packet processing error: {e}")
                await self.restart_sniffer()

    async def watchdog(self):
        while self.running:
            await asyncio.sleep(30)
            if not self.monitor.is_running():
                logger.warning("Sniffer inactive - restarting...")
                await self.monitor.restart()

    async def restart_sniffer(self):
        backoff = 2
        for attempt in range(5):
            try:
                await self.monitor.restart()
                logger.info(f"Sniffer restarted (attempt {attempt + 1})")
                return
            except Exception as e:
                logger.error(f"Restart failed: {e}")
                await asyncio.sleep(backoff)
                backoff *= 2
        logger.critical("Critical sniffer failure!")
        await self.graceful_shutdown()

    async def graceful_shutdown(self, sig=None):
        self.running = False
        await self.monitor.stop()
        await self.db.close()
        logger.info(f"Shutdown complete ({sig.name if sig else 'manual'}).")

async def async_main():
    cw = CyberWitness(interface='Ethernet', fallback_interface='Wi-Fi')
    await cw.initialize_components()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda sig=sig: asyncio.create_task(cw.graceful_shutdown(sig)))

    await asyncio.gather(cw.watchdog(), cw.packet_processing())

def main():
    logging.basicConfig(level=logging.INFO)
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
