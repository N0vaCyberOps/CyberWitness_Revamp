import configparser
import logging
import time
import sys

from utils.logging import log_info, log_error, setup_logging  # Import setup_logging
from alerts.alert_coordinator import AlertCoordinator
from network.advanced_traffic_monitor import AdvancedTrafficMonitor
from database.database_handler import DatabaseHandler
from utils.exception_handler import handle_exception
from utils.performance_monitor import PerformanceMonitor
from database.database_handler import init_db  # Import the init_db function


def main():
    """Główna funkcja programu Cyber Witness."""

    try:
        # Konfiguracja
        config = configparser.ConfigParser()
        config.read('config.ini')

        # Inicjalizacja logowania
        setup_logging(config['logging'])  # Use the setup_logging function

        log_info("Uruchamianie Cyber Witness...")

        # Inicjalizacja monitora wydajności
        performance_monitor = PerformanceMonitor()
        performance_monitor.start()

        # Inicjalizacja bazy danych
        init_db(config['database']['database_file'])  # Initialize the database *before* using DatabaseHandler
        db_handler = DatabaseHandler(config['database'])

        # Inicjalizacja koordynatora alertów
        alert_coordinator = AlertCoordinator(db_handler)

        # Inicjalizacja monitora ruchu sieciowego
        traffic_monitor = AdvancedTrafficMonitor(alert_coordinator, config['network'])
        traffic_monitor.start_monitoring()

        # Symulacja działania programu
        try:
            while True:
                time.sleep(1)
                performance_monitor.tick()

        except KeyboardInterrupt:
            log_info("Zatrzymywanie Cyber Witness (przechwycono KeyboardInterrupt)...")

        finally:
            traffic_monitor.stop_monitoring()
            performance_monitor.stop()
            logging.info("Cyber Witness zatrzymany.")

    except Exception as e:
        handle_exception(e)
        sys.exit(1)


if __name__ == "__main__":
    main()