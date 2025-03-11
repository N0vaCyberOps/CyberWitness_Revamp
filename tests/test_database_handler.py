# test_database_handler.py
import pytest
import tempfile
from database.database_handler import DatabaseHandler

@pytest.mark.asyncio
async def test_get_recent_alerts():
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        db = DatabaseHandler({"database_file": tmp.name})
        await db.initialize()
        
        # Test pustej bazy
        assert await db.get_recent_alerts() == []
        
        # Test z danymi
        await db.save_alert("TEST", {"key": "value"})
        results = await db.get_recent_alerts()
        assert len(results) == 1
        assert results[0]["alert_type"] == "TEST"