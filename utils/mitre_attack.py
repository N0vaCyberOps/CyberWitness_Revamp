import json

class MITREAttack:
    """Moduł do mapowania zagrożeń na MITRE ATT&CK."""

    def __init__(self, mapping_file="database/mitre_mapping.json"):
        with open(mapping_file, "r") as f:
            self.mapping = json.load(f)

    def map_threat(self, attack_type):
        """Zwraca taktykę MITRE ATT&CK dla danego zagrożenia."""
        return self.mapping.get(attack_type, "Unknown Tactic")

# Test
if __name__ == "__main__":
    mitre = MITREAttack()
    print(mitre.map_threat("DDoS Attack"))
