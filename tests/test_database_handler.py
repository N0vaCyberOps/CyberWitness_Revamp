import pytest
import tempfile
from database.database_handler import DatabaseHandler

@pytest.mark.asyncio
async def test_get_recent_alerts():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db = DatabaseHandler({"database_file": tmp.name})
        await db.initialize()

        # Test pustej bazy
        assert await db.get_recent_alerts() == []
