import asyncio
import logging
from network.advanced_traffic_monitor import TrafficMonitor
from database.database_handler import DatabaseHandler
from alerts.alert_coordinator import AlertCoordinator
import sys

logger = logging.getLogger(__name__)

class CyberWitness:
    def __init__(self):
        self.db = DatabaseHandler()
        self.alert_coordinator = AlertCoordinator(self.db)
        self.monitor = TrafficMonitor(self.db, self.alert_coordinator)
        self.queue = asyncio.Queue(maxsize=1000)
        self.running = True

    async def initialize_components(self):
        await self.db.initialize()
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
            if not self.monitor.sniffer.running:
                logger.warning("Sniffer inactive, restarting...")
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

    async def graceful_shutdown(self):
        self.running = False
        await self.monitor.stop()
        await self.db.close()
        logger.info("Shutdown complete.")

    async def initialize_components(self):
        await self.db._init_db()
        await self.monitor.start()

async def async_main():
    cw = CyberWitness()
    await cw.initialize_components()
    cw.running = True

    tasks = [
        asyncio.create_task(cw.packet_processing()),
        asyncio.create_task(cw.monitor.start()),
    ]

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        pass
    finally:
        await cw.monitor.stop()
        await cw.db.close()

def main():
    logging.basicConfig(level=logging.INFO)
    if sys.platform == 'win32':
        try:
            asyncio.run(async_main())
        except KeyboardInterrupt:
            logger.info("Zamknięto aplikację za pomocą Ctrl+C")
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(async_main())

if __name__ == "__main__":
    main()
