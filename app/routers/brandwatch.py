from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from app.core.mcp_models import (
    BrandwatchQueryContent,
    BrandwatchMentionContent,
    BrandwatchProjectContent,
    BrandwatchUserContent,
    BrandwatchClientContent,
    BrandwatchMeContent,
    BrandwatchQueryModel,
    BrandwatchMentionModel,
    BrandwatchProjectModel,
    BrandwatchUserModel,
    BrandwatchClientModel,
    BrandwatchMeModel
)
from app.core.brandwatch_protocol import BrandwatchAPIProtocol
from app.core.security import oauth2_scheme

router = APIRouter()

# Dependency injection untuk model
async def get_brandwatch_user_model():
    async with BrandwatchAPIProtocol() as protocol:
        model = BrandwatchUserModel(protocol)
        yield model

async def get_brandwatch_client_model():
    async with BrandwatchAPIProtocol() as protocol:
        model = BrandwatchClientModel(protocol)
        yield model

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

async def get_brandwatch_me_model():
    async with BrandwatchAPIProtocol() as protocol:
        model = BrandwatchMeModel(protocol)
        yield model

# User Endpoints
@router.post("/users", response_model=Dict[str, Any])
async def create_user(
    content: BrandwatchUserContent,
    model: BrandwatchUserModel = Depends(get_brandwatch_user_model),
    token: str = Depends(oauth2_scheme)
):
    """Create a new Brandwatch user"""
    try:
        result = await model.create_user(content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{user_id}", response_model=Dict[str, Any])
async def get_user(
    user_id: str,
    model: BrandwatchUserModel = Depends(get_brandwatch_user_model),
    token: str = Depends(oauth2_scheme)
):
    """Get Brandwatch user details"""
    try:
        result = await model.get_user(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/users/{user_id}", response_model=Dict[str, Any])
async def update_user(
    user_id: str,
    content: BrandwatchUserContent,
    model: BrandwatchUserModel = Depends(get_brandwatch_user_model),
    token: str = Depends(oauth2_scheme)
):
    """Update Brandwatch user details"""
    try:
        result = await model.update_user(user_id, content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/users/{user_id}", response_model=Dict[str, Any])
async def delete_user(
    user_id: str,
    model: BrandwatchUserModel = Depends(get_brandwatch_user_model),
    token: str = Depends(oauth2_scheme)
):
    """Delete Brandwatch user"""
    try:
        result = await model.delete_user(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Client Endpoints
@router.post("/clients", response_model=Dict[str, Any])
async def create_client(
    content: BrandwatchClientContent,
    model: BrandwatchClientModel = Depends(get_brandwatch_client_model),
    token: str = Depends(oauth2_scheme)
):
    """Create a new Brandwatch client"""
    try:
        result = await model.create_client(content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/clients/{client_id}", response_model=Dict[str, Any])
async def get_client(
    client_id: str,
    model: BrandwatchClientModel = Depends(get_brandwatch_client_model),
    token: str = Depends(oauth2_scheme)
):
    """Get Brandwatch client details"""
    try:
        result = await model.get_client(client_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/clients/{client_id}", response_model=Dict[str, Any])
async def update_client(
    client_id: str,
    content: BrandwatchClientContent,
    model: BrandwatchClientModel = Depends(get_brandwatch_client_model),
    token: str = Depends(oauth2_scheme)
):
    """Update Brandwatch client details"""
    try:
        result = await model.update_client(client_id, content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/clients/{client_id}", response_model=Dict[str, Any])
async def delete_client(
    client_id: str,
    model: BrandwatchClientModel = Depends(get_brandwatch_client_model),
    token: str = Depends(oauth2_scheme)
):
    """Delete Brandwatch client"""
    try:
        result = await model.delete_client(client_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

# Me Endpoints
@router.get("/me", response_model=Dict[str, Any])
async def get_me(
    model: BrandwatchMeModel = Depends(get_brandwatch_me_model),
    token: str = Depends(oauth2_scheme)
):
    """Get current Brandwatch user details"""
    try:
        result = await model.get_me()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/me", response_model=Dict[str, Any])
async def update_me(
    content: BrandwatchMeContent,
    model: BrandwatchMeModel = Depends(get_brandwatch_me_model),
    token: str = Depends(oauth2_scheme)
):
    """Update current Brandwatch user details"""
    try:
        result = await model.update_me(content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 