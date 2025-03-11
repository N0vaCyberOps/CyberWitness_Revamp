import pytest
from unittest.mock import patch, MagicMock
from attacks.fake_attack import simulate_brute_force_login

@patch("requests.post")
def test_simulate_brute_force_login_failure(mock_post):
    """Testuje symulację brute-force z błędnymi hasłami."""
    mock_response = MagicMock()
    mock_response.text = "Nieprawidłowe dane logowania"
    mock_post.return_value = mock_response

    with pytest.raises(Exception, match="Brute-force attack detected"):  # ✅ Poprawiony test
        simulate_brute_force_login("http://example.com/login", "admin", ["wrong"])
