@pytest.mark.asyncio
async def test_concurrent_access():
    """Test równoczesnego dostępu do bazy danych"""
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        db = DatabaseHandler({"database_file": tmp.name})
        await db.initialize()

        async def insert_alert(i):
            await db.save_alert({
                "timestamp": f"2024-01-01 00:00:{i:02d}",
                "alert_type": "TEST",
                "alert_data": {"id": i}
            })

        # Wykonaj 10 równoległych zapisów
        tasks = [insert_alert(i) for i in range(10)]
        await asyncio.gather(*tasks)

        alerts = await db.get_recent_alerts(10)
        assert len(alerts) == 10

@pytest.mark.asyncio
async def test_invalid_alert_data():
    """Test zapisu niepełnych danych alertu"""
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        db = DatabaseHandler({"database_file": tmp.name})
        await db.initialize()

        # Brak wymaganego pola 'timestamp'
        result = await db.save_alert({
            "alert_type": "INVALID",
            "alert_data": {}
        })
        assert result is False