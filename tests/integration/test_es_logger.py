import pytest
from elasticsearch import AsyncElasticsearch
from integrations.elasticsearch_logger import ElasticsearchLogger

@pytest.mark.asyncio
async def test_es_logging():
    # Użyj testowego klastra ES
    es = AsyncElasticsearch("http://localhost:9200")
    logger = ElasticsearchLogger(es)
    
    test_event = {
        "src_ip": "10.0.0.1",
        "alert_type": "TEST"
    }
    
    response = await logger.log_event(test_event)
    assert response['result'] == 'created'
    
    # Czyszczenie
    await es.indices.delete(index="network-anomalies")