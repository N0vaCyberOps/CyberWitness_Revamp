import scapy.all as scapy
import logging
import asyncio
from scapy.interfaces import get_if_list

logger = logging.getLogger("network.advanced_traffic_monitor")

class AdvancedTrafficMonitor:
    def __init__(self, db, alert_coordinator):
        self.db = db
        self.alert_coordinator = alert_coordinator
        self.interfaces = self.detect_interfaces()
        self.sniffers = []

    def detect_interfaces(self):
        """ Automatycznie wykrywa dostępne interfejsy sieciowe. """
        available_interfaces = get_if_list()
        filtered_interfaces = [iface for iface in available_interfaces if not iface.startswith("lo")]
        logger.info(f"Wykryte interfejsy sieciowe: {filtered_interfaces}")
        return filtered_interfaces

    async def start(self):
        """ Uruchamia nasłuch na wszystkich interfejsach. """
        if not self.interfaces:
            logger.error("Brak dostępnych interfejsów do monitorowania.")
            return

        for iface in self.interfaces:
            sniffer = asyncio.create_task(self.start_sniffer(iface))
            self.sniffers.append(sniffer)

        logger.info("Nasłuchiwanie rozpoczęte na wszystkich interfejsach.")
        await asyncio.gather(*self.sniffers)

    async def start_sniffer(self, iface):
        """ Uruchamia sniffer na danym interfejsie. """
        try:
            logger.info(f"Sniffer uruchomiony na interfejsie: {iface}")
            scapy.AsyncSniffer(iface=iface, prn=self.packet_callback, store=False).start()
            await asyncio.sleep(99999)  # Sniffer działa w nieskończoność
        except Exception as e:
            logger.error(f"Błąd sniffera na {iface}: {e}")

    def packet_callback(self, packet):
        """ Obsługuje przechwycone pakiety. """
        if scapy.IP in packet:
            src = packet[scapy.IP].src
            dst = packet[scapy.IP].dst
            logger.info(f"Przechwycono pakiet: {src} -> {dst}")
            # Tu można dodać analizę zagrożeń, np. SQLi, XSS, SYN flood

    async def stop(self):
        """ Zatrzymuje sniffery na wszystkich interfejsach. """
        for sniffer in self.sniffers:
            sniffer.cancel()
        logger.info("Sniffery zatrzymane.")
