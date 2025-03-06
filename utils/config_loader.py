import configparser
import os

CONFIG_PATH = 'config.ini'

def load_config(config_path=CONFIG_PATH):
    """Loads the configuration from the .ini file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    config = configparser.ConfigParser()
    try:
        config.read(config_path)
    except configparser.Error as e:
        raise Exception(f"Error parsing configuration file: {e}") from e
    return config