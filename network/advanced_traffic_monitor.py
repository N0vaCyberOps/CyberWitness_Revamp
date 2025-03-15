import scapy.all as scapy
import logging
from network.packet_analyzer import PacketAnalyzer
import asyncio

logger = logging.getLogger(__name__)

class TrafficMonitor:
    def __init__(self, db, alert_coordinator, interface='Ethernet', fallback_interface='Wi-Fi'):
        self.db = db
        self.alert_coordinator = alert_coordinator
        self.interface = interface
        self.fallback_interface = fallback_interface
        self.sniffer = None
        self.packet_analyzer = PacketAnalyzer(db, alert_coordinator)

    async def start(self):
        self.sniffer = scapy.AsyncSniffer(
            iface=self.interface,
            prn=self.packet_callback,
            store=False
        )
        self.sniffer.start()
        logger.info(f"Sniffer uruchomiony na {self.interface}")

    def packet_callback(self, packet):
        asyncio.create_task(self.packet_analyzer.process_packet(packet))

    async def stop(self):
        if self.sniffer:
            self.sniffer.stop()
            logger.info("Sniffer zatrzymany")

    async def restart(self):
        await self.stop()
        await self.start()
