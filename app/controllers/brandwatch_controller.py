from typing import Any, Dict, List, Optional
from datetime import datetime
from fastapi import HTTPException
from app.interfaces.base import IController
from app.presenters.brandwatch_presenter import BrandwatchPresenter
from app.core.brandwatch_service import BrandwatchService

class BrandwatchController(IController):
    def __init__(self, presenter: BrandwatchPresenter):
        self.presenter = presenter
        self.service = BrandwatchService()

    async def handle_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle request for Brandwatch operations
        """
        action = request_data.get("action")
        
        if action == "get_projects":
            projects = await self.service.get_projects()
            return self.presenter.transform_list(projects)
            
        elif action == "get_project":
            project_id = request_data.get("project_id")
            if not project_id:
                raise HTTPException(status_code=400, detail="Project ID is required")
            project = await self.service.get_project(project_id)
            return self.presenter.transform_data(project)
            
        elif action == "get_queries":
            project_id = request_data.get("project_id")
            if not project_id:
                raise HTTPException(status_code=400, detail="Project ID is required")
            queries = await self.service.get_queries(project_id)
            return self.presenter.transform_list(queries)
            
        elif action == "get_mentions":
            project_id = request_data.get("project_id")
            if not project_id:
                raise HTTPException(status_code=400, detail="Project ID is required")
                
            query_id = request_data.get("query_id")
            start_date = request_data.get("start_date")
            end_date = request_data.get("end_date")
            limit = request_data.get("limit", 100)
            
            mentions = await self.service.get_mentions(
                project_id=project_id,
                query_id=query_id,
                start_date=datetime.fromisoformat(start_date) if start_date else None,
                end_date=datetime.fromisoformat(end_date) if end_date else None,
                limit=limit
            )
            return self.presenter.transform_list(mentions)
            
        raise HTTPException(status_code=400, detail="Invalid action") 