"""
Destinations API Endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.models.schemas import (
    Destination,
    DestinationRecommendation,
    InterestCategory
)
from app.services.destination_service import DestinationService
from app.core.database import get_collection

router = APIRouter()


@router.get("/", response_model=List[Destination])
async def list_destinations(
    skip: int = 0,
    limit: int = 50,
    category: Optional[InterestCategory] = None
):
    """
    List all destinations with optional filtering
    """
    try:
        destinations_collection = await get_collection("destinations")
        
        query = {}
        if category:
            query["category"] = category.value
        
        cursor = destinations_collection.find(query).skip(skip).limit(limit)
        
        destinations = []
        async for doc in cursor:
            doc.pop("_id", None)
            destinations.append(Destination(**doc))
        
        return destinations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{destination_name}", response_model=Destination)
async def get_destination(destination_name: str):
    """
    Get details of a specific destination
    """
    try:
        destinations_collection = await get_collection("destinations")
        destination_data = await destinations_collection.find_one(
            {"name": destination_name}
        )
        
        if not destination_data:
            raise HTTPException(status_code=404, detail="Destination not found")
        
        destination_data.pop("_id", None)
        return Destination(**destination_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recommend", response_model=List[DestinationRecommendation])
async def recommend_destinations(
    interests: List[InterestCategory],
    budget: float,
    days: int,
    month: int,
    has_elderly: bool = False,
    has_infant: bool = False,
    limit: int = 10
):
    """
    Get personalized destination recommendations
    """
    try:
        destination_service = DestinationService()
        
        recommendations = await destination_service.recommend(
            interests=interests,
            budget=budget,
            days=days,
            month=month,
            has_elderly=has_elderly,
            has_infant=has_infant,
            limit=limit
        )
        
        return recommendations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/")
async def search_destinations(
    query: str = Query(..., min_length=2),
    limit: int = 10
):
    """
    Search destinations by name or description
    """
    try:
        destinations_collection = await get_collection("destinations")
        
        # Text search
        cursor = destinations_collection.find({
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}},
                {"state": {"$regex": query, "$options": "i"}}
            ]
        }).limit(limit)
        
        results = []
        async for doc in cursor:
            doc.pop("_id", None)
            results.append(doc)
        
        return {
            "success": True,
            "results": results,
            "count": len(results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# .
