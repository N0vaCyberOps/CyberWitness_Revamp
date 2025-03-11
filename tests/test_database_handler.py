import pytest
import tempfile
import aiosqlite
from database.database_handler import DatabaseHandler, init_db

@pytest.mark.asyncio
async def test_get_recent_alerts_empty():
    """Test sprawdza, czy zwracana lista alertów jest pusta dla nowej bazy."""
    async with tempfile.NamedTemporaryFile(delete=False) as temp_db_file:
        db_path = temp_db_file.name

    await init_db(db_path)
    db_handler = DatabaseHandler({"database_file": db_path})

    await db_handler.connect()
    alerts = await db_handler.get_recent_alerts(5)

    assert alerts == []
