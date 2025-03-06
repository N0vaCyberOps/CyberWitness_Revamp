import asyncio
from scapy.all import AsyncSniffer, get_if_list
from utils.logging import log_info, log_error  # Poprawiony import
from network.advanced_traffic_monitor import AdvancedTrafficMonitor
from network.packet_analyzer import analyze_packet # Usunięto niepotrzebny import save_threats
from alerts.alert_coordinator import AlertCoordinator
from database.database_handler import DatabaseHandler
import configparser

async def test_sniffer():
    """Uruchamia test sniffera."""
    config = configparser.ConfigParser()
    config.read('config.ini')

    db_handler = DatabaseHandler(config['database'])

    alert_coordinator = AlertCoordinator(db_handler)
    monitor = AdvancedTrafficMonitor(alert_coordinator, config['network'])
    await monitor.initialize()

    log_info("⏳ Sniffer działa, zbieranie pakietów przez 15 sekund...")
    try:
        await asyncio.sleep(15)
    except Exception as e:
        log_error(f"⚠️ Błąd sniffingu: {e}")

    log_info("🛑 Zatrzymuję sniffery...")
    await monitor.stop_monitoring()
    log_info("✅ Wszystkie sniffery zatrzymane.")


if __name__ == "__main__":
    asyncio.run(test_sniffer())