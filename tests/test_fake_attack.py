import unittest
from unittest.mock import patch, MagicMock
from attacks.fake_attack import simulate_brute_force_login

class TestFakeThreat(unittest.TestCase):

    @patch("requests.post")
    def test_simulate_brute_force_login_failure(self, mock_post):
        """Testuje symulację brute-force z błędnymi hasłami."""
        mock_response = MagicMock()
        mock_response.text = "Nieprawidłowe dane logowania"
        mock_post.return_value = mock_response

        with self.assertLogs(level="INFO") as cm:
            simulate_brute_force_login("http://example.com/login", "admin", ["wrong"])

        self.assertTrue(any("Nieprawidłowe dane logowania" in msg for msg in cm.output))

if __name__ == "__main__":
    unittest.main()
