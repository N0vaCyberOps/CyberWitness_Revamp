import configparser
import os

CONFIG_PATH = 'config.ini'

def load_config(config_path=CONFIG_PATH):
    """Ładuje konfigurację z pliku .ini."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Plik konfiguracyjny nie został znaleziony: {config_path}")

    config = configparser.ConfigParser()
    try:
        config.read(config_path)
    except configparser.Error as e:
        raise Exception(f"Błąd podczas parsowania pliku konfiguracyjnego: {e}") from e
    return config