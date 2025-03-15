# Poprawiona wersja `database_handler.py` z docstringami
optimized_database_handler_with_docstring = '''"""
CyberWitness - Moduł obsługi bazy danych.
Zarządza zapisami alertów i automatycznie inicjalizuje schemat bazy.

Autor: N0vaCyberOps Team
"""

import sqlite3
import logging
import configparser
import os

# 🔹 Wczytanie konfiguracji
config = configparser.ConfigParser()
config.read("config.ini")

# 🔹 Ścieżka do bazy danych
DB_PATH = config.get("Database", "db_path", fallback="cyber_witness.db")

# 🔹 Logowanie
logger = logging.getLogger(__name__)

class DatabaseHandler:
    """Klasa obsługująca bazę danych dla CyberWitness."""

    def __init__(self):
        """Inicjalizuje połączenie z bazą i tworzy tabele, jeśli nie istnieją."""
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._initialize_schema()

    def _initialize_schema(self):
        """Tworzy tabele bazy danych, jeśli jeszcze nie istnieją."""
        schema = """
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            message TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON alerts(timestamp);
        """
        self.cursor.executescript(schema)
        self.conn.commit()

    def insert_alert(self, message):
        """Dodaje nowy alert do bazy danych.

        Args:
            message (str): Treść alertu do zapisania.
        """
        try:
            with self.conn:
                self.cursor.execute("INSERT INTO alerts (message) VALUES (?)", (message,))
                logger.info(f"Alert zapisany w bazie: {message}")
        except sqlite3.Error as e:
            logger.error(f"Błąd zapisu alertu: {e}")

    def fetch_alerts(self, limit=10):
        """Pobiera ostatnie alerty z bazy danych.

        Args:
            limit (int, optional): Liczba pobranych alertów. Domyślnie 10.

        Returns:
            list: Lista rekordów alertów.
        """
        self.cursor.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT ?", (limit,))
        return self.cursor.fetchall()

if __name__ == "__main__":
    db = DatabaseHandler()
    db.insert_alert("Test alert")
    print(db.fetch_alerts())
'''

# Zapisanie nowej wersji `database_handler.py`
database_handler_path = os.path.join(project_path, "database/database_handler.py")
if os.path.exists(database_handler_path):
    with open(database_handler_path, "w", encoding="utf-8") as f:
        f.write(optimized_database_handler_with_docstring)

# ✅ Dodane docstringi w `database_handler.py`
"✅ `database_handler.py` zaktualizowany o dokumentację!"
