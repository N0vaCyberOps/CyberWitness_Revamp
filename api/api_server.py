# Poprawiona wersja `api_server.py` z docstringami
optimized_api_server_with_docstring = '''"""
CyberWitness - Serwer API.
Umożliwia komunikację z systemem oraz monitorowanie jego statusu.

Autor: N0vaCyberOps Team
"""

from fastapi import FastAPI, HTTPException, Depends
import uvicorn
import asyncio
import logging
import configparser

# 🔹 Wczytanie konfiguracji
config = configparser.ConfigParser()
config.read("config.ini")

# 🔹 Ustawienia API
HOST = config.get("API", "host", fallback="127.0.0.1")
PORT = int(config.get("API", "port", fallback="8000"))

# 🔹 Ustawienia rate limiting
REQUEST_LIMIT = int(config.get("API", "request_limit", fallback="5"))
TIME_WINDOW = int(config.get("API", "time_window", fallback="10"))  # sekundy

# 🔹 Logowanie
logger = logging.getLogger(__name__)

app = FastAPI()

# 🔹 Mechanizm rate limiting
request_timestamps = {}

async def rate_limiter(client_id: str):
    """Prosty mechanizm ograniczania liczby zapytań."""
    now = asyncio.get_event_loop().time()
    timestamps = request_timestamps.get(client_id, [])

    # 🔹 Usuwanie starych wpisów
    timestamps = [t for t in timestamps if now - t < TIME_WINDOW]
    request_timestamps[client_id] = timestamps

    if len(timestamps) >= REQUEST_LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests. Try again later.")

    timestamps.append(now)

@app.get("/")
async def root():
    """Endpoint główny API."""
    return {"message": "CyberWitness API is running!"}

@app.get("/status")
async def status(client_id: str, rate_limit: None = Depends(lambda: rate_limiter(client_id))):
    """Sprawdza status systemu."""
    return {"status": "OK", "rate_limit": "Request accepted"}

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
'''

# Zapisanie nowej wersji `api_server.py`
api_server_path = os.path.join(project_path, "api/api_server.py")
if os.path.exists(api_server_path):
    with open(api_server_path, "w", encoding="utf-8") as f:
        f.write(optimized_api_server_with_docstring)

# ✅ Dodane docstringi w `api_server.py`
"✅ `api_server.py` zaktualizowany o dokumentację!"
