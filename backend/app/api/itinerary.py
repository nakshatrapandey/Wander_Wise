"""
Itinerary Generation API Endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import uuid
from datetime import datetime

from app.models.schemas import (
    UserPreferences,
    ItineraryResponse,
    Itinerary,
    ErrorResponse
)
from app.services.itinerary_generator import ItineraryGenerator
from app.services.ml_service import MLService
from app.core.database import get_collection

router = APIRouter()


@router.post("/generate", response_model=ItineraryResponse)
async def generate_itinerary(preferences: UserPreferences):
    """
    Generate a new personalized itinerary based on user preferences
    """
    try:
        # Initialize services
        ml_service = MLService()
        itinerary_generator = ItineraryGenerator(ml_service)
        
        # Generate itinerary
        itinerary = await itinerary_generator.generate(preferences)
        
        # Save to database
        itineraries_collection = await get_collection("itineraries")
        itinerary_dict = itinerary.model_dump()
        await itineraries_collection.insert_one(itinerary_dict)
        
        # Get ML predictions for context
        ml_predictions = {
            "budget_prediction": await ml_service.predict_budget(
                destinations=itinerary.destinations,
                days=preferences.days,
                travel_style=preferences.travel_style,
                month=preferences.month,
                num_travelers=preferences.num_travelers
            )
        }
        
        return ItineraryResponse(
            success=True,
            itinerary=itinerary,
            message="Itinerary generated successfully",
            ml_predictions=ml_predictions
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{itinerary_id}", response_model=ItineraryResponse)
async def get_itinerary(itinerary_id: str):
    """
    Retrieve an existing itinerary by ID
    """
    try:
        itineraries_collection = await get_collection("itineraries")
        itinerary_data = await itineraries_collection.find_one({"itinerary_id": itinerary_id})
        
        if not itinerary_data:
            raise HTTPException(status_code=404, detail="Itinerary not found")
        
        # Remove MongoDB _id field
        itinerary_data.pop("_id", None)
        
        itinerary = Itinerary(**itinerary_data)
        
        return ItineraryResponse(
            success=True,
            itinerary=itinerary,
            message="Itinerary retrieved successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{itinerary_id}")
async def delete_itinerary(itinerary_id: str):
    """
    Delete an itinerary
    """
    try:
        itineraries_collection = await get_collection("itineraries")
        result = await itineraries_collection.delete_one({"itinerary_id": itinerary_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Itinerary not found")
        
        return {"success": True, "message": "Itinerary deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def list_itineraries(skip: int = 0, limit: int = 10):
    """
    List all itineraries with pagination
    """
    try:
        itineraries_collection = await get_collection("itineraries")
        cursor = itineraries_collection.find().skip(skip).limit(limit).sort("created_at", -1)
        
        itineraries = []
        async for doc in cursor:
            doc.pop("_id", None)
            itineraries.append(doc)
        
        return {
            "success": True,
            "itineraries": itineraries,
            "count": len(itineraries)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# .
