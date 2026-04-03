"""
Machine Learning Prediction API Endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List

from app.models.schemas import (
    BudgetPredictionRequest,
    BudgetPredictionResponse,
    TravelStyle
)
from app.services.ml_service import MLService

router = APIRouter()


@router.post("/predict-budget", response_model=BudgetPredictionResponse)
async def predict_budget(request: BudgetPredictionRequest):
    """
    Predict travel budget using ML model
    """
    try:
        ml_service = MLService()
        
        prediction = await ml_service.predict_budget(
            destinations=request.destinations,
            days=request.days,
            travel_style=request.travel_style,
            month=request.month,
            num_travelers=request.num_travelers
        )
        
        return prediction
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/model-info")
async def get_model_info():
    """
    Get information about ML models
    """
    try:
        ml_service = MLService()
        info = await ml_service.get_model_info()
        
        return {
            "success": True,
            "models": info
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/retrain")
async def retrain_models():
    """
    Retrain ML models (admin endpoint)
    """
    try:
        ml_service = MLService()
        result = await ml_service.retrain_models()
        
        return {
            "success": True,
            "message": "Models retrained successfully",
            "details": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# .
