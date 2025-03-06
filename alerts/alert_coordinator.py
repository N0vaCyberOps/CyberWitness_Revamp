# alerts/alert_coordinator.py
from utils.logging import log_info, log_error  # Correct import
from database.database_handler import DatabaseHandler  # Import DatabaseHandler


class AlertCoordinator:
    """
    Koordynuje obsługę alertów, w tym zapisywanie ich do bazy danych.
    """

    def __init__(self, db_handler):
        """
        Inicjalizuje koordynatora alertów.

        Args:
            db_handler (DatabaseHandler): Instancja DatabaseHandlera do interakcji z bazą danych.
        """
        if not isinstance(db_handler, DatabaseHandler):
            raise TypeError("db_handler must be an instance of DatabaseHandler")
        self.db_handler = db_handler

    async def handle_alert(self, alert_data):
        """
        Obsługuje alert, zapisując go do bazy danych.

        Args:
            alert_data (dict): Słownik z danymi alertu.  Powinien zawierać klucze
                               'timestamp', 'alert_type' i 'alert_data'.
        """
        try:
            if not isinstance(alert_data, dict):
                raise TypeError("alert_data must be a dictionary")
            if not all(key in alert_data for key in ('timestamp', 'alert_type', 'alert_data')):
                raise ValueError("alert_data must contain 'timestamp', 'alert_type', and 'alert_data' keys")

            log_info(f"🚨 Otrzymano alert: {alert_data}")
            await self.db_handler.save_alert(alert_data)

        except TypeError as e:
            log_error(f"❌ Błąd typu podczas obsługi alertu: {e}")
            raise  # Re-raise the exception after logging
        except ValueError as e:
            log_error(f"❌ Błąd wartości podczas obsługi alertu: {e}")
            raise
        except Exception as e:
            log_error(f"❌ Nieoczekiwany błąd podczas obsługi alertu: {e}")
            raise