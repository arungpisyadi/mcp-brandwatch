from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# Protocol Layer
class BrandwatchBaseProtocol(ABC):
    @abstractmethod
    async def authenticate(self) -> str:
        """Authenticate with Brandwatch API"""
        pass

# Content Layer
class BrandwatchUserContent(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., description="User's username")
    full_name: Optional[str] = Field(default=None, description="User's full name")
    role: str = Field(default="user", description="User's role")
    is_active: bool = Field(default=True, description="User's active status")

class BrandwatchClientContent(BaseModel):
    name: str = Field(..., description="Client's name")
    description: Optional[str] = Field(default=None, description="Client's description")
    api_key: str = Field(..., description="Client's API key")
    rate_limit: int = Field(default=30, description="Rate limit per 10 minutes")
    is_active: bool = Field(default=True, description="Client's active status")

class BrandwatchQueryContent(BaseModel):
    name: str = Field(..., description="Unique query name")
    boolean_query: str = Field(..., description="Boolean search query")
    languages: Optional[List[str]] = Field(default=["en"], description="List of languages")
    content_sources: Optional[List[str]] = Field(default=["twitter", "blog", "forum"], description="Content sources")
    start_date: Optional[str] = Field(default=None, description="Start date")
    location_filter: Optional[Dict[str, List[str]]] = Field(default=None, description="Location filter")
    image_filter: Optional[Dict[str, Any]] = Field(default=None, description="Image filter")

class BrandwatchMentionContent(BaseModel):
    query_id: str = Field(..., description="Query ID")
    start_date: Optional[str] = Field(default=None, description="Start date")
    end_date: Optional[str] = Field(default=None, description="End date")
    page_size: int = Field(default=100, ge=1, le=5000, description="Results per page")
    page: int = Field(default=0, ge=0, description="Page number")
    order_by: str = Field(default="added", description="Order by field")
    order_direction: str = Field(default="desc", description="Order direction")

class BrandwatchProjectContent(BaseModel):
    name: str = Field(..., description="Project name")
    description: Optional[str] = Field(default=None, description="Project description")

class BrandwatchMeContent(BaseModel):
    email: EmailStr = Field(..., description="Current user's email address")
    username: str = Field(..., description="Current user's username")
    full_name: Optional[str] = Field(default=None, description="Current user's full name")
    role: str = Field(..., description="Current user's role")
    is_active: bool = Field(..., description="Current user's active status")
    last_login: Optional[datetime] = Field(default=None, description="Last login time")
    created_at: datetime = Field(..., description="Account creation time")
    updated_at: datetime = Field(..., description="Last account update time")

# Model Layer
class BrandwatchUserModel:
    def __init__(self, protocol: BrandwatchBaseProtocol):
        self.protocol = protocol

    async def create_user(self, content: BrandwatchUserContent) -> Dict[str, Any]:
        """Create a new user using the protocol layer"""
        return await self.protocol.create_user(content.model_dump())

    async def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get user details using the protocol layer"""
        return await self.protocol.get_user(user_id)

    async def update_user(self, user_id: str, content: BrandwatchUserContent) -> Dict[str, Any]:
        """Update user details using the protocol layer"""
        return await self.protocol.update_user(user_id, content.model_dump())

    async def delete_user(self, user_id: str) -> Dict[str, Any]:
        """Delete user using the protocol layer"""
        return await self.protocol.delete_user(user_id)

class BrandwatchClientModel:
    def __init__(self, protocol: BrandwatchBaseProtocol):
        self.protocol = protocol

    async def create_client(self, content: BrandwatchClientContent) -> Dict[str, Any]:
        """Create a new client using the protocol layer"""
        return await self.protocol.create_client(content.model_dump())

    async def get_client(self, client_id: str) -> Dict[str, Any]:
        """Get client details using the protocol layer"""
        return await self.protocol.get_client(client_id)

    async def update_client(self, client_id: str, content: BrandwatchClientContent) -> Dict[str, Any]:
        """Update client details using the protocol layer"""
        return await self.protocol.update_client(client_id, content.model_dump())

    async def delete_client(self, client_id: str) -> Dict[str, Any]:
        """Delete client using the protocol layer"""
        return await self.protocol.delete_client(client_id)

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

class BrandwatchMeModel:
    def __init__(self, protocol: BrandwatchBaseProtocol):
        self.protocol = protocol

    async def get_me(self) -> Dict[str, Any]:
        """Get current user details using the protocol layer"""
        return await self.protocol.get_me()

    async def update_me(self, content: BrandwatchMeContent) -> Dict[str, Any]:
        """Update current user details using the protocol layer"""
        return await self.protocol.update_me(content.model_dump()) 