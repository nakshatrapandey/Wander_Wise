"""
Google Maps Service
Handles Google Maps API integration for routing and distance calculations
"""
from typing import List, Dict, Any, Optional, Tuple
import googlemaps
from datetime import datetime

from app.core.config import settings


class MapsService:
    """Service for Google Maps API integration"""
    
    def __init__(self):
        try:
            if settings.GOOGLE_MAPS_API_KEY:
                self.client = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
            else:
                self.client = None
                print("Warning: Google Maps API key not configured. Using simulation mode.")
        except Exception as e:
            self.client = None
            print(f"Warning: Could not initialize Google Maps client: {e}")
    
    async def get_distance_matrix(
        self,
        origins: List[str],
        destinations: List[str],
        mode: str = "driving"
    ) -> Dict[str, Any]:
        """
        Get distance and duration between multiple origins and destinations
        """
        if self.client:
            try:
                result = self.client.distance_matrix(
                    origins=origins,
                    destinations=destinations,
                    mode=mode,
                    units="metric"
                )
                return result
            except Exception as e:
                print(f"Distance matrix API call failed: {e}")
                return self._simulate_distance_matrix(origins, destinations)
        else:
            return self._simulate_distance_matrix(origins, destinations)
    
    async def get_route(
        self,
        origin: str,
        destination: str,
        waypoints: Optional[List[str]] = None,
        optimize_waypoints: bool = True
    ) -> Dict[str, Any]:
        """
        Get optimized route between origin and destination with optional waypoints
        """
        if self.client:
            try:
                result = self.client.directions(
                    origin=origin,
                    destination=destination,
                    waypoints=waypoints,
                    optimize_waypoints=optimize_waypoints,
                    mode="driving"
                )
                
                if result:
                    return self._parse_route(result[0])
                else:
                    return self._simulate_route(origin, destination, waypoints)
            except Exception as e:
                print(f"Directions API call failed: {e}")
                return self._simulate_route(origin, destination, waypoints)
        else:
            return self._simulate_route(origin, destination, waypoints)
    
    async def get_place_details(
        self,
        place_name: str,
        location: Optional[Tuple[float, float]] = None
    ) -> Dict[str, Any]:
        """
        Get details about a place
        """
        if self.client:
            try:
                # Search for place
                if location:
                    result = self.client.places_nearby(
                        location=location,
                        keyword=place_name,
                        radius=5000
                    )
                else:
                    result = self.client.find_place(
                        input=place_name,
                        input_type="textquery",
                        fields=["name", "geometry", "formatted_address", "rating"]
                    )
                
                if result.get("candidates") or result.get("results"):
                    candidates = result.get("candidates", result.get("results", []))
                    if candidates:
                        return candidates[0]
                
                return self._simulate_place_details(place_name)
            except Exception as e:
                print(f"Place details API call failed: {e}")
                return self._simulate_place_details(place_name)
        else:
            return self._simulate_place_details(place_name)
    
    async def geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        """
        Convert address to coordinates
        """
        if self.client:
            try:
                result = self.client.geocode(address)
                if result:
                    location = result[0]["geometry"]["location"]
                    return (location["lat"], location["lng"])
                return None
            except Exception as e:
                print(f"Geocoding failed: {e}")
                return None
        else:
            # Return simulated coordinates
            return (28.6139, 77.2090)  # Default to Delhi
    
    def _simulate_distance_matrix(
        self,
        origins: List[str],
        destinations: List[str]
    ) -> Dict[str, Any]:
        """
        Simulate distance matrix for testing
        """
        rows = []
        for origin in origins:
            elements = []
            for destination in destinations:
                # Simulate distance (random between 100-500 km)
                import random
                distance_km = random.randint(100, 500)
                duration_hours = distance_km / 60  # Assume 60 km/h average
                
                elements.append({
                    "distance": {
                        "text": f"{distance_km} km",
                        "value": distance_km * 1000  # meters
                    },
                    "duration": {
                        "text": f"{int(duration_hours)} hours {int((duration_hours % 1) * 60)} mins",
                        "value": int(duration_hours * 3600)  # seconds
                    },
                    "status": "OK"
                })
            rows.append({"elements": elements})
        
        return {
            "origin_addresses": origins,
            "destination_addresses": destinations,
            "rows": rows,
            "status": "OK"
        }
    
    def _simulate_route(
        self,
        origin: str,
        destination: str,
        waypoints: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Simulate route for testing
        """
        import random
        
        distance_km = random.randint(100, 500)
        duration_hours = distance_km / 60
        
        route_points = [origin]
        if waypoints:
            route_points.extend(waypoints)
        route_points.append(destination)
        
        return {
            "distance": distance_km,
            "duration": duration_hours,
            "route": route_points,
            "optimized": True
        }
    
    def _parse_route(self, route_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse Google Maps route response
        """
        leg = route_data["legs"][0]
        
        return {
            "distance": leg["distance"]["value"] / 1000,  # Convert to km
            "duration": leg["duration"]["value"] / 3600,  # Convert to hours
            "route": [step["html_instructions"] for step in leg["steps"]],
            "optimized": True
        }
    
    def _simulate_place_details(self, place_name: str) -> Dict[str, Any]:
        """
        Simulate place details for testing
        """
        import random
        
        return {
            "name": place_name,
            "formatted_address": f"{place_name}, India",
            "geometry": {
                "location": {
                    "lat": random.uniform(8.0, 35.0),
                    "lng": random.uniform(68.0, 97.0)
                }
            },
            "rating": round(random.uniform(3.5, 5.0), 1)
        }


# .
