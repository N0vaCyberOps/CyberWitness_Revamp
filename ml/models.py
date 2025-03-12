from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
import joblib

class AnomalyDetector:
    # Implementacja z dodanym wsparciem wielu modeli
    def __init__(self, model_type="isolation_forest"):
        self.models = {
            "isolation_forest": IsolationForest(),
            "dbscan": DBSCAN()
        }
        self.model = self.models[model_type]
        
    def save_model(self, path):
        joblib.dump(self.model, path)