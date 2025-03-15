# Refaktoryzacja `alert_coordinator.py`: optymalizacja obsługi alertów
alert_coordinator_path = os.path.join(project_path, "alerts/alert_coordinator.py")

if os.path.exists(alert_coordinator_path):
    with open(alert_coordinator_path, "r", encoding="utf-8") as f:
        alert_coordinator_code = f.read()

    # Poprawiona wersja `alert_coordinator.py` - dodanie limitów czasowych i obsługi kolejek
    optimized_alert_coordinator_code = """import asyncio
import logging
import configparser
from datetime import datetime, timedelta

# 🔹 Wczytanie konfiguracji
config = configparser.ConfigParser()
config.read("config.ini")

# 🔹 Logowanie
logger = logging.getLogger(__name__)

# 🔹 Ustawienia limitów alertów
ALERT_COOLDOWN = int(config.get("Alerts", "cooldown_seconds", fallback="30"))

class AlertCoordinator:
    def __init__(self):
        self.last_alert_time = None
        self.alert_queue = asyncio.Queue()

    async def send_alert(self, message):
        current_time = datetime.now()

        # 🔹 Sprawdzenie cooldownu dla alertów
        if self.last_alert_time and (current_time - self.last_alert_time).seconds < ALERT_COOLDOWN:
            logger.warning("Alert cooldown active. Skipping alert.")
            return

        self.last_alert_time = current_time
        await self.alert_queue.put(message)
        logger.info(f"Queued alert: {message}")

    async def process_alerts(self):
        while True:
            message = await self.alert_queue.get()
            logger.info(f"Processing alert: {message}")
            # 🔹 Tutaj można dodać obsługę wysyłania (np. e-mail, SMS)
            await asyncio.sleep(1)  # Symulacja opóźnienia wysyłki

async def main():
    alert_system = AlertCoordinator()
    await asyncio.gather(alert_system.process_alerts())

if __name__ == "__main__":
    asyncio.run(main())
"""

    # Nadpisanie `alert_coordinator.py` zoptymalizowanym kodem
    with open(alert_coordinator_path, "w", encoding="utf-8") as f:
        f.write(optimized_alert_coordinator_code)

    "✅ `alert_coordinator.py` zoptymalizowany!"
