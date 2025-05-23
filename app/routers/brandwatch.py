from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from app.core.mcp_models import (
    BrandwatchQueryContent,
    BrandwatchMentionContent,
    BrandwatchProjectContent,
    BrandwatchQueryModel,
    BrandwatchMentionModel,
    BrandwatchProjectModel
)
from app.core.brandwatch_protocol import BrandwatchAPIProtocol
from app.core.security import oauth2_scheme

router = APIRouter()

async def get_brandwatch_query_model():
    async with BrandwatchAPIProtocol() as protocol:
        model = BrandwatchQueryModel(protocol)
        yield model

async def get_brandwatch_mention_model():
    async with BrandwatchAPIProtocol() as protocol:
        model = BrandwatchMentionModel(protocol)
        yield model

async def get_brandwatch_project_model():
    async with BrandwatchAPIProtocol() as protocol:
        model = BrandwatchProjectModel(protocol)
        yield model

# Query Endpoints
@router.post("/queries", response_model=Dict[str, Any])
async def create_query(
    content: BrandwatchQueryContent,
    model: BrandwatchQueryModel = Depends(get_brandwatch_query_model),
    token: str = Depends(oauth2_scheme)
):
    """Create a new Brandwatch query"""
    try:
        # Validate query first
        await model.validate_query(content)
        # Create query if validation passes
        result = await model.create_query(content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/queries/validate", response_model=Dict[str, Any])
async def validate_query(
    content: BrandwatchQueryContent,
    model: BrandwatchQueryModel = Depends(get_brandwatch_query_model),
    token: str = Depends(oauth2_scheme)
):
    """Validate a Brandwatch query"""
    try:
        result = await model.validate_query(content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mention Endpoints
@router.get("/mentions", response_model=List[Dict[str, Any]])
async def get_mentions(
    content: BrandwatchMentionContent,
    model: BrandwatchMentionModel = Depends(get_brandwatch_mention_model),
    token: str = Depends(oauth2_scheme)
):
    """Get mentions for a specific query"""
    try:
        result = await model.get_mentions(content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Project Endpoints
@router.post("/projects", response_model=Dict[str, Any])
async def create_project(
    content: BrandwatchProjectContent,
    model: BrandwatchProjectModel = Depends(get_brandwatch_project_model),
    token: str = Depends(oauth2_scheme)
):
    """Create a new Brandwatch project"""
    try:
        result = await model.create_project(content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projects", response_model=List[Dict[str, Any]])
async def get_projects(
    model: BrandwatchProjectModel = Depends(get_brandwatch_project_model),
    token: str = Depends(oauth2_scheme)
):
    """Get all Brandwatch projects"""
    try:
        result = await model.get_projects()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 