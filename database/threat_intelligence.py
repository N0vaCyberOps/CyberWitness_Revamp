import json
import os

class ThreatIntelligenceDatabase:
    """Baza danych dla analizy zagrożeń"""
    def __init__(self, db_path="database/threat_intelligence.json"):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """Tworzy plik bazy danych, jeśli nie istnieje"""
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as db_file:
                json.dump([], db_file)

    def log_threat(self, threat_data):
        """Zapisuje zagrożenie do pliku JSON"""
        with open(self.db_path, 'r+') as db_file:
            data = json.load(db_file)
            data.append(threat_data)
            db_file.seek(0)
            json.dump(data, db_file, indent=4)

    def get_all_threats(self):
        """Zwraca wszystkie zagrożenia"""
        with open(self.db_path, 'r') as db_file:
            return json.load(db_file)
