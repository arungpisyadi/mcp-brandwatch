from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from app.core.mcp import BrandwatchContent, BrandwatchModel
from app.core.brandwatch_protocol import BrandwatchAPIProtocol
from app.core.security import oauth2_scheme

router = APIRouter()

async def get_brandwatch_model():
    async with BrandwatchAPIProtocol() as protocol:
        model = BrandwatchModel(protocol)
        yield model

@router.post("/queries", response_model=Dict[str, Any])
async def create_query(
    content: BrandwatchContent,
    model: BrandwatchModel = Depends(get_brandwatch_model),
    token: str = Depends(oauth2_scheme)
):
    """Create a new Brandwatch query"""
    try:
        result = await model.create_query(content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mentions/{query_id}", response_model=List[Dict[str, Any]])
async def get_mentions(
    query_id: str,
    model: BrandwatchModel = Depends(get_brandwatch_model),
    token: str = Depends(oauth2_scheme)
):
    """Get mentions for a specific query"""
    try:
        result = await model.get_mentions(query_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 