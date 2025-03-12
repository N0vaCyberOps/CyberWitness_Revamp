from elasticsearch import AsyncElasticsearch
from datetime import datetime

class ElasticsearchLogger:
    # Pełna implementacja z poprzedniego kodu
    # ...

    async def create_index_template(self):
        """Automatyczna konfiguracja indeksu w ES"""
        await self.es.indices.put_template(
            name="network-anomalies",
            body={
                "index_patterns": ["network-anomalies*"],
                "mappings": {
                    "properties": {
                        "@timestamp": {"type": "date"},
                        "ja3_hash": {"type": "keyword"},
                        "src_ip": {"type": "ip"}
                    }
                }
            }
        )