import time
import random
import requests
from typing import List
from utils.log_event import log_event

def simulate_brute_force_login(url: str, username: str, password_list: List[str]) -> bool:
    """Wersja zgodna z testami"""
    try:
        for password in password_list:
            time.sleep(0.5 + random.uniform(-0.3, 0.3))
            response = requests.post(
                url,
                data={"username": username, "password": password},
                timeout=5
            )
            if "incorrect" not in response.text.lower():
                log_event("WARNING", "Brute-force attack detected!")
                raise RuntimeError("Brute-force attack detected!")  # Zmieniony wyjątek
        return False
    except requests.RequestException as e:
        log_event("ERROR", f"Request failed: {e}")
        return False