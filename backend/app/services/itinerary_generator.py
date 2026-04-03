"""
Itinerary Generation Service
Generates personalized day-wise travel itineraries
"""
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import random

from app.models.schemas import (
    UserPreferences,
    Itinerary,
    DayPlan,
    Activity,
    BudgetBreakdown,
    TravelStyle,
    InterestCategory
)
from app.services.ml_service import MLService


class ItineraryGenerator:
    """Service for generating personalized itineraries"""
    
    def __init__(self, ml_service: MLService):
        self.ml_service = ml_service
    
    async def generate(self, preferences: UserPreferences) -> Itinerary:
        """
        Generate complete itinerary based on user preferences
        """
        # Get destination recommendations
        budget_per_day = preferences.budget / preferences.days
        
        recommendations = await self.ml_service.get_destination_recommendations(
            interests=preferences.interests,
            travel_style=preferences.travel_style,
            month=preferences.month,
            has_elderly=preferences.has_elderly,
            has_infant=preferences.has_infant,
            budget_per_day=budget_per_day,
            top_k=min(5, preferences.days)  # Max destinations = days
        )
        
        if not recommendations:
            # Fallback to default destinations
            recommendations = await self._get_fallback_destinations(preferences)
        
        # Select destinations based on days
        selected_destinations = self._select_destinations(
            recommendations,
            preferences.days
        )
        
        # Generate day-wise plans
        days = await self._generate_day_plans(
            destinations=selected_destinations,
            preferences=preferences
        )
        
        # Calculate budget breakdown
        budget_breakdown = self._calculate_budget_breakdown(
            days=days,
            total_budget=preferences.budget
        )
        
        # Create itinerary
        itinerary = Itinerary(
            itinerary_id=str(uuid.uuid4()),
            destinations=[dest.destination.name for dest in selected_destinations],
            days=days,
            budget_breakdown=budget_breakdown,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1,
            is_finalized=False
        )
        
        return itinerary
    
    def _select_destinations(
        self,
        recommendations: List,
        num_days: int
    ) -> List:
        """
        Select optimal number of destinations based on trip duration
        """
        if num_days <= 3:
            return recommendations[:1]
        elif num_days <= 7:
            return recommendations[:2]
        elif num_days <= 14:
            return recommendations[:3]
        else:
            return recommendations[:4]
    
    async def _generate_day_plans(
        self,
        destinations: List,
        preferences: UserPreferences
    ) -> List[DayPlan]:
        """
        Generate day-wise plans for the trip
        """
        days = []
        days_per_destination = preferences.days // len(destinations) if destinations else preferences.days
        remaining_days = preferences.days % len(destinations) if destinations else 0
        
        current_day = 1
        
        for idx, dest_rec in enumerate(destinations):
            destination = dest_rec.destination
            
            # Calculate days for this destination
            dest_days = days_per_destination
            if idx < remaining_days:
                dest_days += 1
            
            # Generate activities for each day at this destination
            for day_num in range(dest_days):
                activities = await self._generate_activities(
                    destination=destination,
                    preferences=preferences,
                    day_number=day_num + 1,
                    total_days_at_dest=dest_days
                )
                
                # Generate accommodation
                accommodation = self._generate_accommodation(
                    destination=destination,
                    travel_style=preferences.travel_style
                )
                
                # Generate transport (for first day at destination)
                transport = None
                if day_num == 0 and current_day > 1:
                    transport = self._generate_transport(
                        from_dest=destinations[idx-1].destination.name if idx > 0 else preferences.starting_city,
                        to_dest=destination.name,
                        travel_style=preferences.travel_style
                    )
                
                # Calculate day cost
                activities_cost = sum(act.estimated_cost for act in activities)
                accommodation_cost = accommodation.get("price_per_night", 0)
                transport_cost = transport.get("price", 0) if transport else 0
                meals_cost = self._calculate_meals_cost(preferences.travel_style)
                
                total_cost = activities_cost + accommodation_cost + transport_cost + meals_cost
                
                day_plan = DayPlan(
                    day=current_day,
                    location=destination.name,
                    activities=activities,
                    accommodation=accommodation,
                    meals=self._generate_meals(),
                    transport=transport,
                    total_cost=total_cost,
                    notes=self._generate_day_notes(preferences, destination)
                )
                
                days.append(day_plan)
                current_day += 1
        
        return days
    
    async def _generate_activities(
        self,
        destination: Any,
        preferences: UserPreferences,
        day_number: int,
        total_days_at_dest: int
    ) -> List[Activity]:
        """
        Generate activities for a day based on destination and preferences
        """
        activities = []
        
        # Get key attractions
        attractions = destination.key_attractions[:5]
        
        # Determine number of activities based on traveler type
        if preferences.has_elderly or preferences.has_infant:
            num_activities = 2  # Fewer activities for comfort
        else:
            num_activities = 3
        
        # Select activities based on interests
        for i in range(min(num_activities, len(attractions))):
            attraction = attractions[i] if i < len(attractions) else f"Local Experience {i+1}"
            
            # Determine activity category
            category = self._match_activity_category(
                destination.category,
                preferences.interests
            )
            
            # Adjust for elderly/infant
            is_elderly_friendly = True
            is_infant_friendly = True
            
            if preferences.has_elderly:
                is_elderly_friendly = destination.elderly_friendly_score >= 6.0
            
            if preferences.has_infant:
                is_infant_friendly = destination.infant_friendly_score >= 6.0
            
            # Calculate cost based on travel style
            base_cost = self._get_activity_base_cost(category, preferences.travel_style)
            cost = base_cost * preferences.num_travelers
            
            activity = Activity(
                name=attraction,
                description=f"Explore {attraction} - {category}",
                duration="2-3 hours",
                estimated_cost=cost,
                category=category,
                location=destination.coordinates,
                is_elderly_friendly=is_elderly_friendly,
                is_infant_friendly=is_infant_friendly
            )
            
            activities.append(activity)
        
        return activities
    
    def _match_activity_category(
        self,
        dest_categories: List[str],
        user_interests: List[InterestCategory]
    ) -> str:
        """Match destination category with user interests"""
        user_interest_values = [interest.value for interest in user_interests]
        
        for cat in dest_categories:
            if cat in user_interest_values:
                return cat
        
        return dest_categories[0] if dest_categories else "sightseeing"
    
    def _get_activity_base_cost(self, category: str, travel_style: TravelStyle) -> float:
        """Get base cost for activity based on category and travel style"""
        base_costs = {
            "adventure": {"budget": 500, "moderate": 1000, "luxury": 2000, "backpacker": 300},
            "beach": {"budget": 200, "moderate": 500, "luxury": 1000, "backpacker": 100},
            "cultural": {"budget": 300, "moderate": 600, "luxury": 1200, "backpacker": 200},
            "spiritual": {"budget": 100, "moderate": 300, "luxury": 600, "backpacker": 50},
            "wildlife": {"budget": 800, "moderate": 1500, "luxury": 3000, "backpacker": 500},
            "sightseeing": {"budget": 200, "moderate": 400, "luxury": 800, "backpacker": 150}
        }
        
        category_costs = base_costs.get(category, base_costs["sightseeing"])
        return category_costs.get(travel_style.value, 400)
    
    def _generate_accommodation(
        self,
        destination: Any,
        travel_style: TravelStyle
    ) -> Dict[str, Any]:
        """Generate accommodation details"""
        hotel_types = {
            TravelStyle.BUDGET: "Budget Hotel",
            TravelStyle.MODERATE: "3-Star Hotel",
            TravelStyle.LUXURY: "5-Star Resort",
            TravelStyle.BACKPACKER: "Hostel"
        }
        
        base_prices = {
            TravelStyle.BUDGET: 1000,
            TravelStyle.MODERATE: 2500,
            TravelStyle.LUXURY: 8000,
            TravelStyle.BACKPACKER: 500
        }
        
        return {
            "hotel_name": f"{hotel_types[travel_style]} in {destination.name}",
            "location": destination.name,
            "room_type": "Standard Room" if travel_style != TravelStyle.LUXURY else "Deluxe Suite",
            "price_per_night": base_prices[travel_style],
            "amenities": ["WiFi", "Breakfast", "AC"],
            "rating": 4.0 if travel_style in [TravelStyle.MODERATE, TravelStyle.LUXURY] else 3.5
        }
    
    def _generate_transport(
        self,
        from_dest: str,
        to_dest: str,
        travel_style: TravelStyle
    ) -> Dict[str, Any]:
        """Generate transport details"""
        transport_modes = {
            TravelStyle.BUDGET: "Train",
            TravelStyle.MODERATE: "Flight",
            TravelStyle.LUXURY: "Flight",
            TravelStyle.BACKPACKER: "Bus"
        }
        
        base_prices = {
            TravelStyle.BUDGET: 800,
            TravelStyle.MODERATE: 3000,
            TravelStyle.LUXURY: 5000,
            TravelStyle.BACKPACKER: 500
        }
        
        return {
            "mode": transport_modes[travel_style],
            "from": from_dest,
            "to": to_dest,
            "price": base_prices[travel_style],
            "duration": "2-4 hours",
            "booking_required": True
        }
    
    def _calculate_meals_cost(self, travel_style: TravelStyle) -> float:
        """Calculate daily meals cost"""
        meal_costs = {
            TravelStyle.BUDGET: 500,
            TravelStyle.MODERATE: 1000,
            TravelStyle.LUXURY: 2500,
            TravelStyle.BACKPACKER: 300
        }
        return meal_costs.get(travel_style, 800)
    
    def _generate_meals(self) -> List[Dict[str, Any]]:
        """Generate meal suggestions"""
        return [
            {"type": "breakfast", "suggestion": "Local breakfast at hotel"},
            {"type": "lunch", "suggestion": "Try local cuisine"},
            {"type": "dinner", "suggestion": "Recommended restaurant"}
        ]
    
    def _generate_day_notes(
        self,
        preferences: UserPreferences,
        destination: Any
    ) -> str:
        """Generate helpful notes for the day"""
        notes = []
        
        if preferences.has_elderly:
            notes.append("Take frequent breaks. Avoid strenuous activities.")
        
        if preferences.has_infant:
            notes.append("Carry baby essentials. Look for child-friendly facilities.")
        
        if destination.elderly_friendly_score < 7.0 and preferences.has_elderly:
            notes.append("This destination may have limited accessibility.")
        
        return " ".join(notes) if notes else "Enjoy your day!"
    
    def _calculate_budget_breakdown(
        self,
        days: List[DayPlan],
        total_budget: float
    ) -> BudgetBreakdown:
        """Calculate budget breakdown from day plans"""
        accommodation = sum(
            day.accommodation.get("price_per_night", 0) if day.accommodation else 0 for day in days
        )
        
        transport = sum(
            day.transport.get("price", 0) if day.transport else 0 for day in days
        )
        
        activities = sum(
            sum(act.estimated_cost for act in day.activities) for day in days
        )
        
        food = sum(
            self._calculate_meals_cost(TravelStyle.MODERATE) for day in days
        )
        
        calculated_total = accommodation + transport + activities + food
        miscellaneous = max(0, total_budget - calculated_total)
        
        return BudgetBreakdown(
            accommodation=accommodation,
            transport=transport,
            activities=activities,
            food=food,
            miscellaneous=miscellaneous,
            total=total_budget
        )
    
    async def _get_fallback_destinations(self, preferences: UserPreferences):
        """Get fallback destinations if recommendations fail"""
        all_destinations = await self.ml_service.get_all_destinations()
        
        if not all_destinations:
            return []
        
        # Simple filtering
        filtered = [
            dest for dest in all_destinations
            if preferences.month in dest.best_season
        ]
        
        return filtered[:3] if filtered else all_destinations[:3]


# .
