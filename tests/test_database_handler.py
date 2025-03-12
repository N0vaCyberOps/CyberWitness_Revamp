import pytest
import asyncio
import tempfile
import os
from database.database_handler import DatabaseHandler

@pytest.mark.asyncio
async def test_get_recent_alerts():
    """Test pobierania ostatnich alertów z bazy danych"""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp.close()
        db = DatabaseHandler({"database_file": tmp.name})
        await db.initialize()

        # Test pustej bazy
        assert await db.get_recent_alerts() == []

        # Dodaj testowe alerty
        for i in range(5):
            await db.save_alert({
                "timestamp": f"2024-01-01 00:00:{i:02d}",
                "alert_type": "TEST",
                "alert_data": {"id": i}
            })

        # Pobierz i zweryfikuj
        alerts = await db.get_recent_alerts(3)
        assert len(alerts) == 3
        assert alerts[0]["alert_data"] == '{"id": 4}'
        
    os.unlink(tmp.name)

@pytest.mark.asyncio
async def test_concurrent_access():
    """Test równoczesnego dostępu do bazy danych"""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp.close()
        db = DatabaseHandler({"database_file": tmp.name})
        await db.initialize()

        async def insert_alert(i):
            await db.save_alert({
                "timestamp": f"2024-01-01 00:00:{i:02d}",
                "alert_type": "TEST",
                "alert_data": {"id": i}
            })

        tasks = [insert_alert(i) for i in range(10)]
        await asyncio.gather(*tasks)

        alerts = await db.get_recent_alerts(10)
        assert len(alerts) == 10
        
    os.unlink(tmp.name)

@pytest.mark.asyncio
async def test_invalid_alert_data():
    """Test zapisu niepełnych danych alertu"""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp.close()
        db = DatabaseHandler({"database_file": tmp.name})
        await db.initialize()

        result = await db.save_alert({
            "alert_type": "INVALID",
            "alert_data": {}
        })
        assert result is False
        
    os.unlink(tmp.name)