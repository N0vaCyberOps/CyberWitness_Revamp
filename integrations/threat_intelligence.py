import aiohttp

class ThreatIntelClient:
    # Pełna implementacja z poprzedniego kodu
    # ...
    
    async def get_c2_servers(self):
        """Pobieranie znanych adresów C2"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://otx.alienvault.com/api/v1/indicators/C2",
                headers={"X-OTX-API-KEY": self.api_key}
            ) as resp:
                return await resp.json()