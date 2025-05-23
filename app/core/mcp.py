from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

# Protocol Layer
class BrandwatchProtocol(ABC):
    @abstractmethod
    async def authenticate(self) -> str:
        """Authenticate with Brandwatch API"""
        pass

    @abstractmethod
    async def get_mentions(self, query_id: str) -> List[Dict[str, Any]]:
        """Get mentions from Brandwatch"""
        pass

    @abstractmethod
    async def create_query(self, query_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new query in Brandwatch"""
        pass

# Content Layer
class BrandwatchContent(BaseModel):
    query_id: str
    name: str
    boolean_query: str
    languages: List[str]
    content_sources: List[str]
    start_date: str
    location_filter: Optional[Dict[str, List[str]]] = None
    image_filter: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

# Model Layer
class BrandwatchModel:
    def __init__(self, protocol: BrandwatchProtocol):
        self.protocol = protocol

    async def get_mentions(self, query_id: str) -> List[Dict[str, Any]]:
        """Get mentions using the protocol layer"""
        return await self.protocol.get_mentions(query_id)

    async def create_query(self, content: BrandwatchContent) -> Dict[str, Any]:
        """Create a new query using the protocol layer"""
        return await self.protocol.create_query(content.model_dump()) 