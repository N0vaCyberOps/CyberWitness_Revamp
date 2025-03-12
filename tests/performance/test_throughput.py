import pytest
import asyncio
from scapy.all import Ether, IP, TCP
from network.threat_detector import ThreatDetector

@pytest.mark.benchmark
@pytest.mark.asyncio
async def test_packet_processing_speed(benchmark):
    detector = ThreatDetector(...)  # Inicjalizacja z mockami
    packet = Ether()/IP()/TCP()
    
    # Test 10k pakietów
    async def process_batch():
        for _ in range(10_000):
            await detector.process_packet(packet)
    
    # Pomiar czasu
    time_taken = await benchmark(process_batch)
    assert time_taken < 1.0  # Cel: 10k/s