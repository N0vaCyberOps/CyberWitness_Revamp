# tests/integration/test_es_logger.py
import pytest
from elasticsearch import AsyncElasticsearch
from integrations.elasticsearch_logger import ElasticsearchLogger

@pytest.fixture(scope="module")
async def es_client():
    """Fixture do testów integracyjnych z kontenerem Docker ES"""
    client = AsyncElasticsearch("http://localhost:9200")
    yield client
    await client.close()

@pytest.mark.asyncio
async def test_full_es_integration(es_client):
    logger = ElasticsearchLogger(["http://localhost:9200"])
    
    # 1. Utwórz szablon indeksu
    await logger.create_index_template()
    
    # 2. Zaloguj testowe zdarzenie
    test_event = {
        "src_ip": "10.0.0.1",
        "alert_type": "TEST_INTEGRATION",
        "@timestamp": datetime.utcnow().isoformat()
    }
    response = await logger.log_event(test_event)
    
    # 3. Sprawdź odpowiedź ES
    assert response['result'] == 'created'
    
    # 4. Pobierz dokument z ES
    doc = await es_client.get(
        index="network-anomalies-*",
        id=response['_id']
    )
    
    # 5. Weryfikacja danych
    assert doc['_source']['src_ip'] == "10.0.0.1"
    assert doc['_source']['alert_type'] == "TEST_INTEGRATION"
    
    # 6. Czyszczenie
    await es_client.indices.delete(index="network-anomalies-*")