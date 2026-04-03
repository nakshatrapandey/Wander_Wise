"""
OpenWeather Service
Handles weather data integration
"""
from typing import Dict, Any, Optional
import aiohttp
from datetime import datetime

from app.core.config import settings


class WeatherService:
    """Service for OpenWeather API integration"""
    
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    async def get_current_weather(
        self,
        city: str,
        country_code: str = "IN"
    ) -> Dict[str, Any]:
        """
        Get current weather for a city
        """
        if not self.api_key:
            return self._simulate_weather(city)
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": f"{city},{country_code}",
                "appid": self.api_key,
                "units": "metric"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_weather_data(data)
                    else:
                        print(f"Weather API returned status {response.status}")
                        return self._simulate_weather(city)
        
        except Exception as e:
            print(f"Weather API call failed: {e}")
            return self._simulate_weather(city)
    
    async def get_forecast(
        self,
        city: str,
        country_code: str = "IN",
        days: int = 5
    ) -> Dict[str, Any]:
        """
        Get weather forecast for a city
        """
        if not self.api_key:
            return self._simulate_forecast(city, days)
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": f"{city},{country_code}",
                "appid": self.api_key,
                "units": "metric",
                "cnt": days * 8  # 8 forecasts per day (3-hour intervals)
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_forecast_data(data)
                    else:
                        return self._simulate_forecast(city, days)
        
        except Exception as e:
            print(f"Forecast API call failed: {e}")
            return self._simulate_forecast(city, days)
    
    async def get_seasonal_info(
        self,
        city: str,
        month: int
    ) -> Dict[str, Any]:
        """
        Get seasonal information for travel planning
        """
        # Get current weather as baseline
        weather = await self.get_current_weather(city)
        
        # Adjust based on month
        seasonal_data = self._get_seasonal_adjustments(month)
        
        return {
            "city": city,
            "month": month,
            "avg_temperature": weather.get("temperature", 25) + seasonal_data["temp_adjustment"],
            "conditions": seasonal_data["conditions"],
            "rainfall_probability": seasonal_data["rainfall"],
            "travel_advisory": seasonal_data["advisory"],
            "best_time": seasonal_data["best_time"]
        }
    
    def _parse_weather_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse OpenWeather API response"""
        return {
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "city": data["name"]
        }
    
    def _parse_forecast_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse forecast API response"""
        forecasts = []
        
        for item in data["list"]:
            forecasts.append({
                "datetime": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "description": item["weather"][0]["description"],
                "humidity": item["main"]["humidity"]
            })
        
        return {
            "city": data["city"]["name"],
            "forecasts": forecasts
        }
    
    def _simulate_weather(self, city: str) -> Dict[str, Any]:
        """Simulate weather data for testing"""
        import random
        
        return {
            "temperature": random.randint(15, 35),
            "feels_like": random.randint(15, 35),
            "humidity": random.randint(40, 80),
            "description": random.choice(["clear sky", "few clouds", "scattered clouds", "light rain"]),
            "wind_speed": random.uniform(2.0, 10.0),
            "city": city
        }
    
    def _simulate_forecast(self, city: str, days: int) -> Dict[str, Any]:
        """Simulate forecast data for testing"""
        import random
        from datetime import timedelta
        
        forecasts = []
        base_date = datetime.utcnow()
        
        for i in range(days * 8):
            forecast_time = base_date + timedelta(hours=i * 3)
            forecasts.append({
                "datetime": forecast_time.strftime("%Y-%m-%d %H:%M:%S"),
                "temperature": random.randint(15, 35),
                "description": random.choice(["clear sky", "few clouds", "light rain"]),
                "humidity": random.randint(40, 80)
            })
        
        return {
            "city": city,
            "forecasts": forecasts
        }
    
    def _get_seasonal_adjustments(self, month: int) -> Dict[str, Any]:
        """Get seasonal adjustments based on month"""
        # Indian seasons
        if month in [12, 1, 2]:  # Winter
            return {
                "temp_adjustment": -5,
                "conditions": "Pleasant and cool",
                "rainfall": 10,
                "advisory": "Best time for travel. Carry light woolens.",
                "best_time": True
            }
        elif month in [3, 4, 5]:  # Summer
            return {
                "temp_adjustment": 5,
                "conditions": "Hot and dry",
                "rainfall": 15,
                "advisory": "Can be very hot. Stay hydrated and use sun protection.",
                "best_time": False
            }
        elif month in [6, 7, 8, 9]:  # Monsoon
            return {
                "temp_adjustment": 0,
                "conditions": "Rainy and humid",
                "rainfall": 80,
                "advisory": "Heavy rainfall expected. Carry rain gear and check for travel advisories.",
                "best_time": False
            }
        else:  # Post-monsoon (Oct, Nov)
            return {
                "temp_adjustment": -2,
                "conditions": "Pleasant and clear",
                "rainfall": 20,
                "advisory": "Excellent time for travel. Weather is pleasant.",
                "best_time": True
            }


# .
