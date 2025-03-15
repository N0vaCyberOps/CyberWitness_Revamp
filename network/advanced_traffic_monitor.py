import scapy.all as scapy
import logging
import asyncio
import datetime
import aiofiles  # Dodana biblioteka do asynchronicznego zapisu plików

logger = logging.getLogger(__name__)

class AdvancedTrafficMonitor:
    def __init__(self, db, alert_coordinator, interface):
        self.db = db
        self.alert_coordinator = alert_coordinator
        self.interface = interface
        self.sniffer = None
        self.running = False
        self.log_file = None
        self.log_filename = ""

    async def start(self):
        """Uruchomienie sniffera na wybranym interfejsie."""
        try:
            logger.info(f"Sniffing started on {self.interface}")

            # Utwórz nazwę pliku i otwórz go asynchronicznie
            now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.log_filename = f"packet_log_{now}.txt"
            self.log_file = await aiofiles.open(self.log_filename, mode="a")

            # Uruchom sniffera
            self.running = True
            self.sniffer = scapy.AsyncSniffer(
                iface=self.interface,
                prn=self.packet_callback,  # Zmieniono na metodę klasy
                store=False
            )
            self.sniffer.start()

            # Czekaj na zatrzymanie
            while self.running:
                await asyncio.sleep(0.1)

        except Exception as e:
            logger.error(f"Błąd sniffera: {str(e)}")
        finally:
            if self.log_file:
                await self.log_file.close()

    async def packet_callback(self, packet):
        """Asynchroniczna obsługa pakietów."""
        try:
            log_entry = packet.summary()
            logger.info(log_entry)

            # Zapisz do pliku (asynchronicznie)
            await self.log_file.write(log_entry + "\n")

            # Tutaj możesz dodać logikę bazy danych i alertów
            # await self.db.insert_packet(log_entry)
            # await self.alert_coordinator.check_for_alerts(packet)

        except Exception as e:
            logger.error(f"Błąd przetwarzania pakietu: {str(e)}")

    async def stop(self):
        """Zatrzymanie sniffera."""
        if self.sniffer:
            self.running = False
            self.sniffer.stop()
            logger.info("Sniffer zatrzymany.")
            if self.log_file:
                await self.log_file.close()