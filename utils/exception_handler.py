import logging
import sys

def global_exception_handler(exc_type, exc_value, exc_traceback):
    """Globalny handler wyjątków - loguje wszystkie błędy"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.error("❌ Wystąpił nieobsłużony wyjątek!", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = global_exception_handler
