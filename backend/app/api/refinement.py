"""
Itinerary Refinement API Endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.models.schemas import (
    RefinementRequest,
    RefinementResponse,
    Itinerary
)
from app.services.refinement_engine import RefinementEngine
from app.core.database import get_collection

router = APIRouter()


@router.post("/refine", response_model=RefinementResponse)
async def refine_itinerary(request: RefinementRequest):
    """
    Refine an existing itinerary based on natural language input
    """
    try:
        # Get existing itinerary
        itineraries_collection = await get_collection("itineraries")
        itinerary_data = await itineraries_collection.find_one(
            {"itinerary_id": request.itinerary_id}
        )
        
        if not itinerary_data:
            raise HTTPException(status_code=404, detail="Itinerary not found")
        
        # Remove MongoDB _id
        itinerary_data.pop("_id", None)
        current_itinerary = Itinerary(**itinerary_data)
        
        # Initialize refinement engine
        refinement_engine = RefinementEngine()
        
        # Process refinement
        refined_itinerary, changes = await refinement_engine.refine(
            current_itinerary=current_itinerary,
            user_message=request.user_message,
            context=request.context
        )
        
        # Update version and timestamp
        refined_itinerary.version += 1
        refined_itinerary.updated_at = datetime.utcnow()
        
        # Save updated itinerary
        await itineraries_collection.update_one(
            {"itinerary_id": request.itinerary_id},
            {"$set": refined_itinerary.model_dump()}
        )
        
        return RefinementResponse(
            success=True,
            itinerary=refined_itinerary,
            changes_made=changes,
            message="Itinerary refined successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/finalize/{itinerary_id}")
async def finalize_itinerary(itinerary_id: str):
    """
    Mark an itinerary as finalized (no more changes)
    """
    try:
        itineraries_collection = await get_collection("itineraries")
        
        result = await itineraries_collection.update_one(
            {"itinerary_id": itinerary_id},
            {"$set": {"is_finalized": True}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Itinerary not found")
        
        return {
            "success": True,
            "message": "Itinerary finalized successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from datetime import datetime

# .
