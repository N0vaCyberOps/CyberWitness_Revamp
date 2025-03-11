import logging
from utils.log_event import log_event

def test_log_event_info(caplog):
    """Test logowania na poziomie INFO."""
    with caplog.at_level(logging.INFO):
        log_event("INFO", "Testowy log INFO")
    assert "Testowy log INFO" in caplog.text

def test_log_event_error(caplog):
    """Test logowania na poziomie ERROR."""
    with caplog.at_level(logging.ERROR):
        log_event("ERROR", "Testowy log ERROR")
    assert "Testowy log ERROR" in caplog.text
