
import sys
import asyncio
from utils import setup_logging, global_exception_handler, load_config
from network.advanced_traffic_monitor import AdvancedTrafficMonitor
from alerts.alert_coordinator import AlertCoordinator
from api.api_server import run_api_server

class CyberWitnessN0va:
    def __init__(self):
        self.config = load_config()
        self.monitor = AdvancedTrafficMonitor(self.config)
        self.alerts = AlertCoordinator(self.config)
        self.api_task = None

    async def startup(self):
        """Inicjalizacja komponentów systemu"""
        await self.monitor.initialize()
        await self.alerts.initialize()
        self.api_task = asyncio.create_task(run_api_server())  # ✅ Poprawione: usunięto self.config

    async def shutdown(self):
        """Bezpieczne wyłączanie systemu"""
        await self.monitor.stop()
        await self.alerts.shutdown()
        if self.api_task:
            self.api_task.cancel()
            await self.api_task

async def main():
    app = CyberWitnessN0va()
    await app.startup()
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        await app.shutdown()

if __name__ == "__main__":
    setup_logging()
    sys.excepthook = global_exception_handler
    asyncio.run(main())
