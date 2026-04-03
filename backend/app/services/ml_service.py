"""
Machine Learning Service
Handles ML model predictions and recommendations
"""
import pickle
import os
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

from app.models.schemas import (
    TravelStyle,
    InterestCategory,
    Destination,
    DestinationRecommendation
)


class MLService:
    """Machine Learning service for recommendations and predictions"""
    
    def __init__(self):
        self.destinations_data: Optional[List[Dict]] = None
        self.budget_model = None
        self.tfidf_vectorizer = None
        self.destination_vectors = None
        self._load_data()
        self._load_models()
    
    def _load_data(self):
        """Load destinations dataset"""
        try:
            data_path = os.path.join("backend", "data", "destinations.json")
            if os.path.exists(data_path):
                import json
                with open(data_path, 'r', encoding='utf-8') as f:
                    self.destinations_data = json.load(f)
            else:
                # Use default minimal dataset if file doesn't exist
                self.destinations_data = self._get_default_destinations()
        except Exception as e:
            print(f"Warning: Could not load destinations data: {e}")
            self.destinations_data = self._get_default_destinations()
    
    def _get_default_destinations(self) -> List[Dict]:
        """Get default destinations for testing"""
        return [
            {
                "name": "Goa",
                "state": "Goa",
                "category": ["beach", "relaxation", "food"],
                "description": "Beautiful beaches and Portuguese heritage",
                "best_season": [11, 12, 1, 2],
                "avg_budget_per_day": {"budget": 2000, "moderate": 4000, "luxury": 8000},
                "elderly_friendly_score": 8.5,
                "infant_friendly_score": 7.0,
                "key_attractions": ["Baga Beach", "Fort Aguada", "Dudhsagar Falls"],
                "avg_temperature": {1: 25, 2: 26, 11: 28, 12: 27},
                "coordinates": {"lat": 15.2993, "lng": 74.1240},
                "nearby_cities": ["Mumbai", "Pune"]
            },
            {
                "name": "Manali",
                "state": "Himachal Pradesh",
                "category": ["adventure", "hill_station", "relaxation"],
                "description": "Scenic hill station with adventure activities",
                "best_season": [3, 4, 5, 6, 10, 11],
                "avg_budget_per_day": {"budget": 1800, "moderate": 3500, "luxury": 7000},
                "elderly_friendly_score": 6.0,
                "infant_friendly_score": 5.0,
                "key_attractions": ["Rohtang Pass", "Solang Valley", "Hadimba Temple"],
                "avg_temperature": {3: 10, 4: 15, 5: 20, 6: 22},
                "coordinates": {"lat": 32.2396, "lng": 77.1887},
                "nearby_cities": ["Chandigarh", "Delhi"]
            }
        ]
    
    def _load_models(self):
        """Load trained ML models"""
        try:
            model_path = os.path.join("backend", "models", "budget_model.pkl")
            if os.path.exists(model_path):
                with open(model_path, 'rb') as f:
                    self.budget_model = pickle.load(f)
        except Exception as e:
            print(f"Warning: Could not load budget model: {e}")
    
    async def get_destination_recommendations(
        self,
        interests: List[InterestCategory],
        travel_style: TravelStyle,
        month: int,
        has_elderly: bool = False,
        has_infant: bool = False,
        budget_per_day: Optional[float] = None,
        top_k: int = 5
    ) -> List[DestinationRecommendation]:
        """
        Get destination recommendations using TF-IDF and cosine similarity
        """
        if not self.destinations_data:
            return []
        
        # Create user profile text
        user_profile = " ".join([interest.value for interest in interests])
        user_profile += f" {travel_style.value}"
        
        # Create destination texts
        destination_texts = []
        valid_destinations = []
        
        for dest in self.destinations_data:
            # Filter by season
            if month not in dest.get("best_season", []):
                continue
            
            # Filter by elderly/infant friendliness
            if has_elderly and dest.get("elderly_friendly_score", 0) < 6.0:
                continue
            if has_infant and dest.get("infant_friendly_score", 0) < 6.0:
                continue
            
            # Filter by budget if provided
            if budget_per_day:
                dest_budget = dest.get("avg_budget_per_day", {}).get(travel_style.value, 0)
                if dest_budget > budget_per_day * 1.5:  # Allow 50% flexibility
                    continue
            
            # Create text representation
            dest_text = " ".join(dest.get("category", []))
            dest_text += " " + dest.get("description", "")
            dest_text += " " + " ".join(dest.get("key_attractions", []))
            
            destination_texts.append(dest_text)
            valid_destinations.append(dest)
        
        if not destination_texts:
            return []
        
        # Calculate TF-IDF and cosine similarity
        vectorizer = TfidfVectorizer(stop_words='english')
        all_texts = [user_profile] + destination_texts
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        
        # Calculate similarity scores
        user_vector = tfidf_matrix[0:1]
        dest_vectors = tfidf_matrix[1:]
        similarities = cosine_similarity(user_vector, dest_vectors)[0]
        
        # Rank destinations
        ranked_indices = np.argsort(similarities)[::-1][:top_k]
        
        recommendations = []
        for idx in ranked_indices:
            dest = valid_destinations[idx]
            score = float(similarities[idx])
            
            # Generate reason
            matching_interests = [cat for cat in dest.get("category", []) 
                                if cat in [i.value for i in interests]]
            reason = f"Matches your interests: {', '.join(matching_interests)}"
            
            if month in dest.get("best_season", []):
                reason += f". Best time to visit in month {month}"
            
            recommendations.append(DestinationRecommendation(
                destination=Destination(**dest),
                relevance_score=score,
                reason=reason
            ))
        
        return recommendations
    
    async def predict_budget(
        self,
        destinations: List[str],
        days: int,
        travel_style: TravelStyle,
        month: int,
        num_travelers: int
    ) -> Dict[str, Any]:
        """
        Predict trip budget using ML model or heuristics
        """
        # If model is loaded, use it
        if self.budget_model:
            try:
                # Prepare features (this is simplified - actual implementation would be more complex)
                features = np.array([[len(destinations), days, num_travelers]])
                predicted = self.budget_model.predict(features)[0]
                
                return {
                    "predicted_budget": float(predicted),
                    "confidence": 0.85,
                    "breakdown": self._calculate_breakdown(predicted),
                    "factors": ["destinations", "days", "travel_style", "season"]
                }
            except Exception as e:
                print(f"Model prediction failed: {e}")
        
        # Fallback to heuristic calculation
        base_budget_per_day = {
            TravelStyle.BUDGET: 1500,
            TravelStyle.MODERATE: 3500,
            TravelStyle.LUXURY: 7000,
            TravelStyle.BACKPACKER: 1000
        }
        
        daily_budget = base_budget_per_day.get(travel_style, 3000)
        
        # Adjust for number of destinations (more destinations = more transport cost)
        transport_multiplier = 1 + (len(destinations) - 1) * 0.2
        
        # Adjust for season (peak season = higher prices)
        season_multiplier = 1.2 if month in [12, 1, 4, 5, 6] else 1.0
        
        total_budget = daily_budget * days * num_travelers * transport_multiplier * season_multiplier
        
        return {
            "predicted_budget": float(total_budget),
            "confidence": 0.75,
            "breakdown": self._calculate_breakdown(total_budget),
            "factors": ["travel_style", "days", "destinations", "season", "travelers"]
        }
    
    def _calculate_breakdown(self, total_budget: float) -> Dict[str, float]:
        """Calculate budget breakdown by category"""
        return {
            "accommodation": total_budget * 0.35,
            "transport": total_budget * 0.25,
            "activities": total_budget * 0.20,
            "food": total_budget * 0.15,
            "miscellaneous": total_budget * 0.05
        }
    
    async def get_destination_by_name(self, name: str) -> Optional[Destination]:
        """Get destination details by name"""
        if not self.destinations_data:
            return None
        
        for dest in self.destinations_data:
            if dest.get("name", "").lower() == name.lower():
                return Destination(**dest)
        
        return None
    
    async def get_all_destinations(self) -> List[Destination]:
        """Get all destinations"""
        if not self.destinations_data:
            return []
        
        return [Destination(**dest) for dest in self.destinations_data]


# .
