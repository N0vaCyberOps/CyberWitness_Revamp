import asyncio
from scapy.all import AsyncSniffer
from typing import Optional
from utils.log_event import log_event

class AdvancedTrafficMonitor:
    def __init__(self, config: dict, analyzer: callable):
        self.config = config
        self.analyzer = analyzer
        self.sniffer: Optional[AsyncSniffer] = None
        self._running = False
        self._monitor_task: Optional[asyncio.Task] = None

    async def start_monitoring(self):
        """Asynchroniczne uruchomienie monitorowania z obsługą błędów"""
        if self._running:
            return

        self._running = True
        try:
            self.sniffer = AsyncSniffer(
                iface=self.config.get("interface"),
                filter=self.config.get("filter"),
                prn=self.analyzer,
                store=False
            )
            self.sniffer.start()
            self._monitor_task = asyncio.create_task(self._monitor_status())
            log_event("INFO", "Monitoring started successfully")
        except Exception as e:
            self._running = False
            log_event("ERROR", f"Failed to start monitoring: {e}")
            raise

    async def _monitor_status(self):
        """Monitorowanie statusu sniffera w tle"""
        while self._running:
            await asyncio.sleep(1)
            if not self.sniffer.running:
                self._running = False
                log_event("WARNING", "Sniffer stopped unexpectedly")

    async def stop_monitoring(self):
        """Bezpieczne zatrzymanie monitorowania"""
        if self._running:
            self._running = False
            if self.sniffer:
                self.sniffer.stop()
            if self._monitor_task:
                await self._monitor_task
            log_event("INFO", "Monitoring stopped gracefully")