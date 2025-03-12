async def main():
    from network.threat_detector import ThreatDetector
    from integrations import ThreatIntelClient, ElasticsearchLogger
    
    intel = ThreatIntelClient("API_KEY")
    es = ElasticsearchLogger(["es01:9200"])
    detector = ThreatDetector(intel, es)
    
    await intel.update_signatures()
    await es.create_index_template()
    
    while True:
        packet = await get_packet()  # Funkcja do implementacji
        await detector.process_packet(packet)