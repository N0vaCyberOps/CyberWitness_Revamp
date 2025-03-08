import unittest
import os
from utils.logging import log_debug, log_info, log_warning, log_error, log_critical

class TestLogging(unittest.TestCase):

    def setUp(self):
        """Tworzy tymczasowy plik logów."""
        self.temp_log_path = "test_logging.log"

    def tearDown(self):
        """Usuwa plik logów po teście."""
        if os.path.exists(self.temp_log_path):
            os.remove(self.temp_log_path)

    def test_log_levels(self):
        """Sprawdza poprawność zapisu logów dla wszystkich poziomów."""
        log_functions = {
            "DEBUG": log_debug,
            "INFO": log_info,
            "WARNING": log_warning,
            "ERROR": log_error,
            "CRITICAL": log_critical,
        }
        messages = {
            "DEBUG": "Debug message",
            "INFO": "Info message",
            "WARNING": "Warning message",
            "ERROR": "Error message",
            "CRITICAL": "Critical message",
        }

        for level, log_func in log_functions.items():
            with self.subTest(level=level):
                log_func(messages[level], log_file=self.temp_log_path)

                with open(self.temp_log_path, "r") as f:
                    content = f.read()

                self.assertIn(level, content)
                self.assertIn(messages[level], content)

if __name__ == "__main__":
    unittest.main()
