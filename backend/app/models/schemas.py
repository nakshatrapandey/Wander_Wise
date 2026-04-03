"""
Pydantic Schemas for Request/Response Models
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class TravelStyle(str, Enum):
    """Travel style options"""
    BUDGET = "budget"
    MODERATE = "moderate"
    LUXURY = "luxury"
    BACKPACKER = "backpacker"


class InterestCategory(str, Enum):
    """Interest categories"""
    ADVENTURE = "adventure"
    BEACH = "beach"
    CULTURAL = "cultural"
    SPIRITUAL = "spiritual"
    WILDLIFE = "wildlife"
    HILL_STATION = "hill_station"
    HISTORICAL = "historical"
    FOOD = "food"
    SHOPPING = "shopping"
    RELAXATION = "relaxation"


class TravelerType(str, Enum):
    """Special traveler types"""
    ELDERLY = "elderly"
    INFANT = "infant"
    NONE = "none"


# ============= User Input Models =============

class UserPreferences(BaseModel):
    """User travel preferences input"""
    budget: float = Field(..., description="Total budget in INR", gt=0)
    days: int = Field(..., description="Number of days", ge=1, le=30)
    starting_city: str = Field(..., description="Starting city")
    interests: List[InterestCategory] = Field(..., description="List of interests")
    travel_style: TravelStyle = Field(..., description="Travel style")
    month: int = Field(..., description="Month of travel (1-12)", ge=1, le=12)
    num_travelers: int = Field(default=1, description="Number of travelers", ge=1)
    has_elderly: bool = Field(default=False, description="Traveling with elderly")
    has_infant: bool = Field(default=False, description="Traveling with infant")
    additional_preferences: Optional[str] = Field(default=None, description="Additional preferences")


# ============= Itinerary Models =============

class Activity(BaseModel):
    """Single activity in itinerary"""
    name: str
    description: str
    duration: str
    estimated_cost: float
    category: str
    location: Optional[Dict[str, float]] = None  # lat, lng
    is_elderly_friendly: bool = True
    is_infant_friendly: bool = True


class DayPlan(BaseModel):
    """Single day plan"""
    day: int
    date: Optional[str] = None
    location: str
    activities: List[Activity]
    accommodation: Optional[Dict[str, Any]] = None
    meals: List[Dict[str, Any]] = []
    transport: Optional[Dict[str, Any]] = None
    total_cost: float
    notes: Optional[str] = None


class BudgetBreakdown(BaseModel):
    """Budget breakdown"""
    accommodation: float
    transport: float
    activities: float
    food: float
    miscellaneous: float
    total: float


class Itinerary(BaseModel):
    """Complete itinerary"""
    itinerary_id: str
    user_id: Optional[str] = None
    destinations: List[str]
    days: List[DayPlan]
    budget_breakdown: BudgetBreakdown
    total_distance: Optional[float] = None
    optimized_route: Optional[List[str]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    version: int = 1
    is_finalized: bool = False


class ItineraryResponse(BaseModel):
    """Itinerary response"""
    success: bool
    itinerary: Itinerary
    message: str = "Itinerary generated successfully"
    ml_predictions: Optional[Dict[str, Any]] = None


# ============= Refinement Models =============

class RefinementRequest(BaseModel):
    """Request to refine itinerary"""
    itinerary_id: str
    user_message: str = Field(..., description="Natural language refinement request")
    context: Optional[Dict[str, Any]] = None


class RefinementResponse(BaseModel):
    """Response after refinement"""
    success: bool
    itinerary: Itinerary
    changes_made: List[str]
    message: str


# ============= Destination Models =============

class Destination(BaseModel):
    """Destination information"""
    name: str
    state: str
    category: List[InterestCategory]
    description: str
    best_season: List[int]  # months
    avg_budget_per_day: Dict[str, float]  # by travel style
    elderly_friendly_score: float = Field(ge=0, le=10)
    infant_friendly_score: float = Field(ge=0, le=10)
    key_attractions: List[str]
    avg_temperature: Dict[int, float]  # month: temp
    coordinates: Dict[str, float]  # lat, lng
    nearby_cities: List[str]


class DestinationRecommendation(BaseModel):
    """Recommended destination with score"""
    destination: Destination
    relevance_score: float
    reason: str


# ============= Booking Models =============

class FlightBooking(BaseModel):
    """Flight booking details"""
    flight_number: str
    airline: str
    departure: str
    arrival: str
    departure_time: str
    arrival_time: str
    price: float
    pnr: Optional[str] = None


class HotelBooking(BaseModel):
    """Hotel booking details"""
    hotel_name: str
    location: str
    check_in: str
    check_out: str
    room_type: str
    price_per_night: float
    total_nights: int
    total_price: float
    booking_id: Optional[str] = None


class TransportBooking(BaseModel):
    """Transport booking details"""
    type: str  # train, bus, rental
    from_location: str
    to_location: str
    date: str
    price: float
    booking_id: Optional[str] = None


class BookingSummary(BaseModel):
    """Complete booking summary"""
    itinerary_id: str
    flights: List[FlightBooking] = []
    hotels: List[HotelBooking] = []
    transports: List[TransportBooking] = []
    activities_cost: float
    total_cost: float
    payment_status: str = "pending"
    booking_reference: Optional[str] = None


class PaymentRequest(BaseModel):
    """Payment request"""
    booking_summary_id: str
    amount: float
    currency: str = "INR"


class PaymentResponse(BaseModel):
    """Payment response with QR"""
    success: bool
    qr_code_url: str
    payment_id: str
    order_id: str
    amount: float
    currency: str


class BookingConfirmation(BaseModel):
    """Final booking confirmation"""
    booking_reference: str
    itinerary_id: str
    confirmations: Dict[str, List[str]]  # type: [confirmation_ids]
    total_paid: float
    booking_date: datetime
    status: str


# ============= ML Models =============

class BudgetPredictionRequest(BaseModel):
    """Budget prediction request"""
    destinations: List[str]
    days: int
    travel_style: TravelStyle
    month: int
    num_travelers: int


class BudgetPredictionResponse(BaseModel):
    """Budget prediction response"""
    predicted_budget: float
    confidence: float
    breakdown: Dict[str, float]
    factors: List[str]


# ============= Error Models =============

class ErrorResponse(BaseModel):
    """Error response"""
    success: bool = False
    error: str
    details: Optional[Dict[str, Any]] = None

# .
