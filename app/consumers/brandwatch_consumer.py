import asyncio
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
from app.core.mcp_models import (
    BrandwatchQueryContent,
    BrandwatchMentionContent,
    BrandwatchProjectContent,
    BrandwatchQueryModel,
    BrandwatchMentionModel,
    BrandwatchProjectModel
)
from app.core.brandwatch_protocol import BrandwatchAPIProtocol

logger = logging.getLogger(__name__)

class BrandwatchConsumer:
    def __init__(self):
        self.query_model = None
        self.mention_model = None
        self.project_model = None
        self.last_poll_time = None
        self.poll_interval = 600  # 10 menit sesuai rate limit Brandwatch

    async def initialize(self):
        """Initialize models with protocol"""
        async with BrandwatchAPIProtocol() as protocol:
            self.query_model = BrandwatchQueryModel(protocol)
            self.mention_model = BrandwatchMentionModel(protocol)
            self.project_model = BrandwatchProjectModel(protocol)

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