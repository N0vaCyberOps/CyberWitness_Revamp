import unittest
import configparser
import os
from alerts.alert_coordinator import AlertCoordinator
from network.advanced_traffic_monitor import AdvancedTrafficMonitor
from database.database_handler import DatabaseHandler

class TestSniffer(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        """Konfiguracja przed każdym testem."""
        self.config = configparser.ConfigParser()
        self.config.read("test_config.ini")

        self.db_handler = DatabaseHandler(self.config["database"])
        self.alert_coordinator = AlertCoordinator(self.db_handler)
        self.advanced_monitor = AdvancedTrafficMonitor(alert_coordinator=self.alert_coordinator, config=self.config["network"])

if __name__ == "__main__":
    unittest.main()
