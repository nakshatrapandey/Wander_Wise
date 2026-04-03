"""
Refinement Engine Service
Handles iterative refinement of itineraries based on natural language input
"""
import re
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime

from app.models.schemas import (
    Itinerary,
    DayPlan,
    Activity,
    BudgetBreakdown,
    TravelStyle,
    InterestCategory
)


class RefinementEngine:
    """Engine for refining itineraries based on user feedback"""
    
    def __init__(self):
        self.intent_patterns = self._initialize_intent_patterns()
    
    def _initialize_intent_patterns(self) -> Dict[str, List[str]]:
        """Initialize regex patterns for intent detection"""
        return {
            "reduce_budget": [
                r"reduce.*budget",
                r"lower.*cost",
                r"cheaper",
                r"save.*money",
                r"cut.*expenses"
            ],
            "increase_budget": [
                r"increase.*budget",
                r"more.*expensive",
                r"luxury",
                r"upgrade",
                r"premium"
            ],
            "remove_activity": [
                r"remove.*(?:activity|activities)",
                r"skip.*(?:activity|activities)",
                r"don't want.*(?:activity|activities)",
                r"exclude.*(?:activity|activities)",
                r"no.*(?:trekking|adventure|beach|shopping|cultural|spiritual|wildlife)"
            ],
            "add_activity": [
                r"add.*(?:activity|activities)",
                r"include.*(?:activity|activities)",
                r"want.*(?:more|additional)",
                r"more.*(?:trekking|adventure|beach|shopping|cultural|spiritual|wildlife)"
            ],
            "change_destination": [
                r"change.*destination",
                r"different.*place",
                r"instead of",
                r"replace.*with"
            ],
            "reduce_days": [
                r"reduce.*days",
                r"shorter.*trip",
                r"less.*days",
                r"fewer.*days"
            ],
            "increase_days": [
                r"add.*days",
                r"extend.*trip",
                r"more.*days",
                r"longer.*trip"
            ],
            "more_relaxation": [
                r"more.*relax",
                r"less.*intense",
                r"slower.*pace",
                r"easy.*going",
                r"leisure"
            ],
            "more_adventure": [
                r"more.*adventure",
                r"exciting",
                r"thrilling",
                r"active"
            ],
            "elderly_friendly": [
                r"elderly.*friendly",
                r"senior.*citizen",
                r"accessible",
                r"easy.*walk"
            ],
            "infant_friendly": [
                r"baby.*friendly",
                r"infant.*friendly",
                r"child.*friendly",
                r"kid.*friendly"
            ]
        }
    
    async def refine(
        self,
        current_itinerary: Itinerary,
        user_message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[Itinerary, List[str]]:
        """
        Refine itinerary based on user message
        Returns: (refined_itinerary, list_of_changes)
        """
        user_message_lower = user_message.lower()
        changes_made = []
        
        # Detect intents
        intents = self._detect_intents(user_message_lower)
        
        if not intents:
            # If no specific intent detected, try general modification
            changes_made.append("Applied general modifications based on your feedback")
            return current_itinerary, changes_made
        
        # Process each intent
        for intent in intents:
            if intent == "reduce_budget":
                current_itinerary, change = await self._reduce_budget(current_itinerary, user_message_lower)
                changes_made.append(change)
            
            elif intent == "increase_budget":
                current_itinerary, change = await self._increase_budget(current_itinerary, user_message_lower)
                changes_made.append(change)
            
            elif intent == "remove_activity":
                current_itinerary, change = await self._remove_activities(current_itinerary, user_message_lower)
                changes_made.append(change)
            
            elif intent == "add_activity":
                current_itinerary, change = await self._add_activities(current_itinerary, user_message_lower)
                changes_made.append(change)
            
            elif intent == "more_relaxation":
                current_itinerary, change = await self._make_more_relaxed(current_itinerary)
                changes_made.append(change)
            
            elif intent == "more_adventure":
                current_itinerary, change = await self._make_more_adventurous(current_itinerary)
                changes_made.append(change)
            
            elif intent == "elderly_friendly":
                current_itinerary, change = await self._make_elderly_friendly(current_itinerary)
                changes_made.append(change)
            
            elif intent == "infant_friendly":
                current_itinerary, change = await self._make_infant_friendly(current_itinerary)
                changes_made.append(change)
        
        # Recalculate budget breakdown
        current_itinerary.budget_breakdown = self._recalculate_budget(current_itinerary.days)
        
        # Update timestamp
        current_itinerary.updated_at = datetime.utcnow()
        
        return current_itinerary, changes_made
    
    def _detect_intents(self, message: str) -> List[str]:
        """Detect user intents from message"""
        detected_intents = []
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message, re.IGNORECASE):
                    detected_intents.append(intent)
                    break
        
        return detected_intents
    
    async def _reduce_budget(
        self,
        itinerary: Itinerary,
        message: str
    ) -> Tuple[Itinerary, str]:
        """Reduce budget by downgrading accommodations and activities"""
        reduction_percentage = 0.20  # Default 20% reduction
        
        # Try to extract percentage from message
        percentage_match = re.search(r'(\d+)\s*%', message)
        if percentage_match:
            reduction_percentage = int(percentage_match.group(1)) / 100
        
        for day in itinerary.days:
            # Reduce accommodation cost
            if day.accommodation:
                original_price = day.accommodation.get("price_per_night", 0)
                day.accommodation["price_per_night"] = original_price * (1 - reduction_percentage)
            
            # Reduce activity costs
            for activity in day.activities:
                activity.estimated_cost *= (1 - reduction_percentage)
            
            # Recalculate day total
            day.total_cost *= (1 - reduction_percentage)
        
        change = f"Reduced budget by {int(reduction_percentage * 100)}% by downgrading accommodations and activities"
        return itinerary, change
    
    async def _increase_budget(
        self,
        itinerary: Itinerary,
        message: str
    ) -> Tuple[Itinerary, str]:
        """Increase budget by upgrading accommodations and activities"""
        increase_percentage = 0.30  # Default 30% increase
        
        for day in itinerary.days:
            # Upgrade accommodation
            if day.accommodation:
                original_price = day.accommodation.get("price_per_night", 0)
                day.accommodation["price_per_night"] = original_price * (1 + increase_percentage)
                day.accommodation["room_type"] = "Deluxe Suite"
            
            # Upgrade activities
            for activity in day.activities:
                activity.estimated_cost *= (1 + increase_percentage)
                activity.description += " (Premium Experience)"
            
            # Recalculate day total
            day.total_cost *= (1 + increase_percentage)
        
        change = f"Upgraded to premium options with {int(increase_percentage * 100)}% budget increase"
        return itinerary, change
    
    async def _remove_activities(
        self,
        itinerary: Itinerary,
        message: str
    ) -> Tuple[Itinerary, str]:
        """Remove specific types of activities"""
        # Detect activity types to remove
        activity_keywords = {
            "trekking": ["trek", "hike", "climb"],
            "adventure": ["adventure", "extreme", "thrill"],
            "beach": ["beach", "water", "swim"],
            "shopping": ["shop", "market", "mall"],
            "cultural": ["cultural", "museum", "heritage"],
            "spiritual": ["temple", "spiritual", "religious"]
        }
        
        activities_to_remove = []
        for activity_type, keywords in activity_keywords.items():
            for keyword in keywords:
                if keyword in message:
                    activities_to_remove.append(activity_type)
                    break
        
        removed_count = 0
        for day in itinerary.days:
            original_activities = day.activities.copy()
            day.activities = [
                act for act in day.activities
                if not any(keyword in act.name.lower() or keyword in act.category.lower() 
                          for keyword in sum([activity_keywords.get(at, []) for at in activities_to_remove], []))
            ]
            removed_count += len(original_activities) - len(day.activities)
            
            # Recalculate day cost
            day.total_cost = sum(act.estimated_cost for act in day.activities)
            if day.accommodation:
                day.total_cost += day.accommodation.get("price_per_night", 0)
            if day.transport:
                day.total_cost += day.transport.get("price", 0)
        
        change = f"Removed {removed_count} activities matching your preferences"
        return itinerary, change
    
    async def _add_activities(
        self,
        itinerary: Itinerary,
        message: str
    ) -> Tuple[Itinerary, str]:
        """Add more activities based on user request"""
        # Detect activity type to add
        activity_types = {
            "relaxation": "Spa & Wellness",
            "adventure": "Adventure Activity",
            "cultural": "Cultural Experience",
            "food": "Food Tour",
            "shopping": "Shopping Experience"
        }
        
        activity_to_add = "Local Experience"
        for key, value in activity_types.items():
            if key in message:
                activity_to_add = value
                break
        
        added_count = 0
        for day in itinerary.days:
            if len(day.activities) < 4:  # Don't overcrowd days
                new_activity = Activity(
                    name=f"{activity_to_add} in {day.location}",
                    description=f"Additional {activity_to_add.lower()} based on your request",
                    duration="2 hours",
                    estimated_cost=500.0,
                    category=activity_to_add.lower().replace(" ", "_"),
                    is_elderly_friendly=True,
                    is_infant_friendly=True
                )
                day.activities.append(new_activity)
                day.total_cost += new_activity.estimated_cost
                added_count += 1
        
        change = f"Added {added_count} new {activity_to_add.lower()} activities"
        return itinerary, change
    
    async def _make_more_relaxed(
        self,
        itinerary: Itinerary
    ) -> Tuple[Itinerary, str]:
        """Make itinerary more relaxed by reducing activities"""
        for day in itinerary.days:
            if len(day.activities) > 2:
                # Keep only 2 activities per day
                removed = day.activities[2:]
                day.activities = day.activities[:2]
                
                # Recalculate cost
                removed_cost = sum(act.estimated_cost for act in removed)
                day.total_cost -= removed_cost
            
            # Update notes
            day.notes = "Relaxed pace with plenty of free time. " + (day.notes or "")
        
        change = "Reduced activities to 2 per day for a more relaxed pace"
        return itinerary, change
    
    async def _make_more_adventurous(
        self,
        itinerary: Itinerary
    ) -> Tuple[Itinerary, str]:
        """Make itinerary more adventurous"""
        for day in itinerary.days:
            # Add adventure activity if not present
            has_adventure = any("adventure" in act.category.lower() for act in day.activities)
            
            if not has_adventure and len(day.activities) < 4:
                adventure_activity = Activity(
                    name=f"Adventure Activity in {day.location}",
                    description="Exciting adventure experience",
                    duration="3 hours",
                    estimated_cost=1000.0,
                    category="adventure",
                    is_elderly_friendly=False,
                    is_infant_friendly=False
                )
                day.activities.append(adventure_activity)
                day.total_cost += adventure_activity.estimated_cost
        
        change = "Added adventure activities to make the trip more exciting"
        return itinerary, change
    
    async def _make_elderly_friendly(
        self,
        itinerary: Itinerary
    ) -> Tuple[Itinerary, str]:
        """Make itinerary elderly-friendly"""
        for day in itinerary.days:
            # Remove non-elderly-friendly activities
            day.activities = [
                act for act in day.activities
                if act.is_elderly_friendly
            ]
            
            # Limit to 2 activities per day
            if len(day.activities) > 2:
                day.activities = day.activities[:2]
            
            # Update notes
            day.notes = "Elderly-friendly pace with accessible locations. " + (day.notes or "")
            
            # Recalculate cost
            day.total_cost = sum(act.estimated_cost for act in day.activities)
            if day.accommodation:
                day.total_cost += day.accommodation.get("price_per_night", 0)
            if day.transport:
                day.total_cost += day.transport.get("price", 0)
        
        change = "Modified itinerary to be elderly-friendly with accessible activities"
        return itinerary, change
    
    async def _make_infant_friendly(
        self,
        itinerary: Itinerary
    ) -> Tuple[Itinerary, str]:
        """Make itinerary infant-friendly"""
        for day in itinerary.days:
            # Remove non-infant-friendly activities
            day.activities = [
                act for act in day.activities
                if act.is_infant_friendly
            ]
            
            # Limit to 2 activities per day
            if len(day.activities) > 2:
                day.activities = day.activities[:2]
            
            # Update notes
            day.notes = "Infant-friendly with short durations and child facilities. " + (day.notes or "")
            
            # Recalculate cost
            day.total_cost = sum(act.estimated_cost for act in day.activities)
            if day.accommodation:
                day.total_cost += day.accommodation.get("price_per_night", 0)
            if day.transport:
                day.total_cost += day.transport.get("price", 0)
        
        change = "Modified itinerary to be infant-friendly with suitable activities"
        return itinerary, change
    
    def _recalculate_budget(self, days: List[DayPlan]) -> BudgetBreakdown:
        """Recalculate budget breakdown after modifications"""
        accommodation = sum(
            day.accommodation.get("price_per_night", 0) if day.accommodation else 0
            for day in days
        )
        
        transport = sum(
            day.transport.get("price", 0) if day.transport else 0
            for day in days
        )
        
        activities = sum(
            sum(act.estimated_cost for act in day.activities)
            for day in days
        )
        
        food = len(days) * 800  # Estimated food cost per day
        
        total = accommodation + transport + activities + food
        miscellaneous = total * 0.05  # 5% for miscellaneous
        
        return BudgetBreakdown(
            accommodation=accommodation,
            transport=transport,
            activities=activities,
            food=food,
            miscellaneous=miscellaneous,
            total=total + miscellaneous
        )


# .
