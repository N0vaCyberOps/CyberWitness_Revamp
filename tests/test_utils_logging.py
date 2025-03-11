# test_utils_logging.py
import logging
import pytest
from utils.log_event import log_event

def test_log_levels(caplog):
    """Testuje poprawność logowania dla wszystkich poziomów z weryfikacją outputu."""
    with caplog.at_level(logging.DEBUG):
        log_event("DEBUG", "Debug message")
        log_event("INFO", "Info message")
        log_event("WARNING", "Warning message")
        log_event("ERROR", "Error message")
        log_event("CRITICAL", "Critical message")

    records = caplog.records
    assert len(records) == 5
    assert records[0].message == "Debug message"
    assert records[0].levelname == "DEBUG"
    assert records[3].levelname == "ERROR"
    assert "Critical message" in caplog.text