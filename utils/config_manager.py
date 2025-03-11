import json

class ConfigManager:
    """Zarządza konfiguracją aplikacji."""
    _instance = None

    def __new__(cls, config_path="config.json"):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.config_path = config_path
            cls._instance.config = None
        return cls._instance

    def _load_config(self):
        """Wczytuje konfigurację z pliku."""
        try:
            with open(self.config_path, "r") as file:
                self.config = json.load(file)
        except FileNotFoundError:
            self.config = {}

    def get_config(self, key, default=None):
        """Zwraca wartość konfiguracji dla danego klucza."""
        if self.config is None:
            self._load_config()
        return self.config.get(key, default)

    def validate_config(self):
        """Waliduje konfigurację."""
        if not self.get_config("api_key"):
            raise ValueError("API key is missing in config")
        return True

# Przykładowe użycie
if __name__ == "__main__":
    config = ConfigManager("config.json") # config.json musi istnieć w tym samym folderze
    print(config.get_config("test_key", "default_value"))