import logging
import configparser
from utils.config_loader import load_config

def setup_logging(config):
    """Configures the logging system based on the config file."""
    try:
        log_level_str = config.get('level', 'INFO').upper()
        log_level = getattr(logging, log_level_str, logging.INFO)
        log_filename = config.get('filename', 'cyber_witness.log')

        logging.basicConfig(
            filename=log_filename,
            level=log_level,
            format="%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s",
        )
        log_info(f"Logging initialized. Level: {log_level_str}, File: {log_filename}")

    except (configparser.NoSectionError, configparser.NoOptionError, AttributeError) as e:
        print(f"Error loading logging configuration: {e}. Using default logging settings.")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s",
        )
        log_info("Logging initialized with default settings.")

# Define log functions for consistent use
def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

def log_warning(message):
    logging.warning(message)

def log_debug(message):
    logging.debug(message)

def log_critical(message):
    logging.critical(message)