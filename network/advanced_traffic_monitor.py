import scapy.all as scapy
import asyncio
import logging
import datetime
import aiofiles

class AdvancedTrafficMonitor:
    def __init__(self, interface, log_file="cyberwitness_report.txt"):
        self.interface = interface
        self.log_file = log_file
        self.logger = logging.getLogger(__name__)
        self.captured_packets = []  # Bufor na przechwycone pakiety

    def packet_callback(self, packet):
        """Funkcja wywoływana dla każdego przechwyconego pakietu."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {packet.summary()}\n"
        
        self.logger.info(f"Przechwycono pakiet: {log_entry.strip()}")
        self.captured_packets.append(log_entry)

    async def save_report(self):
        """Zapisuje przechwycone pakiety do pliku logu."""
        if not self.captured_packets:
            self.logger.warning("Brak przechwyconych pakietów do zapisania.")
            return

        filename = f"cyberwitness_report_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        
        async with aiofiles.open(filename, "w") as f:
            await f.writelines(self.captured_packets)

        self.logger.info(f"Zapisano raport: {filename}")

    async def start_sniffing(self):
        """Rozpoczyna nasłuchiwanie na wybranym interfejsie."""
        self.logger.info(f"Sniffing started on {self.interface}")
        try:
            scapy.sniff(iface=self.interface, prn=self.packet_callback, store=False)
        except Exception as e:
            self.logger.error(f"Błąd sniffingu: {e}")

    async def stop_sniffing(self):
        """Kończy nasłuchiwanie i zapisuje raport."""
        self.logger.info("Stopping sniffing...")
        await self.save_report()
        self.logger.info("Sniffing stopped.")
