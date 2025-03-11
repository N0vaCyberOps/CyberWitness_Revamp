class AlertCoordinator:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    async def handle_alert(self, alert_data):  # ✅ Poprawione: Dodano self
        """Obsługuje przychodzący alert i zapisuje go w bazie danych."""
        try:
            await self.db_handler.save_alert(alert_data)
            return {"status": "success", "message": "Alert zapisany."}
        except Exception as e:
            return {"status": "error", "message": str(e)}
