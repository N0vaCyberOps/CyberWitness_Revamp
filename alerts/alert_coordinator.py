class AlertCoordinator:
    def __init__(self, config=None):
        """
        Inicjalizuje koordynatora alertów.
        
        :param config: Opcjonalna konfiguracja (np. ustawienia alertów).
        """
        self.config = config
        print("✅ AlertCoordinator initialized!")

    async def initialize(self):
        """
        Inicjalizuje moduł alertów (jeśli wymagane są jakieś operacje startowe).
        """
        print("🔄 AlertCoordinator is initializing...")

    def send_alert(self, message):
        """
        Wysyła alert z podanym komunikatem.

        :param message: Treść alertu.
        """
        print(f"⚠️ ALERT: {message}")

    def get_alert_settings(self):
        """
        Zwraca ustawienia alertów, jeśli są dostępne.
        """
        return self.config if self.config else "No config provided"
