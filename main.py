# main.py
import asyncio
import configparser
import logging
import sys

from utils.logging import log_info, log_error, setup_logging  # Poprawiony import
from alerts.alert_coordinator import AlertCoordinator
from network.advanced_traffic_monitor import AdvancedTrafficMonitor
from database.database_handler import DatabaseHandler, init_db
from utils.exception_handler import handle_exception


async def main():
    """Główna funkcja programu Cyber Witness."""

    # Konfiguracja logowania
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
    except configparser.Error as e:
        print(f"Błąd wczytywania pliku konfiguracyjnego config.ini: {e}")
        sys.exit(1)

    try:
        setup_logging(config['logging']) #Konfiguracja z pliku
    except (KeyError, configparser.NoSectionError) as e:
        print(f"Błąd konfiguracji logowania: {e}. Sprawdź plik config.ini.")
        sys.exit(1)

    log_info("Uruchamianie Cyber Witness...")

    # Inicjalizacja bazy danych, przed utworzeniem handlera
    try:
        await init_db(config['database']['database_file'])
        db_handler = DatabaseHandler(config['database'])
    except KeyError:
        log_error("Brak sekcji [database] lub klucza 'database_file' w config.ini.")
        sys.exit(1)
    except Exception as e:
        handle_exception(e)
        sys.exit(1)


    # Inicjalizacja koordynatora alertów
    alert_coordinator = AlertCoordinator(db_handler)

    # Inicjalizacja monitora ruchu
    try:
        traffic_monitor = AdvancedTrafficMonitor(alert_coordinator, config['network'])
        await traffic_monitor.start_monitoring()
    except KeyError:
        log_error("Brak sekcji [network] lub klucza 'interface' w config.ini.")
        sys.exit(1)
    except Exception as e:
        handle_exception(e)  # Ogólna obsługa błędów, w tym błędów Scapy
        sys.exit(1)

    log_info("Monitoring ruchu sieciowego uruchomiony. Wciśnij CTRL+C, aby zatrzymać.")

    # Główna pętla
    try:
        while True:
            await asyncio.sleep(1)  # Czekaj 1 sekundę, nie blokuj CPU

    except KeyboardInterrupt:
        log_info("Zatrzymywanie Cyber Witness (przechwycono KeyboardInterrupt)...")
    finally:
        if 'traffic_monitor' in locals(): # Sprawdź, czy obiekt istnieje
            await traffic_monitor.stop_monitoring()
        if 'db_handler' in locals(): # Sprawdz
            await db_handler.close()
        log_info("Cyber Witness zatrzymany.")



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        handle_exception(e)
        sys.exit(1)