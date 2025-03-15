# Poprawiona wersja `alert_coordinator.py` z docstringami
optimized_alert_coordinator_with_docstring = '''"""
CyberWitness - Moduł zarządzania alertami.
Obsługuje kolejkę alertów i limituje ich częstotliwość.

Autor: N0vaCyberOps Team
"""

import asyncio
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
    """Klasa zarządzająca alertami w CyberWitness."""

    def __init__(self):
        """Inicjalizuje kolejkę alertów i czas ostatniego powiadomienia."""
        self.last_alert_time = None
        self.alert_queue = asyncio.Queue()

    async def send_alert(self, message):
        """Dodaje alert do kolejki, jeśli nie jest aktywny cooldown."""
        current_time = datetime.now()

        if self.last_alert_time and (current_time - self.last_alert_time).seconds < ALERT_COOLDOWN:
            logger.warning("Alert cooldown active. Skipping alert.")
            return

        self.last_alert_time = current_time
        await self.alert_queue.put(message)
        logger.info(f"Queued alert: {message}")

    async def process_alerts(self):
        """Obsługuje kolejkę alertów, wysyłając je w odpowiednich odstępach czasu."""
        while True:
            message = await self.alert_queue.get()
            logger.info(f"Processing alert: {message}")
            await asyncio.sleep(1)  # Symulacja opóźnienia wysyłki

async def main():
    """Uruchamia moduł alertów."""
    alert_system = AlertCoordinator()
    await asyncio.gather(alert_system.process_alerts())

if __name__ == "__main__":
    asyncio.run(main())
'''

# Zapisanie nowej wersji `alert_coordinator.py`
alert_coordinator_path = os.path.join(project_path, "alerts/alert_coordinator.py")
if os.path.exists(alert_coordinator_path):
    with open(alert_coordinator_path, "w", encoding="utf-8") as f:
        f.write(optimized_alert_coordinator_with_docstring)

# ✅ Dodane docstringi w `alert_coordinator.py`
"✅ `alert_coordinator.py` zaktualizowany o dokumentację!"
