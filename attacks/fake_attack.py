import requests
import logging

def simulate_brute_force_login(url, username, password_list):
    """Symuluje atak brute-force na logowanie."""
    for password in password_list:
        response = requests.post(url, data={"username": username, "password": password})
        if "Nieprawidłowe dane logowania" in response.text:
            logging.info(f"Nieudane logowanie dla {username} z hasłem {password}")
        else:
            logging.warning("Brute-force attack detected!")
            raise Exception("Brute-force attack detected")  # ✅ Rzuca wyjątek zgodny z testem
