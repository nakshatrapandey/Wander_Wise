from typing import List, Dict
import json
import os


class DestinationService:
    def __init__(self):
        # Path to dataset
        self.data_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "data",
            "destinations.json"
        )

        # Load dataset
        self.destinations = self._load_destinations()

    def _load_destinations(self) -> List[Dict]:
        """
        Load destination dataset from JSON file
        """
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ destinations.json not found, using fallback data")
            return self._fallback_data()

    def _fallback_data(self) -> List[Dict]:
        """
        Fallback dataset if JSON is missing
        """
        return [
            {
                "name": "Goa",
                "category": ["beach", "party"],
                "budget_range": "medium",
                "best_season": ["nov", "dec", "jan"],
                "elderly_friendly": 0.7,
                "infant_friendly": 0.6,
                "avg_cost_per_day": 3000
            },
            {
                "name": "Manali",
                "category": ["mountain", "adventure"],
                "budget_range": "medium",
                "best_season": ["mar", "apr", "may"],
                "elderly_friendly": 0.5,
                "infant_friendly": 0.4,
                "avg_cost_per_day": 2500
            },
            {
                "name": "Jaipur",
                "category": ["historical", "cultural"],
                "budget_range": "low",
                "best_season": ["oct", "nov", "feb"],
                "elderly_friendly": 0.9,
                "infant_friendly": 0.8,
                "avg_cost_per_day": 2000
            }
        ]

    def get_all_destinations(self) -> List[Dict]:
        return self.destinations

    def filter_destinations(
        self,
        interests: List[str],
        budget: str,
        month: str,
        elderly: bool = False,
        infant: bool = False
    ) -> List[Dict]:
        """
        Basic filtering before ML ranking
        """
        filtered = []

        for dest in self.destinations:
            # Interest match
            if not any(i in dest["category"] for i in interests):
                continue

            # Budget match
            if dest["budget_range"] != budget:
                continue

            # Season match
            if month.lower() not in dest["best_season"]:
                continue

            # Elderly/infant adjustments
            if elderly and dest["elderly_friendly"] < 0.6:
                continue

            if infant and dest["infant_friendly"] < 0.6:
                continue

            filtered.append(dest)

        return filtered

    def estimate_budget(
        self,
        destination: Dict,
        days: int
    ) -> Dict:
        """
        Estimate total trip cost
        """
        base_cost = destination["avg_cost_per_day"] * days

        return {
            "destination": destination["name"],
            "days": days,
            "estimated_cost": base_cost,
            "breakdown": {
                "stay": int(base_cost * 0.4),
                "travel": int(base_cost * 0.3),
                "activities": int(base_cost * 0.2),
                "misc": int(base_cost * 0.1),
            }
        }
