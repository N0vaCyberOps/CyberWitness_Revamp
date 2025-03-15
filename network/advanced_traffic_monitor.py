import scapy.all as scapy
import logging
import asyncio
from network.packet_analyzer import PacketAnalyzer

logger = logging.getLogger(__name__)

class TrafficMonitor:
    def __init__(self, db, alert_coordinator, interface='Wi-Fi', fallback_interface='Ethernet'):
        self.db = db
        self.alert_coordinator = alert_coordinator
        self.interface = interface
        self.fallback_interface = fallback_interface
        self.sniffer = None
        self.packet_analyzer = PacketAnalyzer(db, alert_coordinator)
        self.interface_check_task = None

    async def check_interface(self):
        while True:
            await asyncio.sleep(10)
            proc = await asyncio.create_subprocess_exec(
                'ipconfig', '/all',
                stdout=asyncio.subprocess.PIPE
            )
            stdout, _ = await proc.communicate()
            output = stdout.decode(errors='ignore')
            if self.interface not in output:
                logging.warning(f"Interface {self.interface} down, switching to fallback {self.fallback_interface}")
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
            logging.info(f"Sniffer started on {self.interface}")
            self.interface_check_task = asyncio.create_task(self.check_interface())
        except Exception as e:
            logging.error(f"Błąd uruchomienia sniffera na {self.interface}: {str(e)}")
            raise

    def packet_callback(self, packet):
        self.packet_analyzer.process_packet(packet)

    async def stop(self):
        if self.sniffer:
            self.sniffer.stop()
            if self.interface_check_task:
                self.interface_check_task.cancel()
            logging.info("Sniffer stopped")

    async def restart(self):
        await self.stop()
        await self.start()
