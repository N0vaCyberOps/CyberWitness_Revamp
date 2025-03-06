import asyncio
from scapy.all import AsyncSniffer, get_if_list
# Corrected absolute imports:
from utils.logging import log_info, log_error
from network.advanced_traffic_monitor import AdvancedTrafficMonitor
from network.packet_analyzer import analyze_packet
from alerts.alert_coordinator import AlertCoordinator
from database.database_handler import DatabaseHandler, init_db
import configparser
import unittest # Import unittest


class TestSniffer(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        """Setup method to initialize resources before each test."""
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.db_handler = DatabaseHandler(self.config['database'])
        self.alert_coordinator = AlertCoordinator(self.db_handler)
        self.monitor = AdvancedTrafficMonitor(self.alert_coordinator, self.config['network'])
        await self.monitor.initialize()



    async def test_sniffer_initialization(self):
        """Test if the sniffer initializes correctly."""
        self.assertTrue(self.monitor._running, "Monitor should be running after initialization.")
        self.assertIsNotNone(self.monitor.sniffer, "Sniffer should be initialized.")
        self.assertNotEqual(len(self.monitor.valid_interfaces),0, "Sniffer should have valid interface")

    async def test_sniffer_stop(self):
        """Test stopping the sniffer."""
        await self.monitor.stop_monitoring()
        self.assertFalse(self.monitor._running, "Monitor should not be running after stopping.")
        self.assertIsNone(self.monitor.sniffer.running, "Sniffer should be stopped.")


    async def asyncTearDown(self):
        await self.monitor.stop_monitoring()


if __name__ == "__main__":
    unittest.main()