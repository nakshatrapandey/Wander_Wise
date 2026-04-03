"""
Booking and Payment API Endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import uuid
from datetime import datetime

from app.models.schemas import (
    BookingSummary,
    PaymentRequest,
    PaymentResponse,
    BookingConfirmation,
    Itinerary
)
from app.services.booking_service import BookingService
from app.services.payment_service import PaymentService
from app.core.database import get_collection

router = APIRouter()


@router.post("/create-summary/{itinerary_id}", response_model=BookingSummary)
async def create_booking_summary(itinerary_id: str):
    """
    Create a booking summary from finalized itinerary
    """
    try:
        # Get itinerary
        itineraries_collection = await get_collection("itineraries")
        itinerary_data = await itineraries_collection.find_one(
            {"itinerary_id": itinerary_id}
        )
        
        if not itinerary_data:
            raise HTTPException(status_code=404, detail="Itinerary not found")
        
        if not itinerary_data.get("is_finalized", False):
            raise HTTPException(
                status_code=400,
                detail="Itinerary must be finalized before booking"
            )
        
        itinerary_data.pop("_id", None)
        itinerary = Itinerary(**itinerary_data)
        
        # Create booking summary
        booking_service = BookingService()
        booking_summary = await booking_service.create_summary(itinerary)
        
        # Save to database
        bookings_collection = await get_collection("bookings")
        await bookings_collection.insert_one(booking_summary.model_dump())
        
        return booking_summary
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/payment/initiate", response_model=PaymentResponse)
async def initiate_payment(payment_request: PaymentRequest):
    """
    Initiate payment and generate QR code
    """
    try:
        # Get booking summary
        bookings_collection = await get_collection("bookings")
        booking_data = await bookings_collection.find_one(
            {"itinerary_id": payment_request.booking_summary_id}
        )
        
        if not booking_data:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        # Initialize payment service
        payment_service = PaymentService()
        
        # Create payment order
        payment_response = await payment_service.create_payment_order(
            amount=payment_request.amount,
            currency=payment_request.currency,
            booking_id=payment_request.booking_summary_id
        )
        
        return payment_response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/payment/verify/{payment_id}")
async def verify_payment(payment_id: str, signature: str):
    """
    Verify payment signature (simulated)
    """
    try:
        payment_service = PaymentService()
        is_valid = await payment_service.verify_payment(payment_id, signature)
        
        if not is_valid:
            raise HTTPException(status_code=400, detail="Invalid payment signature")
        
        return {
            "success": True,
            "message": "Payment verified successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/confirm/{booking_id}", response_model=BookingConfirmation)
async def confirm_booking(booking_id: str):
    """
    Generate final booking confirmation with PNRs and booking IDs
    """
    try:
        # Get booking summary
        bookings_collection = await get_collection("bookings")
        booking_data = await bookings_collection.find_one(
            {"itinerary_id": booking_id}
        )
        
        if not booking_data:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        booking_data.pop("_id", None)
        booking_summary = BookingSummary(**booking_data)
        
        # Generate confirmation
        booking_service = BookingService()
        confirmation = await booking_service.generate_confirmation(booking_summary)
        
        # Save confirmation
        confirmations_collection = await get_collection("confirmations")
        await confirmations_collection.insert_one(confirmation.model_dump())
        
        # Update booking status
        await bookings_collection.update_one(
            {"itinerary_id": booking_id},
            {"$set": {"payment_status": "completed"}}
        )
        
        return confirmation
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/confirmation/{booking_reference}", response_model=BookingConfirmation)
async def get_confirmation(booking_reference: str):
    """
    Retrieve booking confirmation by reference
    """
    try:
        confirmations_collection = await get_collection("confirmations")
        confirmation_data = await confirmations_collection.find_one(
            {"booking_reference": booking_reference}
        )
        
        if not confirmation_data:
            raise HTTPException(status_code=404, detail="Confirmation not found")
        
        confirmation_data.pop("_id", None)
        return BookingConfirmation(**confirmation_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# .
