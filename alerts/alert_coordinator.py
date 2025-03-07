# alerts/alert_coordinator.py
from utils.logging import log_info, log_error
from database.database_handler import DatabaseHandler  # Corrected import


class AlertCoordinator:
    """
    Koordynuje obsługę alertów (powiadomienia, zapis do bazy danych).
    """

    def __init__(self, db_handler):
        """
        Inicjalizuje koordynatora alertów.

        Args:
            db_handler (DatabaseHandler): Instancja DatabaseHandlera.
        """
        if not isinstance(db_handler, DatabaseHandler):
            raise TypeError("db_handler musi być instancją DatabaseHandler")
        self.db_handler = db_handler

    async def handle_alert(self, alert_data):
        """
        Obsługuje alert.  Obecnie: zapisuje do bazy danych.
        Docelowo: wysyłanie powiadomień, itp.

        Args:
            alert_data (dict): Dane alertu.  Powinny zawierać: timestamp,
                               source_ip, destination_ip, protocol,
                               threat_level, details.
        """
        try:
            if not isinstance(alert_data, dict):
                raise TypeError("alert_data musi być słownikiem")
            required_keys = ("timestamp", "source_ip", "destination_ip", "protocol", "threat_level", "details")
            if not all(key in alert_data for key in required_keys):
                raise ValueError(f"alert_data musi zawierać klucze: {required_keys}")

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