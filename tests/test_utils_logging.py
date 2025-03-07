# tests/test_utils_logging.py
import unittest
import logging
# Correct absolute import:
from utils.logging import setup_logging, log_info, log_error, log_warning, log_debug, log_critical
import configparser
import os
import tempfile


class TestLogging(unittest.TestCase):

    def setUp(self):
        # Create a temporary file for logging
        self.temp_log_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
        self.temp_log_path = self.temp_log_file.name
        self.temp_log_file.close()  # Close immediately, setup_logging will open it.

        # Create a config for the logging module.
        self.config = configparser.ConfigParser()
        self.config['logging'] = {
            'level': 'DEBUG',  # Use DEBUG for comprehensive testing
            'filename': self.temp_log_path
        }
        setup_logging(self.config['logging'])
        self.log = logging.getLogger() # Get the root logger

    def test_setup_logging(self):
        """Test that logging is set up correctly with the provided config."""
        self.assertEqual(self.log.level, logging.DEBUG) # Check level

        # Check that we have a FileHandler
        file_handler_found = False
        for handler in self.log.handlers:
            if isinstance(handler, logging.FileHandler):
                file_handler_found = True
                self.assertEqual(handler.baseFilename, os.path.abspath(self.temp_log_path)) # Check filename
                break
        self.assertTrue(file_handler_found, "FileHandler not found in logger handlers")


    def test_log_info(self):
        log_info("This is an info message.")
        with open(self.temp_log_path, 'r') as f:
            content = f.read()
            self.assertIn("INFO", content)
            self.assertIn("This is an info message.", content)

    def test_log_error(self):
        log_error("This is an error message.")
        with open(self.temp_log_path, 'r') as f:
            content = f.read()
            self.assertIn("ERROR", content)
            self.assertIn("This is an error message.", content)

    def test_log_warning(self):
        log_warning("This is a warning message.")
        with open(self.temp_log_path, 'r') as f:
            content = f.read()
            self.assertIn("WARNING", content)
            self.assertIn("This is a warning message.", content)

    def test_log_debug(self):
        log_debug("This is a debug message.")
        with open(self.temp_log_path, 'r') as f:
            content = f.read()
            self.assertIn("DEBUG", content)
            self.assertIn("This is a debug message.", content)

    def test_log_critical(self):
        log_critical("This is a critical message.")
        with open(self.temp_log_path, 'r') as f:
            content = f.read()
            self.assertIn("CRITICAL", content)
            self.assertIn("This is a critical message.", content)

    def tearDown(self):
        # Clean up: remove the temporary log file.
        # First, close any handlers that might be writing to it.
        for handler in self.log.handlers:
            handler.close()  # Crucial to close before removing
        if os.path.exists(self.temp_log_path):
            os.remove(self.temp_log_path)


if __name__ == '__main__':
    unittest.main()