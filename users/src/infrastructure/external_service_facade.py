import httpx


class ExternalServiceFacade:

    def __init__(self, base_url: str):
        self.base_url = base_url

    async def proxy_get(self, endpoint: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/v1/api/{endpoint}")
            response.raise_for_status()
            return response.json()

    async def proxy_post(self, endpoint: str, data: dict) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/v1/api/{endpoint}", json=data, timeout=None)
            response.raise_for_status()
            return response.json()