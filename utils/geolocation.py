import requests
import os
from utils.log_event import log_event

GEOLOCATION_API = os.getenv("GEOLOCATION_API", "https://ipinfo.io/{ip}/json")

class GeoLocation:
    """Moduł do pobierania informacji geolokalizacyjnych na podstawie adresu IP."""

    @staticmethod
    def get_location(ip_address):
        """
        Pobiera lokalizację dla podanego adresu IP.

        Args:
            ip_address (str): Adres IP do sprawdzenia.

        Returns:
            dict: Słownik z informacjami o lokalizacji lub None w przypadku błędu.
        """
        try:
            response = requests.get(GEOLOCATION_API.format(ip=ip_address))
            if response.status_code == 200:
                location_data = response.json()
                log_event("GEOLOCATION_SUCCESS", f"Lokalizacja IP {ip_address}: {location_data}")
                return location_data
            else:
                log_event("GEOLOCATION_ERROR", f"Błąd pobierania lokalizacji dla {ip_address}: {response.text}", severity="ERROR")
                return None
        except Exception as e:
            log_event("GEOLOCATION_EXCEPTION", f"Błąd geolokalizacji: {e}", severity="ERROR")
            return None
