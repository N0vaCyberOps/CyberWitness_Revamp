# network/alert_coordinator.py
from database.database_handler import DatabaseHandler
from utils.log_event import log_event

class AlertCoordinator:
    def __init__(self, db_handler: DatabaseHandler):
        self.db_handler = db_handler

    async def handle_alert(self, alert_data: dict):
        """Process and save alerts."""
        try:
            await self.db_handler.save_alert(alert_data)
            log_event("INFO", f"Alert processed: {alert_data['alert_type']}")
        except Exception as e:
            log_event("ERROR", f"Alert handling failed: {e}")
            raise