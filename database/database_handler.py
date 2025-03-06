# database/database_handler.py
import sqlite3
import json
from utils.logging import log_info, log_error  # Correct import
import asyncio


def init_db(database_file):
    """Inicjalizuje bazę danych SQLite."""
    try:
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS threats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                source_ip TEXT,
                destination_ip TEXT,
                protocol TEXT,
                threat_level REAL,
                details TEXT
            )
        """)

        cursor.execute("""
           CREATE TABLE IF NOT EXISTS alerts (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               timestamp TEXT NOT NULL,
               alert_type TEXT,
               alert_data TEXT
           )
       """)
        conn.commit()
        conn.close()
        log_info("✅ Baza danych zainicjalizowana.")  # Added logging
    except sqlite3.Error as e:
        log_error(f"❌ Błąd inicjalizacji bazy: {e}")


class DatabaseHandler:
    """Obsługuje interakcje z bazą danych."""

    def __init__(self, config):
        """
        Inicjalizuje DatabaseHandler.
        :param config: Sekcja 'database' z pliku konfiguracyjnego.
        """
        self.database_file = config['database_file']
        # You could add connection pooling here for better performance in a production environment.

    async def save_alert(self, alert_data):
        """Asynchronicznie zapisuje alert do bazy danych."""
        try:
            # Convert alert_data to JSON string
            alert_data_json = json.dumps(alert_data['alert_data']) # Only the 'alert_data' part is JSON

            conn = sqlite3.connect(self.database_file)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO alerts (timestamp, alert_type, alert_data)
                VALUES (?, ?, ?)
            """, (alert_data['timestamp'], alert_data['alert_type'], alert_data_json)) # Use get to avoid KeyError
            conn.commit()
            conn.close()
            log_info(f"💾 Alert zapisany do bazy danych: {alert_data}")  # Corrected logging
        except sqlite3.Error as e:
            log_error(f"❌ Błąd zapisu alertu do bazy danych: {e}")
        except Exception as e:
             log_error(f"❌ Nieoczekiwany błąd przy zapisie alertu: {e}")


    async def save_threat(self, threat_data):
        """Asynchronicznie zapisuje informacje o zagrożeniu do bazy danych."""
        #  This method is correct;  it's the packet analyzer that calls it.  Keeping it async.
        try:
            conn = sqlite3.connect(self.database_file)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO threats (timestamp, source_ip, destination_ip, protocol, threat_level, details)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (threat_data['timestamp'], threat_data['source_ip'], threat_data['destination_ip'],
                  threat_data['protocol'], threat_data['threat_level'], threat_data['details']))
            conn.commit()
            conn.close()
            log_info(f"💾 Zapisano zagrożenie do bazy danych: {threat_data}")
        except sqlite3.Error as e:
            log_error(f"❌ Błąd zapisu do bazy danych: {e}")
        except Exception as e:
            log_error(f"❌ Nieoczekiwany błąd przy zapisie zagrożenia: {e}")

    async def get_recent_threats(self, limit=10):
      """Pobiera określoną liczbę ostatnich zagrożeń z bazy danych."""
      try:
          conn = sqlite3.connect(self.database_file)
          conn.row_factory = sqlite3.Row  # Ustaw row_factory, aby zwracać słowniki
          cursor = conn.cursor()
          cursor.execute("SELECT * FROM threats ORDER BY timestamp DESC LIMIT ?", (limit,))
          rows = cursor.fetchall()
          conn.close()

          # Konwertuj wiersze na listę słowników
          threats = [dict(row) for row in rows]
          return threats

      except sqlite3.Error as e:
          log_error(f"Błąd podczas pobierania zagrożeń: {e}")
          return []  # Zwróć pustą listę w przypadku błędu
      except Exception as e:
          log_error(f"Nieoczekiwany błąd: {e}")
          return []


    async def get_recent_alerts(self, limit=10):
        """Pobiera określoną liczbę ostatnich alertów z bazy danych."""
        try:
            conn = sqlite3.connect(self.database_file)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            conn.close()

            alerts = []
            for row in rows:
              alert = dict(row)
              # Parsuj dane alertu z JSON
              try:
                  alert['alert_data'] = json.loads(alert['alert_data'])
              except json.JSONDecodeError:
                  log_error(f"Błąd dekodowania JSON dla alertu ID {alert['id']}")
                  alert['alert_data'] = {}  # Ustaw puste dane, jeśli błąd
              alerts.append(alert)
            return alerts
        except sqlite3.Error as e:
            log_error(f"Błąd podczas pobierania alertów z bazy: {e}")
            return []  # Zwróć pustą listę w przypadku błędu.
        except Exception as e:
            log_error(f"Nieoczekiwany błąd: {e}")
            return []