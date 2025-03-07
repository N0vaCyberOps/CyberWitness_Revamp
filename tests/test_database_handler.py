# tests/test_database_handler.py
import unittest
import configparser
import os
import json
import asyncio
from database.database_handler import DatabaseHandler, init_db  # Import absolutny


class TestDatabaseHandler(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        """Konfiguracja przed każdym testem."""
        # Załaduj TESTOWĄ konfigurację
        config_path = os.path.join(os.path.dirname(__file__), "test_config.ini")
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        # Zainicjuj bazę danych (używając testowego pliku bazy danych)
        await init_db(self.config['database']['database_file']) # Dodaj await

        self.db_handler = DatabaseHandler(self.config['database'])
        self.test_alert_data = {
            'timestamp': '2024-04-27 12:00:00',
            'alert_type': 'Test Alert',
            'alert_data': {'source_ip': '192.168.1.2', 'ports': [22, 80, 443]}
        }
        self.test_threat_data = {
            'timestamp': '2024-04-27 13:00:00',
            'source_ip': '192.168.1.3',
            'destination_ip': '10.0.0.1',
            'protocol': 'TCP',
            'threat_level': 0.8,
            'details': 'Possible port scan'
        }

    async def test_save_and_retrieve_alert(self):
        """Testuj zapisywanie i pobieranie alertu."""
        await self.db_handler.save_alert(self.test_alert_data)
        retrieved_alerts = await self.db_handler.get_recent_alerts(limit=1)
        self.assertEqual(len(retrieved_alerts), 1)
        retrieved_alert = retrieved_alerts[0]

        # Porównaj słownik bezpośrednio, a nie string JSON
        self.assertEqual(retrieved_alert['alert_data'], self.test_alert_data['alert_data'])
        self.assertEqual(retrieved_alert['timestamp'], self.test_alert_data['timestamp'])
        self.assertEqual(retrieved_alert['alert_type'], self.test_alert_data['alert_type'])
    async def test_save_and_retrieve_threat(self):
        """Testuj zapisywanie i pobieranie zagrożenia."""
        await self.db_handler.save_threat(self.test_threat_data)
        retrieved_threats = await self.db_handler.get_recent_threats(limit=1)
        self.assertEqual(len(retrieved_threats), 1)
        retrieved_threat = retrieved_threats[0]
        # Konwertuj pobrane zagrożenie na słownik do porównania, obsługując JSON w 'details', jeśli to konieczne
        self.assertEqual(retrieved_threat['timestamp'], self.test_threat_data['timestamp'])
        self.assertEqual(retrieved_threat['source_ip'], self.test_threat_data['source_ip'])
        self.assertEqual(retrieved_threat['destination_ip'], self.test_threat_data['destination_ip'])
        self.assertEqual(retrieved_threat['protocol'], self.test_threat_data['protocol'])
        self.assertEqual(retrieved_threat['threat_level'], self.test_threat_data['threat_level'])
        self.assertEqual(retrieved_threat['details'], self.test_threat_data['details'])

    async def test_get_recent_threats_empty(self):
        """Testuj pobieranie ostatnich zagrożeń, gdy baza danych jest pusta."""
        threats = await self.db_handler.get_recent_threats()
        self.assertEqual(threats, [])

    async def test_get_recent_threats_limit(self):
        """Testuj pobieranie ograniczonej liczby ostatnich zagrożeń."""
        # Zapisz wiele zagrożeń
        for i in range(5):
            threat_data = self.test_threat_data.copy()
            threat_data['timestamp'] = f'2024-04-27 13:00:{i}'
            await self.db_handler.save_threat(threat_data)

        # Pobierz ograniczoną liczbę zagrożeń
        limited_threats = await self.db_handler.get_recent_threats(limit=3)
        self.assertEqual(len(limited_threats), 3)


    async def test_get_recent_alerts_limit(self):
        """Testuj pobieranie ograniczonej liczby ostatnich alertów."""
        # Zapisz wiele alertów
        for i in range(5):
            alert_data = self.test_alert_data.copy()
            alert_data['timestamp'] = f'2024-04-27 12:00:{i}'
            await self.db_handler.save_alert(alert_data)

        # Pobierz ograniczoną liczbę alertów
        limited_alerts = await self.db_handler.