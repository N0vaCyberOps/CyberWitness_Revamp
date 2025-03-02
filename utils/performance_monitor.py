# File: performance_monitor.py
# Location: CyberWitness_N0va/utils/

import psutil
import asyncio
import logging

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Moduł monitorujący wydajność systemu"""
    def __init__(self, interval=5):
        self.interval = interval

    async def monitor(self):
        """Monitorowanie wydajności CPU i RAM"""
        while True:
            cpu_usage = psutil.cpu_percent()
            memory_usage = psutil.virtual_memory().percent
            logger.info(f"CPU: {cpu_usage}% | RAM: {memory_usage}%")
            await asyncio.sleep(self.interval)

    async def start(self):
        """Uruchomienie monitorowania"""
        logger.info("Performance monitoring started.")
        await self.monitor()
