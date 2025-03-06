import configparser
import logging
import time
import sys

from utils.logging import log_info, log_error, setup_logging
from alerts.alert_coordinator import AlertCoordinator
from network.advanced_traffic_monitor import AdvancedTrafficMonitor
from database.database_handler import DatabaseHandler, init_db #Import init_db
from utils.exception_handler import handle_exception
from utils.performance_monitor import PerformanceMonitor


def main():
    """Główna funkcja programu Cyber Witness."""

    try:
        # Konfiguracja
        config = configparser.ConfigParser()
        config.read('config.ini')

        # Inicjalizacja logowania
        setup_logging(config['logging'])

        log_info("Uruchamianie Cyber Witness...")

        # Inicjalizacja monitora wydajności
        performance_monitor = PerformanceMonitor()
        performance_monitor.start()


        # Inicjalizacja bazy danych - *before* creating the handler
        init_db(config['database']['database_file'])
        db_handler = DatabaseHandler(config['database'])

        # Inicjalizacja koordynatora alertów
        alert_coordinator = AlertCoordinator(db_handler)

        # Inicjalizacja monitora ruchu sieciowego
        traffic_monitor = AdvancedTrafficMonitor(alert_coordinator, config['network'])
        traffic_monitor.start_monitoring()

        # Symulacja działania programu (np. oczekiwanie na zdarzenia)
        try:
            while True:
                time.sleep(1)
                performance_monitor.tick()  # Check performance

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