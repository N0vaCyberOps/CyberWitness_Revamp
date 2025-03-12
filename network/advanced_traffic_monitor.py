import asyncio
from scapy.all import AsyncSniffer
from typing import Optional
import time

class AdvancedTrafficMonitor:
    def __init__(self, config: dict, analyzer: callable):
        self.config = config
        self.analyzer = analyzer
        self.sniffer: Optional[AsyncSniffer] = None
        self._running = False
        self._last_capture = 0

    async def start_monitoring(self):
        if self._running:
            return
        
        self._running = True
        self.sniffer = AsyncSniffer(
            iface=self.config.get("interface"),
            filter=self._compile_filters(),
            prn=self.analyzer,
            store=False
        )
        self.sniffer.start()

    def _compile_filters(self):
        """Kompilacja filtrów BPF do postaci binarnej"""
        filters = self.config.get("filter", "")
        return filters if " " not in filters else f"({filters})"

    async def get_stats(self):
        """Statystyki w czasie rzeczywistym bez blokowania głównego wątku"""
        return {
            "start_time": self._last_capture,
            "packet_count": len(self.sniffer.results) if self.sniffer else 0
        }