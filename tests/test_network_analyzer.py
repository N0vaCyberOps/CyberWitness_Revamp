@pytest.mark.asyncio
async def test_capture_interruption():
    """Test przerwania przechwytywania pakietów"""
    analyzer = NetworkAnalyzer()
    
    with patch("modules.network_analyzer.sniff") as mock_sniff:
        mock_sniff.side_effect = KeyboardInterrupt("User interruption")
        
        result = await analyzer.capture_and_analyze(count=10)
        assert result == []

@pytest.mark.asyncio
async def test_empty_capture():
    """Test przechwytywania 0 pakietów"""
    analyzer = NetworkAnalyzer()
    result = await analyzer.capture_and_analyze(count=0)
    assert result == []