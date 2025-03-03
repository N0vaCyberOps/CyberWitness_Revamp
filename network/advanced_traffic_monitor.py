import asyncio
from scapy.all import AsyncSniffer, IP, TCP, UDP
from database.threat_intelligence import ThreatIntelligenceDatabase
from utils.analysis.behavioral_analyzer import BehavioralAnalyzer

class AdvancedTrafficMonitor:
    """Zaawansowany system monitorowania ruchu sieciowego z analizą AI"""
    def __init__(self, config):
        self.config = config
        self.sniffers = {}
        self.analyzer = BehavioralAnalyzer()
        self.threat_db = ThreatIntelligenceDatabase()
        self.packet_queue = asyncio.Queue(maxsize=10000)

    async def packet_processing_worker(self):
        """Przetwarzanie pakietów w kolejce"""
        while True:
            packet = await self.packet_queue.get()
            try:
                threat_score = await self.analyzer.evaluate_packet(packet)
                if threat_score > 0.7:
                    await self.threat_db.log_threat(packet)
            finally:
                self.packet_queue.task_done()

    async def start_interface(self, interface):
        """Uruchomienie monitorowania dla interfejsu sieciowego"""
        def packet_handler(pkt):
            if not self.packet_queue.full():
                self.packet_queue.put_nowait(pkt)

        sniffer = AsyncSniffer(
            iface=interface,
            prn=packet_handler,
            filter="ip or ip6",
            store=False
        )
        sniffer.start()
        self.sniffers[interface] = sniffer

    async def initialize(self):
        """Inicjalizacja systemu monitorowania"""
        workers = [asyncio.create_task(self.packet_processing_worker())
                   for _ in range(self.config.getint('monitoring', 'workers'))]
        
        interfaces = self.config['monitoring']['interfaces'].split(',')
        for iface in interfaces:
            await self.start_interface(iface.strip())

    async def stop(self):
        """Zatrzymanie wszystkich snifferów"""
        for sniffer in self.sniffers.values():
            sniffer.stop()
        self.sniffers.clear()
