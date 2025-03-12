@pytest.mark.asyncio
async def test_connection_failure():
    """Test błędów połączenia z bazą danych"""
    with patch("aiosqlite.connect", side_effect=Exception("Connection failed")):
        db = DatabaseHandler({"database_file": "invalid.db"})
        
        with pytest.raises(Exception):
            await db.initialize()

@pytest.mark.asio
async def test_close_connection():
    """Test poprawnego zamykania połączenia"""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp.close()
        db = DatabaseHandler({"database_file": tmp.name})
        await db.initialize()
        
        # Symulacja otwartego połączenia
        conn = await db._get_connection()
        assert conn is not None
        
        await db.close()
        assert db._pool is None
        
    os.unlink(tmp.name)