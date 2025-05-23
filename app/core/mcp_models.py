from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

# Protocol Layer
class BrandwatchBaseProtocol(ABC):
    @abstractmethod
    async def authenticate(self) -> str:
        """Authenticate with Brandwatch API"""
        pass

# Content Layer
class BrandwatchQueryContent(BaseModel):
    name: str = Field(..., description="Nama query yang unik")
    boolean_query: str = Field(..., description="Query pencarian boolean")
    languages: Optional[List[str]] = Field(default=["en"], description="Daftar bahasa")
    content_sources: Optional[List[str]] = Field(default=["twitter", "blog", "forum"], description="Sumber konten")
    start_date: Optional[str] = Field(default=None, description="Tanggal mulai")
    location_filter: Optional[Dict[str, List[str]]] = Field(default=None, description="Filter lokasi")
    image_filter: Optional[Dict[str, Any]] = Field(default=None, description="Filter gambar")

class BrandwatchMentionContent(BaseModel):
    query_id: str = Field(..., description="ID query")
    start_date: Optional[str] = Field(default=None, description="Tanggal mulai")
    end_date: Optional[str] = Field(default=None, description="Tanggal selesai")
    page_size: int = Field(default=100, ge=1, le=5000, description="Jumlah hasil per halaman")
    page: int = Field(default=0, ge=0, description="Nomor halaman")
    order_by: str = Field(default="added", description="Urutan berdasarkan")
    order_direction: str = Field(default="desc", description="Arah pengurutan")

class BrandwatchProjectContent(BaseModel):
    name: str = Field(..., description="Nama project")
    description: Optional[str] = Field(default=None, description="Deskripsi project")

# Model Layer
class BrandwatchQueryModel:
    def __init__(self, protocol: BrandwatchBaseProtocol):
        self.protocol = protocol

    async def create_query(self, content: BrandwatchQueryContent) -> Dict[str, Any]:
        """Create a new query using the protocol layer"""
        return await self.protocol.create_query(content.model_dump())

    async def validate_query(self, content: BrandwatchQueryContent) -> Dict[str, Any]:
        """Validate query before creation"""
        return await self.protocol.validate_query(content.model_dump())

class BrandwatchMentionModel:
    def __init__(self, protocol: BrandwatchBaseProtocol):
        self.protocol = protocol

    async def get_mentions(self, content: BrandwatchMentionContent) -> List[Dict[str, Any]]:
        """Get mentions using the protocol layer"""
        return await self.protocol.get_mentions(content.model_dump())

class BrandwatchProjectModel:
    def __init__(self, protocol: BrandwatchBaseProtocol):
        self.protocol = protocol

    async def create_project(self, content: BrandwatchProjectContent) -> Dict[str, Any]:
        """Create a new project using the protocol layer"""
        return await self.protocol.create_project(content.model_dump())

    async def get_projects(self) -> List[Dict[str, Any]]:
        """Get all projects using the protocol layer"""
        return await self.protocol.get_projects() 