import pytest
from database.threat_intelligence import ThreatIntelligence  # Załóżmy że klasa istnieje

@pytest.mark.asyncio
async def test_threat_lookup():
    """Test wyszukiwania zagrożeń w bazie"""
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        ti = ThreatIntelligence(tmp.name)
        await ti.initialize()
        
        # Dodaj przykładowe zagrożenie
        await ti.add_indicator("malicious.com", "domain")
        
        # Sprawdź istniejący wskaźnik
        assert await ti.check_indicator("malicious.com")
        
        # Sprawdź nieistniejący wskaźnik
        assert not await ti.check_indicator("safe.com")