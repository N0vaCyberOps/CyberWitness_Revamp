import scapy.all as scapy
import asyncio
import logging
import datetime
import aiofiles
from threading import Lock

class AdvancedTrafficMonitor:
    def __init__(self, interface):
        self.interface = interface
        self.logger = logging.getLogger("CyberWitness")
        self.captured_packets = []  # Bufor na przechwycone pakiety
        self.lock = Lock()  # Synchronizacja dostępu do listy pakietów
        self.is_sniffing = False  # Flaga kontrolna do zatrzymywania sniffingu

    def packet_callback(self, packet):
        """Obsługuje przechwycone pakiety."""
        if not self.is_sniffing:
            return

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {packet.summary()}\n"

        with self.lock:
            self.captured_packets.append(log_entry)
        self.logger.info(f"Przechwycono pakiet: {log_entry.strip()}")

    async def save_report(self):
        """Zapisuje przechwycone pakiety do pliku logu."""
        if not self.captured_packets:
            self.logger.warning("Brak przechwyconych pakietów do zapisania.")
            return

        filename = f"logs/cyberwitness_report_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

        try:
            async with aiofiles.open(filename, "w") as f:
                async with self.lock:
                    await f.writelines(self.captured_packets)
                    self.captured_packets.clear()
            self.logger.info(f"Zapisano raport: {filename}")
        except Exception as e:
            self.logger.error(f"Błąd zapisu pliku: {str(e)}")

    async def start_sniffing(self):
        """Uruchamia sniffing na wybranym interfejsie."""
        self.is_sniffing = True
        self.logger.info(f"Rozpoczynanie sniffowania na {self.interface}")

        try:
            await asyncio.to_thread(
                scapy.sniff,
                iface=self.interface,
                prn=self.packet_callback,
                store=False
            )
        except Exception as e:
            self.logger.error(f"Błąd sniffingu: {str(e)}")
            self.is_sniffing = False

    async def stop_sniffing(self):
        """Zatrzymuje sniffing i zapisuje raport."""
        self.is_sniffing = False
        self.logger.info("Zatrzymywanie sniffingu...")
        await self.save_report()
        self.logger.info("Sniffowanie zatrzymane.")
