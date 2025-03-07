import asyncio
from scapy.all import IP, AsyncSniffer, get_if_list
from utils.logging import log_info, log_error  # Correct import
from network.packet_analyzer import analyze_packet


class AdvancedTrafficMonitor:
    """Zaawansowany system monitorowania ruchu sieciowego."""

    def __init__(self, alert_coordinator, config):
        self.config = config
        self.alert_coordinator = alert_coordinator
        # Corrected: Use getint and provide fallback directly to getint
        self.max_queue_size = config.getint('monitoring', 'max_queue_size', fallback=0)  # Use getint
        self.packet_queue = asyncio.Queue(maxsize=self.max_queue_size)
        self._running = False
        self.processed_packets = 0
        self.errors = 0
        self.sniffer = None

    async def initialize(self):
        """Inicjalizacja monitora, w tym uruchomienie sniffingu."""
        log_info("🔍 AdvancedTrafficMonitor initialized.")
        self._running = True

        raw_interfaces = self.config.get("monitoring", "interfaces", fallback="")
        interfaces = [iface.strip() for iface in raw_interfaces.split(",") if iface.strip()]
        available_interfaces = get_if_list()
        self.valid_interfaces = [iface for iface in interfaces if iface in available_interfaces]

        if not self.valid_interfaces:
            log_error(f"⚠️ Brak dostępnych interfejsów! Możliwe: {available_interfaces}")
            return

        log_info(f"✅ Sniffer uruchomiony na: {self.valid_interfaces}")
        self.sniffer = AsyncSniffer(iface=self.valid_interfaces, prn=self.handle_packet_wrapper, store=False)
        self.sniffer.start()



    async def handle_packet_wrapper(self, packet):
        """
        Wrapper do obsługi pakietów.
        """
        await self.handle_packet(packet)


    async def handle_packet(self, packet):
        """Obsługuje pojedynczy pakiet, analizuje go i wrzuca do kolejki."""
        try:
            if IP in packet:
                log_info(f"📡 Przechwycono pakiet od: {packet[IP].src}")
            await self.packet_queue.put(packet)
            self.processed_packets += 1

            threat_data = await analyze_packet(packet)
            if threat_data:
                await self.alert_coordinator.handle_alert(threat_data)

        except asyncio.QueueFull:
            log_error("⚠️ Kolejka pakietów pełna! Odrzucam pakiet.")
            self.errors += 1
        except Exception as e:
            log_error(f"⚠️ Błąd w handle_packet: {e}")
            self.errors += 1

    async def start_monitoring(self):
        """Rozpoczyna monitorowanie."""
        await self.initialize()


    async def stop_monitoring(self):
        """Zatrzymuje monitorowanie."""
        log_info("🛑 Zatrzymuję AdvancedTrafficMonitor...")
        self._running = False
        if self.sniffer:
             self.sniffer.stop()
        while not self.packet_queue.empty():
            try:
                self.packet_queue.get_nowait()
            except asyncio.QueueEmpty:
                break
        log_info("✅ AdvancedTrafficMonitor zatrzymany.")

    def get_stats(self):
        """Zwraca statystyki monitora."""
        return {
            "processed_packets": self.processed_packets,
            "errors": self.errors,
            "queue_size": self.packet_queue.qsize()
        }