import json
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ConfigManager:
    """Moduł do zarządzania konfiguracją aplikacji."""

    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        """Ładuje plik konfiguracji JSON."""
        try:
            with open(self.config_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            logging.warning(f"Config file not found: {self.config_path}")
            return {}
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON in config file: {self.config_path}")
            return {}

    def get_config(self, key: str, default=None):
        """Zwraca wartość klucza konfiguracyjnego lub zmiennej środowiskowej."""
        value = os.getenv(key.upper(), self.config.get(key, default))
        if isinstance(value, str) and value.lower() in ("true", "false"):
            return value.lower() == "true"
        if isinstance(value, str) and value.isdigit():
            return int(value)
        return value
