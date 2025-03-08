import logging
import logging.handlers
import configparser
import os
from datetime import datetime
from threading import Lock

# Globalny mutex do synchronizacji logowania
log_lock = Lock()

# 📌 Wczytaj konfigurację logowania **tylko raz** (wydajność!)
config = configparser.ConfigParser()
config.read("config.ini")
LOG_FILE = config.get("logging", "log_file", fallback="cyber_witness.log")

# 📌 Ustawienia loggera – działa globalnie!
logger = logging.getLogger("CyberWitnessLogger")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(event_type)s - %(message)s",
                              datefmt="%Y-%m-%d %H:%M:%S")

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler = logging.handlers.RotatingFileHandler(
    LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def log_event(event_type: str, message: str, severity: str = "INFO"):
    """
    Loguje zdarzenie w systemie Cyber Witness.

    Args:
        event_type (str): Typ zdarzenia (np. "THREAT_DETECTED", "SYSTEM_ERROR").
        message (str): Opis zdarzenia.
        severity (str): Poziom logowania ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL").
    """
    severity = severity.upper()
    allowed_severities = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if severity not in allowed_severities:
        severity = "WARNING"

    with log_lock:
        try:
            if severity == "DEBUG":
                logger.debug(message, extra={"event_type": event_type})
            elif severity == "INFO":
                logger.info(message, extra={"event_type": event_type})
            elif severity == "WARNING":
                logger.warning(message, extra={"event_type": event_type})
            elif severity == "ERROR":
                logger.error(message, extra={"event_type": event_type})
            elif severity == "CRITICAL":
                logger.critical(message, extra={"event_type": event_type})
        except Exception as e:
            with open("logging_error.log", "a") as f:
                f.write(f"[{datetime.now()}] Błąd logowania: {e}\n")
