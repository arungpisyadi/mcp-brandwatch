import os
import httpx
from typing import Any, Dict, List
from .mcp import BrandwatchProtocol

class BrandwatchAPIProtocol(BrandwatchProtocol):
    def __init__(self):
        self.base_url = os.getenv("BRANDWATCH_API_URL")
        self.client_id = os.getenv("BRANDWATCH_CLIENT_ID")
        self.access_token = None
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=30.0,
            verify=True
        )

    async def authenticate(self) -> str:
        """Authenticate with Brandwatch API"""
        if not self.access_token:
            response = await self.client.post(
                "/oauth/token",
                params={
                    "grant_type": "api-password",
                    "client_id": self.client_id
                }
            )
            response.raise_for_status()
            data = response.json()
            self.access_token = data["access_token"]
            self.client.headers["Authorization"] = f"Bearer {self.access_token}"
        return self.access_token

    async def get_mentions(self, query_id: str) -> List[Dict[str, Any]]:
        """Get mentions from Brandwatch"""
        await self.authenticate()
        response = await self.client.get(f"/mentions/{query_id}")
        response.raise_for_status()
        return response.json()

    async def create_query(self, query_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new query in Brandwatch"""
        await self.authenticate()
        response = await self.client.post(
            "/queries",
            json=query_data
        )
        response.raise_for_status()
        return response.json()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose() 