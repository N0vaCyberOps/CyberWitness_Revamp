import logging

# Konfiguracja globalnego loggera
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Mapa poziomów logowania
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

def log_event(level, message):
    """
    Loguje zdarzenie w systemie.

    Args:
        level (str): Poziom logowania (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        message (str): Treść loga.
    """
    log_level = LOG_LEVELS.get(level.upper(), logging.INFO)
    logging.log(log_level, message)
