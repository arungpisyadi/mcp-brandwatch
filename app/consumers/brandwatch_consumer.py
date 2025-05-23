import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from app.core.mcp_models import (
    BrandwatchQueryContent,
    BrandwatchMentionContent,
    BrandwatchProjectContent,
    BrandwatchUserContent,
    BrandwatchClientContent,
    BrandwatchQueryModel,
    BrandwatchMentionModel,
    BrandwatchProjectModel,
    BrandwatchUserModel,
    BrandwatchClientModel
)
from app.core.brandwatch_protocol import BrandwatchAPIProtocol

logger = logging.getLogger(__name__)

class BrandwatchConsumer:
    def __init__(self):
        self.user_model = None
        self.client_model = None
        self.query_model = None
        self.mention_model = None
        self.project_model = None
        self.last_poll_time = None
        self.poll_interval = 600  # 10 menit sesuai rate limit Brandwatch

    async def initialize(self):
        """Initialize models with protocol"""
        async with BrandwatchAPIProtocol() as protocol:
            self.user_model = BrandwatchUserModel(protocol)
            self.client_model = BrandwatchClientModel(protocol)
            self.query_model = BrandwatchQueryModel(protocol)
            self.mention_model = BrandwatchMentionModel(protocol)
            self.project_model = BrandwatchProjectModel(protocol)

    # User methods
    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        try:
            content = BrandwatchUserContent(**user_data)
            result = await self.user_model.create_user(content)
            logger.info(f"User created successfully: {result['id']}")
            return result
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise

    async def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get user details"""
        try:
            result = await self.user_model.get_user(user_id)
            logger.info(f"Retrieved user: {user_id}")
            return result
        except Exception as e:
            logger.error(f"Error getting user: {str(e)}")
            raise

    async def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user details"""
        try:
            content = BrandwatchUserContent(**user_data)
            result = await self.user_model.update_user(user_id, content)
            logger.info(f"User updated successfully: {user_id}")
            return result
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            raise

    async def delete_user(self, user_id: str) -> Dict[str, Any]:
        """Delete user"""
        try:
            result = await self.user_model.delete_user(user_id)
            logger.info(f"User deleted successfully: {user_id}")
            return result
        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}")
            raise

    # Client methods
    async def create_client(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new client"""
        try:
            content = BrandwatchClientContent(**client_data)
            result = await self.client_model.create_client(content)
            logger.info(f"Client created successfully: {result['id']}")
            return result
        except Exception as e:
            logger.error(f"Error creating client: {str(e)}")
            raise

    async def get_client(self, client_id: str) -> Dict[str, Any]:
        """Get client details"""
        try:
            result = await self.client_model.get_client(client_id)
            logger.info(f"Retrieved client: {client_id}")
            return result
        except Exception as e:
            logger.error(f"Error getting client: {str(e)}")
            raise

    async def update_client(self, client_id: str, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update client details"""
        try:
            content = BrandwatchClientContent(**client_data)
            result = await self.client_model.update_client(client_id, content)
            logger.info(f"Client updated successfully: {client_id}")
            return result
        except Exception as e:
            logger.error(f"Error updating client: {str(e)}")
            raise

    async def delete_client(self, client_id: str) -> Dict[str, Any]:
        """Delete client"""
        try:
            result = await self.client_model.delete_client(client_id)
            logger.info(f"Client deleted successfully: {client_id}")
            return result
        except Exception as e:
            logger.error(f"Error deleting client: {str(e)}")
            raise

    # Query methods
    async def create_query(self, query_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new query"""
        try:
            content = BrandwatchQueryContent(**query_data)
            # Validate query first
            await self.query_model.validate_query(content)
            # Create query if validation passes
            result = await self.query_model.create_query(content)
            logger.info(f"Query created successfully: {result['id']}")
            return result
        except Exception as e:
            logger.error(f"Error creating query: {str(e)}")
            raise

    # Mention methods
    async def poll_mentions(self, query_id: str) -> List[Dict[str, Any]]:
        """Poll mentions for a query"""
        try:
            # Check rate limit
            if self.last_poll_time:
                time_since_last_poll = (datetime.now() - self.last_poll_time).total_seconds()
                if time_since_last_poll < self.poll_interval:
                    await asyncio.sleep(self.poll_interval - time_since_last_poll)

            # Get mentions
            content = BrandwatchMentionContent(
                query_id=query_id,
                start_date=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
                end_date=datetime.now().strftime("%Y-%m-%d"),
                page_size=100,
                page=0,
                order_by="added",
                order_direction="desc"
            )
            result = await self.mention_model.get_mentions(content)
            self.last_poll_time = datetime.now()
            logger.info(f"Retrieved {len(result)} mentions for query {query_id}")
            return result
        except Exception as e:
            logger.error(f"Error polling mentions: {str(e)}")
            raise

    # Project methods
    async def create_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new project"""
        try:
            content = BrandwatchProjectContent(**project_data)
            result = await self.project_model.create_project(content)
            logger.info(f"Project created successfully: {result['id']}")
            return result
        except Exception as e:
            logger.error(f"Error creating project: {str(e)}")
            raise

    async def get_projects(self) -> List[Dict[str, Any]]:
        """Get all projects"""
        try:
            result = await self.project_model.get_projects()
            logger.info(f"Retrieved {len(result)} projects")
            return result
        except Exception as e:
            logger.error(f"Error getting projects: {str(e)}")
            raise

    async def start_polling(self, query_id: str, callback):
        """Start polling mentions for a query"""
        while True:
            try:
                mentions = await self.poll_mentions(query_id)
                if mentions:
                    await callback(mentions)
            except Exception as e:
                logger.error(f"Error in polling loop: {str(e)}")
            await asyncio.sleep(self.poll_interval) 