import configparser
from .logging import setup_logging
from .exception_handler import global_exception_handler

def load_config(config_path="config.ini"):
    """Ładuje plik konfiguracyjny."""
    config = configparser.ConfigParser()
    config.read(config_path)
    return config
