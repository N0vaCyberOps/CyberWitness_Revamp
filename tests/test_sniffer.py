# tests/test_sniffer.py
import asyncio
from scapy.all import AsyncSniffer, get_if_list, IP, TCP  # Poprawione importy
# Poprawione importy absolutne:
from utils.logging import log_info, log_error
from network.advanced_traffic_monitor import AdvancedTrafficMonitor
from network.packet_analyzer import analyze_packet
from alerts.alert_coordinator import AlertCoordinator
from database.database_handler import DatabaseHandler, init_db
import configparser
import unittest  # Importuj unittest
import os # Importuj os


class TestSniffer(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        """Konfiguracja przed każdym testem."""
        # Załaduj TESTOWY plik konfiguracyjny
        config_path = os.path.join(os.path.dirname(__file__), "test_config.ini")
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        # Zainicjuj bazę danych (używając testowego pliku bazy danych)
        init_db(self.config['database']['database_file'])  # Zainicjuj testową bazę danych

        self.db_handler = DatabaseHandler(self.config['database'])
        self.alert_coordinator = AlertCoordinator(self.db_handler)
        self.advanced_monitor = AdvancedTrafficMonitor(interface="lo", alert_coordinator=self.alert_coordinator, config=self.config) # Użyj self.config
        self.sniffer = AsyncSniffer(
            iface="lo",  # Użyj interfejsu loopback do testowania
            prn=lambda pkt: analyze_packet(pkt, self.alert_coordinator, self.config), # Użyj self.config
            store=False
        )


    async def test_sniffer_initialization(self):
        """Testuj, czy sniffer inicjalizuje się poprawnie."""
        self.assertIsNotNone(self.sniffer, "Sniffer powinien być zainicjalizowany")
        self.assertEqual(self.sniffer.iface, "lo", "Sniffer powinien nasłuchiwać na interfejsie loopback")


    async def test_sniffer_stop(self):
        """Testuj zatrzymywanie sniffera."""
        self.sniffer.start()
        await asyncio.sleep(0.5)  # Daj mu trochę czasu na uruchomienie
        self.sniffer.stop()
        self.assertFalse(self.sniffer.running, "Sniffer powinien być zatrzymany")

    async def asyncTearDown(self):
        """Posprzątaj po każdym teście."""
        if self.sniffer.running:
            self.sniffer.stop()
        self.db_handler.close() #Dodano
        # Usuń testowy plik bazy danych. BARDZO WAŻNE!
        if os.path.exists(self.config['database']['database_file']):
            os.remove(self.config['database']['database_file'])
        # Usuń plik dziennika testów.
        if os.path.exists(self.config['logging']['filename']):
           os.remove(self.config['logging']['filename'])




if __name__ == '__main__':
    unittest.main()