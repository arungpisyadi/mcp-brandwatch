from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime
from app.controllers.brandwatch_controller import BrandwatchController
from app.presenters.brandwatch_presenter import BrandwatchPresenter

router = APIRouter()
brandwatch_presenter = BrandwatchPresenter()
brandwatch_controller = BrandwatchController(brandwatch_presenter)

@router.get("/projects")
async def get_projects():
    """
    Get list of all projects
    """
    request_data = {"action": "get_projects"}
    return await brandwatch_controller.handle_request(request_data)

@router.get("/projects/{project_id}")
async def get_project(project_id: int):
    """
    Get specific project details
    """
    request_data = {
        "action": "get_project",
        "project_id": project_id
    }
    return await brandwatch_controller.handle_request(request_data)

@router.get("/projects/{project_id}/queries")
async def get_queries(project_id: int):
    """
    Get list of queries for a project
    """
    request_data = {
        "action": "get_queries",
        "project_id": project_id
    }
    return await brandwatch_controller.handle_request(request_data)

@router.get("/projects/{project_id}/mentions")
async def get_mentions(
    project_id: int,
    query_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = Query(default=100, le=1000)
):
    """
    Get mentions with optional filtering
    """
    request_data = {
        "action": "get_mentions",
        "project_id": project_id,
        "query_id": query_id,
        "start_date": start_date.isoformat() if start_date else None,
        "end_date": end_date.isoformat() if end_date else None,
        "limit": limit
    }
    return await brandwatch_controller.handle_request(request_data) 