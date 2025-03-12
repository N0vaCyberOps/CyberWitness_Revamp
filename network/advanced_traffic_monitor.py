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
        if self._running:
            return
            
        self._running = True
        self.sniffer = AsyncSniffer(
            iface=self.config.get("interface"),
            filter=self.config.get("filter"),
            prn=self.analyzer,
            store=False
        )
        self.sniffer.start()
        
        # Dodano zarządzanie taskiem
        self._monitor_task = asyncio.create_task(self._monitor_status())

    async def _monitor_status(self):
        while self._running:
            await asyncio.sleep(1)
            if not self.sniffer.running:
                self._running = False

    async def stop_monitoring(self):
        self._running = False
        if self.sniffer:
            self.sniffer.stop()
        if self._monitor_task:
            await self._monitor_task