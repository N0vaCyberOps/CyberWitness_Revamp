import numpy as np
from sklearn.ensemble import IsolationForest
from utils.log_event import log_event

class AIAnalyzer:
    """Moduł AI do wykrywania anomalii w pakietach sieciowych."""

    def __init__(self):
        """
        Inicjalizuje model AI (Isolation Forest) do wykrywania anomalii.
        """
        self.model = IsolationForest(contamination=0.05, random_state=42)
        self.training_data = []

    def train_model(self, packets):
        """
        Trenuje model AI na podstawie historycznych pakietów.

        Args:
            packets (list): Lista cech pakietów do nauki.
        """
        if len(packets) > 10:  # Minimalna liczba próbek do nauki
            self.training_data = np.array(packets)
            self.model.fit(self.training_data)
            log_event("AI_TRAINED", "Model AI został przetrenowany.")

    def extract_features(self, packet):
        """
        Ekstrahuje cechy z pakietu sieciowego do analizy AI.

        Args:
            packet (scapy.Packet): Pakiet Scapy.

        Returns:
            list: Wektor cech.
        """
        return [
            len(packet),  # Rozmiar pakietu
            packet[0].proto if hasattr(packet[0], "proto") else 0,  # Protokół IP
            packet[0].sport if hasattr(packet[0], "sport") else 0,  # Port źródłowy
            packet[0].dport if hasattr(packet[0], "dport") else 0,  # Port docelowy
        ]

    def detect_anomaly(self, packet):
        """
        Wykrywa anomalie w pakietach sieciowych.

        Args:
            packet (scapy.Packet): Pakiet sieciowy.

        Returns:
            bool: True, jeśli wykryto anomalię, False w przeciwnym razie.
        """
        features = np.array(self.extract_features(packet)).reshape(1, -1)

        if len(self.training_data) > 10:
            prediction = self.model.predict(features)
            if prediction[0] == -1:
                log_event("ANOMALY_DETECTED", f"Anomalia wykryta w pakiecie: {packet.summary()}", severity="WARNING")
                return True
        return False
