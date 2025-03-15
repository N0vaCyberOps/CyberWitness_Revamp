import scapy.all as scapy
import logging
import asyncio
import datetime

logger = logging.getLogger(__name__)

class AdvancedTrafficMonitor:
    def __init__(self, db, alert_coordinator, interface):
        self.db = db
        self.alert_coordinator = alert_coordinator
        self.interface = interface
        self.sniffer = None
        self.running = False

    async def start(self):
        """Uruchomienie sniffera na wybranym interfejsie."""
        try:
            logger.info(f"Sniffing started on {self.interface}")

            # Otwarcie pliku do zapisu
            now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_filename = f"packet_log_{now}.txt"

            def packet_callback(packet):
                """Obsługa przechwyconych pakietów."""
                log_entry = packet.summary()
                logger.info(log_entry)
                
                # Zapis do pliku
                with open(log_filename, "a") as f:
                    f.write(log_entry + "\n")

            # Uruchom sniffera w tle
            self.running = True
            self.sniffer = scapy.AsyncSniffer(iface=self.interface, prn=packet_callback, store=False)
            self.sniffer.start()
            while self.running:
                await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Błąd sniffera: {str(e)}")

    async def stop(self):
        """Zatrzymanie sniffera."""
        if self.sniffer:
            self.running = False
            self.sniffer.stop()
            logger.info("Sniffer zatrzymany.")

    async def restart(self):
        """Restartowanie sniffera."""
        await self.stop()
        await self.start()
