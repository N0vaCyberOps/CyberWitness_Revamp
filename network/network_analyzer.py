import asyncio
from scapy.all import sniff
from typing import List, Dict, Any, Optional
from utils.log_event import log_event
from .packet_analyzer import analyze_packet

class NetworkAnalyzer:
    def __init__(self, max_buffer_size: int = 1000):
        self._captured_packets: List[Dict[str, Any]] = []
        self._max_buffer = max_buffer_size
        self._capture_active = False

    async def capture_and_analyze(
        self,
        count: int = 100,
        interface: Optional[str] = None,
        filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        self._captured_packets = []
        self._capture_active = True
        
        try:
            await asyncio.to_thread(
                self._start_sync_capture,
                count,
                interface,
                filter
            )
            return self._captured_packets
        except Exception as e:
            log_event("ERROR", f"Capture failed: {e}")
            return []
        finally:
            self._capture_active = False

    def _start_sync_capture(self, count: int, interface: Optional[str], filter: Optional[str]):
        sniff(
            iface=interface,
            filter=filter,
            prn=self._process_packet,
            count=count,
            stop_filter=lambda _: not self._capture_active
        )

    def _process_packet(self, packet):
        try:
            analyzed = analyze_packet(packet)
            if len(self._captured_packets) >= self._max_buffer:
                self._captured_packets.pop(0)
            self._captured_packets.append(analyzed)
        except Exception as e:
            log_event("ERROR", f"Packet processing error: {e}")

    def stop_capture(self):
        self._capture_active = False