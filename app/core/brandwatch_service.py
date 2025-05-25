import os
import time
from typing import List, Optional
import aiohttp
from datetime import datetime, timedelta
from app.models.brandwatch import BrandwatchProject, BrandwatchQuery, BrandwatchMention

class BrandwatchService:
    def __init__(self):
        self.api_url = os.getenv("BRANDWATCH_API_URL", "https://api.brandwatch.com")
        self.api_key = os.getenv("BRANDWATCH_API_KEY")
        self.rate_limit = 30  # calls per 10 minutes
        self.rate_window = 600  # 10 minutes in seconds
        self.calls = []
        
    def _check_rate_limit(self):
        """Check and enforce rate limiting"""
        now = time.time()
        # Remove calls older than the rate window
        self.calls = [call for call in self.calls if now - call < self.rate_window]
        
        if len(self.calls) >= self.rate_limit:
            sleep_time = self.calls[0] + self.rate_window - now
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        self.calls.append(now)

    async def _make_request(self, endpoint: str, method: str = "GET", params: Optional[dict] = None) -> dict:
        """Make API request with rate limiting and error handling"""
        self._check_rate_limit()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method,
                f"{self.api_url}/{endpoint}",
                headers=headers,
                params=params
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Brandwatch API error: {error_text}")
                return await response.json()

    async def get_projects(self) -> List[BrandwatchProject]:
        """Get list of projects"""
        data = await self._make_request("projects/summary")
        return [BrandwatchProject(**project) for project in data["results"]]

    async def get_project(self, project_id: int) -> BrandwatchProject:
        """Get specific project details"""
        data = await self._make_request(f"projects/{project_id}")
        return BrandwatchProject(**data["results"][0])

    async def get_queries(self, project_id: int) -> List[BrandwatchQuery]:
        """Get list of queries for a project"""
        data = await self._make_request(f"projects/{project_id}/queries/summary")
        return [BrandwatchQuery(**query) for query in data["results"]]

    async def get_mentions(
        self,
        project_id: int,
        query_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[BrandwatchMention]:
        """Get mentions with optional filtering"""
        params = {
            "limit": limit
        }
        
        if query_id:
            params["queryId"] = query_id
        if start_date:
            params["startDate"] = start_date.isoformat()
        if end_date:
            params["endDate"] = end_date.isoformat()
            
        data = await self._make_request(f"projects/{project_id}/mentions", params=params)
        return [BrandwatchMention(**mention) for mention in data["results"]] 