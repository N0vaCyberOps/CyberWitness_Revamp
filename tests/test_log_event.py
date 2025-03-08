import unittest
import os
from utils.logging import log_event

class TestLogEvent(unittest.TestCase):

    def setUp(self):
        """Tworzy tymczasowy plik logów."""
        self.temp_log_path = "test_cyber_witness.log"

    def tearDown(self):
        """Usuwa plik logów po teście, jeśli istnieje."""
        if os.path.exists(self.temp_log_path):
            try:
                os.remove(self.temp_log_path)
            except PermissionError:
                pass  # Jeśli plik jest otwarty, zostanie zamknięty w kolejnym teście.

    def test_log_event_info(self):
        """Test zapisu logów INFO."""
        log_event("INFO", "Testowy log INFO", log_file=self.temp_log_path)

        with open(self.temp_log_path, "r") as f:
            content = f.read()

        self.assertIn("INFO", content)
        self.assertIn("Testowy log INFO", content)

if __name__ == "__main__":
    unittest.main()
