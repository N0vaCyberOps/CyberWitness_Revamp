import asyncio
from scapy.all import sniff
from utils.log_event import log_event

class AdvancedTrafficMonitor:
    def __init__(self, config, analyzer):
        self.config = config
        self.analyzer = analyzer
        self._running = False
        self._lock = asyncio.Lock()  # ✅ Added lock for thread safety

    async def start_monitoring(self, interface=None, filter=None):
        """Starts network monitoring asynchronously."""
        async with self._lock:
            if self._running:
                log_event("WARNING", "Monitoring is already running")
                return

            self._running = True
            log_event("INFO", "Network monitoring started")

            try:
                await asyncio.to_thread(
                    sniff,
                    iface=interface or self.config.get("interface"),
                    filter=filter or self.config.get("filter"),
                    prn=self.analyzer.analyze_packet,
                    store=False,
                    stop_filter=lambda _: not self._running
                )
            except Exception as e:
                log_event("ERROR", f"Monitoring error: {e}")
            finally:
                async with self._lock:
                    self._running = False
                    log_event("INFO", "Network monitoring stopped")

    async def stop_monitoring(self):
        """Stops network monitoring."""
        async with self._lock:
            if not self._running:
                return
            self._running = False
            log_event("INFO", "Stopping network monitoring")
