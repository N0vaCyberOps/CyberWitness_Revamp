import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class EvidenceCollector:
    """Moduł do zbierania dowodów cyfrowych."""

    def collect_screenshot(self, url: str, filename: str = "screenshot.png"):
        """Zapisuje zrzut ekranu strony internetowej."""
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = None
        try:
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            driver.save_screenshot(filename)
            logging.info(f"Screenshot saved: {filename}")
        except Exception as e:
            logging.error(f"Error saving screenshot: {e}")
        finally:
            if driver:
                driver.quit()

    def collect_logs(self, log_path: str, output_path: str = "logs.txt"):
        """Kopiuje plik logów."""
        try:
            if not os.path.exists(log_path):
                raise FileNotFoundError(f"File {log_path} does not exist.")

            with open(log_path, "r") as log_file:
                log_content = log_file.read()

            with open(output_path, "w") as output_file:
                output_file.write(log_content)

            logging.info(f"Logs copied to: {output_path}")
        except Exception as e:
            logging.error(f"Error copying logs: {e}")
