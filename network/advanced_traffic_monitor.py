import scapy.all as scapy
import logging
import asyncio
from network.packet_analyzer import PacketAnalyzer  # Dodano import

logger = logging.getLogger(__name__)

class TrafficMonitor:
    def __init__(self, db, alert_coordinator, interface='eth0', fallback_interface='wlan0'):
        self.db = db
        self.alert_coordinator = alert_coordinator
        self.interface = interface
        self.fallback_interface = fallback_interface
        self.sniffer = None
        self.packet_analyzer = PacketAnalyzer(db, alert_coordinator)  # Poprawiono inicjalizację
        self.interface_check_task = None

    async def check_interface(self):
        while True:
            await asyncio.sleep(10)
            proc = await asyncio.create_subprocess_exec(
                'ip', 'link', 'show', self.interface,
                stdout=asyncio.subprocess.PIPE
            )
            stdout, _ = await proc.communicate()
            if b"DOWN" in stdout:
                logger.warning(f"Interface {self.interface} down!")
                self.interface = self.fallback_interface
                await self.restart()

    async def start(self):
        try:
            self.sniffer = scapy.AsyncSniffer(
                iface=self.interface,
                prn=self.packet_callback,
                store=False
            )
            self.sniffer.start()
            logger.info(f"Sniffing started on {self.interface}")
            self.interface_check_task = asyncio.create_task(self.check_interface())
        except Exception as e:
            logger.error(f"Sniffer error on {self.interface}: {str(e)}")
            raise

    def packet_callback(self, packet):
        self.packet_analyzer.process_packet(packet)

    async def stop(self):
        if self.sniffer:
            self.sniffer.stop()
            if self.interface_check_task:
                self.interface_check_task.cancel()
            logger.info("Sniffer stopped")

    async def restart(self):
        await self.stop()
        await self.start()