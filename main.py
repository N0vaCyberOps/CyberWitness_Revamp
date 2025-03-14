import asyncio
import signal
import logging
import psutil
from network.advanced_traffic_monitor import TrafficMonitor
from database.database_handler import DatabaseHandler
from alerts.alert_coordinator import AlertCoordinator

logger = logging.getLogger(__name__)

class CyberWitness:
    def __init__(self):
        self.db = DatabaseHandler()
        self.alert_coordinator = AlertCoordinator(self.db)
        self.monitor = TrafficMonitor(self.db, self.alert_coordinator)
        self.queue = asyncio.Queue(maxsize=1000)
        self.running = False
        self.sniffer_alive = asyncio.Event()

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
                logger.error(f"Packet processing error: {e}")
                await self.restart_sniffer()

    async def watchdog(self):
        while self.running:
            await asyncio.sleep(30)
            if not self.sniffer_alive.is_set():
                logger.warning("Sniffer inactive - restarting...")
                await self.restart_sniffer()

    async def restart_sniffer(self):
        backoff = 2
        for attempt in range(5):
            try:
                await self.monitor.restart()
                self.sniffer_alive.set()
                logger.info(f"Sniffer restarted (attempt {attempt + 1})")
                return
            except Exception as e:
                logger.error(f"Restart failed: {e}")
                await asyncio.sleep(backoff)
                backoff *= 2
        logger.critical("Critical sniffer failure!")
        await self.alert_coordinator.trigger_alert(
            "Critical Sniffer Failure",
            "Sniffer failed to restart after multiple attempts.",
            "CRITICAL"
        )
        await self.graceful_shutdown()

    async def monitor_resources(self):
        while self.running:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_usage = psutil.virtual_memory().percent
            logger.info(f"CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%")
            if cpu_usage > 90 or memory_usage > 90:
                await self.alert_coordinator.trigger_alert(
                    "High Resource Usage",
                    f"CPU: {cpu_usage}%, Memory: {memory_usage}%",
                    "HIGH"
                )
            await asyncio.sleep(60)

    async def graceful_shutdown(self, sig=None):
        self.running = False
        self.sniffer_alive.clear()
        await self.monitor.stop()
        await self.db.close()
        logger.info(f"Shutdown complete ({sig.name if sig else 'manual'})")

async def async_main():
    cw = CyberWitness()
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(cw.graceful_shutdown(sig)))

    asyncio.create_task(cw.watchdog())
    asyncio.create_task(cw.monitor_resources())
    await cw.packet_processing()

def main():
    logging.basicConfig(level=logging.INFO)
    asyncio.run(async_main())

if __name__ == "__main__":
    main()