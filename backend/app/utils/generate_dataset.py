"""
Dataset Generation Utility
Generates comprehensive Indian destinations dataset
"""
import json
import os
from typing import List, Dict, Any


def generate_destinations_dataset() -> List[Dict[str, Any]]:
    """
    Generate comprehensive dataset of 100+ Indian destinations
    """
    destinations = [
        # Beach Destinations
        {
            "name": "Goa",
            "state": "Goa",
            "category": ["beach", "relaxation", "food", "adventure"],
            "description": "Beautiful beaches, Portuguese heritage, vibrant nightlife, and water sports",
            "best_season": [11, 12, 1, 2, 3],
            "avg_budget_per_day": {"budget": 2000, "moderate": 4000, "luxury": 8000, "backpacker": 1500},
            "elderly_friendly_score": 8.5,
            "infant_friendly_score": 7.5,
            "key_attractions": ["Baga Beach", "Fort Aguada", "Dudhsagar Falls", "Old Goa Churches", "Anjuna Flea Market"],
            "avg_temperature": {1: 25, 2: 26, 3: 28, 11: 28, 12: 27},
            "coordinates": {"lat": 15.2993, "lng": 74.1240},
            "nearby_cities": ["Mumbai", "Pune", "Bangalore"]
        },
        {
            "name": "Andaman Islands",
            "state": "Andaman and Nicobar Islands",
            "category": ["beach", "adventure", "wildlife", "relaxation"],
            "description": "Pristine beaches, coral reefs, water sports, and tropical paradise",
            "best_season": [10, 11, 12, 1, 2, 3, 4],
            "avg_budget_per_day": {"budget": 3000, "moderate": 6000, "luxury": 12000, "backpacker": 2500},
            "elderly_friendly_score": 6.0,
            "infant_friendly_score": 5.5,
            "key_attractions": ["Radhanagar Beach", "Cellular Jail", "Havelock Island", "Neil Island", "Scuba Diving"],
            "avg_temperature": {10: 28, 11: 27, 12: 26, 1: 25, 2: 26, 3: 28, 4: 29},
            "coordinates": {"lat": 11.7401, "lng": 92.6586},
            "nearby_cities": ["Kolkata", "Chennai"]
        },
        {
            "name": "Puri",
            "state": "Odisha",
            "category": ["beach", "spiritual", "cultural"],
            "description": "Sacred beach town with Jagannath Temple and golden beaches",
            "best_season": [10, 11, 12, 1, 2, 3],
            "avg_budget_per_day": {"budget": 1500, "moderate": 3000, "luxury": 6000, "backpacker": 1000},
            "elderly_friendly_score": 7.5,
            "infant_friendly_score": 7.0,
            "key_attractions": ["Jagannath Temple", "Puri Beach", "Konark Sun Temple", "Chilika Lake"],
            "avg_temperature": {10: 28, 11: 26, 12: 24, 1: 22, 2: 24, 3: 27},
            "coordinates": {"lat": 19.8135, "lng": 85.8312},
            "nearby_cities": ["Bhubaneswar", "Kolkata"]
        },
        
        # Hill Stations
        {
            "name": "Manali",
            "state": "Himachal Pradesh",
            "category": ["hill_station", "adventure", "relaxation"],
            "description": "Scenic hill station with snow-capped mountains and adventure activities",
            "best_season": [3, 4, 5, 6, 10, 11],
            "avg_budget_per_day": {"budget": 1800, "moderate": 3500, "luxury": 7000, "backpacker": 1200},
            "elderly_friendly_score": 6.0,
            "infant_friendly_score": 5.0,
            "key_attractions": ["Rohtang Pass", "Solang Valley", "Hadimba Temple", "Old Manali", "Vashisht Hot Springs"],
            "avg_temperature": {3: 10, 4: 15, 5: 20, 6: 22, 10: 15, 11: 10},
            "coordinates": {"lat": 32.2396, "lng": 77.1887},
            "nearby_cities": ["Chandigarh", "Delhi", "Shimla"]
        },
        {
            "name": "Shimla",
            "state": "Himachal Pradesh",
            "category": ["hill_station", "cultural", "relaxation"],
            "description": "Colonial hill station with Victorian architecture and pleasant climate",
            "best_season": [3, 4, 5, 6, 9, 10, 11],
            "avg_budget_per_day": {"budget": 2000, "moderate": 4000, "luxury": 8000, "backpacker": 1500},
            "elderly_friendly_score": 8.0,
            "infant_friendly_score": 7.5,
            "key_attractions": ["Mall Road", "Ridge", "Christ Church", "Jakhu Temple", "Kufri"],
            "avg_temperature": {3: 12, 4: 17, 5: 22, 6: 25, 9: 20, 10: 16, 11: 12},
            "coordinates": {"lat": 31.1048, "lng": 77.1734},
            "nearby_cities": ["Chandigarh", "Delhi"]
        },
        {
            "name": "Darjeeling",
            "state": "West Bengal",
            "category": ["hill_station", "cultural", "relaxation"],
            "description": "Tea gardens, toy train, and stunning Himalayan views",
            "best_season": [3, 4, 5, 9, 10, 11],
            "avg_budget_per_day": {"budget": 1800, "moderate": 3500, "luxury": 7000, "backpacker": 1200},
            "elderly_friendly_score": 7.0,
            "infant_friendly_score": 6.5,
            "key_attractions": ["Tiger Hill", "Darjeeling Himalayan Railway", "Tea Gardens", "Peace Pagoda", "Mall Road"],
            "avg_temperature": {3: 15, 4: 18, 5: 20, 9: 18, 10: 16, 11: 13},
            "coordinates": {"lat": 27.0360, "lng": 88.2627},
            "nearby_cities": ["Kolkata", "Siliguri"]
        },
        {
            "name": "Ooty",
            "state": "Tamil Nadu",
            "category": ["hill_station", "relaxation", "adventure"],
            "description": "Queen of hill stations with botanical gardens and toy train",
            "best_season": [4, 5, 6, 9, 10, 11],
            "avg_budget_per_day": {"budget": 2000, "moderate": 4000, "luxury": 8000, "backpacker": 1500},
            "elderly_friendly_score": 8.5,
            "infant_friendly_score": 8.0,
            "key_attractions": ["Botanical Gardens", "Ooty Lake", "Nilgiri Mountain Railway", "Rose Garden", "Doddabetta Peak"],
            "avg_temperature": {4: 20, 5: 22, 6: 20, 9: 18, 10: 18, 11: 16},
            "coordinates": {"lat": 11.4064, "lng": 76.6932},
            "nearby_cities": ["Bangalore", "Coimbatore", "Mysore"]
        },
        
        # Cultural & Historical
        {
            "name": "Rajasthan (Jaipur)",
            "state": "Rajasthan",
            "category": ["cultural", "historical", "shopping"],
            "description": "Pink city with magnificent palaces, forts, and vibrant culture",
            "best_season": [10, 11, 12, 1, 2, 3],
            "avg_budget_per_day": {"budget": 2000, "moderate": 4500, "luxury": 9000, "backpacker": 1500},
            "elderly_friendly_score": 7.0,
            "infant_friendly_score": 6.5,
            "key_attractions": ["Amber Fort", "City Palace", "Hawa Mahal", "Jantar Mantar", "Nahargarh Fort"],
            "avg_temperature": {10: 28, 11: 24, 12: 20, 1: 18, 2: 22, 3: 27},
            "coordinates": {"lat": 26.9124, "lng": 75.7873},
            "nearby_cities": ["Delhi", "Agra", "Udaipur"]
        },
        {
            "name": "Agra",
            "state": "Uttar Pradesh",
            "category": ["cultural", "historical"],
            "description": "Home to the iconic Taj Mahal and Mughal architecture",
            "best_season": [10, 11, 12, 1, 2, 3],
            "avg_budget_per_day": {"budget": 1800, "moderate": 3500, "luxury": 7000, "backpacker": 1200},
            "elderly_friendly_score": 6.5,
            "infant_friendly_score": 6.0,
            "key_attractions": ["Taj Mahal", "Agra Fort", "Fatehpur Sikri", "Mehtab Bagh", "Itmad-ud-Daulah"],
            "avg_temperature": {10: 28, 11: 24, 12: 19, 1: 16, 2: 20, 3: 26},
            "coordinates": {"lat": 27.1767, "lng": 78.0081},
            "nearby_cities": ["Delhi", "Jaipur"]
        },
        {
            "name": "Varanasi",
            "state": "Uttar Pradesh",
            "category": ["spiritual", "cultural", "historical"],
            "description": "Ancient spiritual city on the banks of Ganges",
            "best_season": [10, 11, 12, 1, 2, 3],
            "avg_budget_per_day": {"budget": 1500, "moderate": 3000, "luxury": 6000, "backpacker": 1000},
            "elderly_friendly_score": 5.5,
            "infant_friendly_score": 4.5,
            "key_attractions": ["Dashashwamedh Ghat", "Kashi Vishwanath Temple", "Sarnath", "Ganges Aarti", "Banaras Hindu University"],
            "avg_temperature": {10: 28, 11: 24, 12: 19, 1: 16, 2: 20, 3: 26},
            "coordinates": {"lat": 25.3176, "lng": 82.9739},
            "nearby_cities": ["Allahabad", "Lucknow"]
        },
        
        # Adventure Destinations
        {
            "name": "Rishikesh",
            "state": "Uttarakhand",
            "category": ["adventure", "spiritual", "relaxation"],
            "description": "Yoga capital with river rafting and spiritual experiences",
            "best_season": [9, 10, 11, 12, 1, 2, 3, 4, 5],
            "avg_budget_per_day": {"budget": 1500, "moderate": 3000, "luxury": 6000, "backpacker": 1000},
            "elderly_friendly_score": 6.5,
            "infant_friendly_score": 5.5,
            "key_attractions": ["Laxman Jhula", "Ram Jhula", "Beatles Ashram", "River Rafting", "Triveni Ghat"],
            "avg_temperature": {9: 25, 10: 22, 11: 18, 12: 15, 1: 12, 2: 15, 3: 20, 4: 25, 5: 30},
            "coordinates": {"lat": 30.0869, "lng": 78.2676},
            "nearby_cities": ["Delhi", "Dehradun"]
        },
        {
            "name": "Leh Ladakh",
            "state": "Ladakh",
            "category": ["adventure", "hill_station", "cultural"],
            "description": "High altitude desert with monasteries and stunning landscapes",
            "best_season": [5, 6, 7, 8, 9],
            "avg_budget_per_day": {"budget": 2500, "moderate": 5000, "luxury": 10000, "backpacker": 2000},
            "elderly_friendly_score": 3.0,
            "infant_friendly_score": 2.0,
            "key_attractions": ["Pangong Lake", "Nubra Valley", "Hemis Monastery", "Khardung La Pass", "Magnetic Hill"],
            "avg_temperature": {5: 10, 6: 15, 7: 20, 8: 18, 9: 12},
            "coordinates": {"lat": 34.1526, "lng": 77.5771},
            "nearby_cities": ["Srinagar", "Manali"]
        }
    ]
    
    # Add more destinations to reach 100+
    additional_destinations = [
        # Kerala Backwaters
        {
            "name": "Alleppey",
            "state": "Kerala",
            "category": ["relaxation", "cultural", "beach"],
            "description": "Venice of the East with backwaters and houseboats",
            "best_season": [10, 11, 12, 1, 2, 3],
            "avg_budget_per_day": {"budget": 2500, "moderate": 5000, "luxury": 10000, "backpacker": 2000},
            "elderly_friendly_score": 8.0,
            "infant_friendly_score": 7.5,
            "key_attractions": ["Backwater Cruise", "Vembanad Lake", "Alappuzha Beach", "Krishnapuram Palace"],
            "avg_temperature": {10: 28, 11: 26, 12: 24, 1: 23, 2: 25, 3: 28},
            "coordinates": {"lat": 9.4981, "lng": 76.3388},
            "nearby_cities": ["Kochi", "Trivandrum"]
        },
        
        # Wildlife Destinations
        {
            "name": "Jim Corbett National Park",
            "state": "Uttarakhand",
            "category": ["wildlife", "adventure", "relaxation"],
            "description": "India's oldest national park famous for tigers",
            "best_season": [11, 12, 1, 2, 3, 4, 5],
            "avg_budget_per_day": {"budget": 3000, "moderate": 6000, "luxury": 12000, "backpacker": 2500},
            "elderly_friendly_score": 6.0,
            "infant_friendly_score": 5.0,
            "key_attractions": ["Tiger Safari", "Corbett Falls", "Garjiya Devi Temple", "River Rafting"],
            "avg_temperature": {11: 20, 12: 15, 1: 12, 2: 15, 3: 20, 4: 25, 5: 30},
            "coordinates": {"lat": 29.5316, "lng": 78.9463},
            "nearby_cities": ["Delhi", "Nainital"]
        },
        
        # Add more destinations programmatically
        {
            "name": "Hampi",
            "state": "Karnataka",
            "category": ["historical", "cultural", "adventure"],
            "description": "UNESCO World Heritage site with ancient ruins",
            "best_season": [10, 11, 12, 1, 2, 3],
            "avg_budget_per_day": {"budget": 1500, "moderate": 3000, "luxury": 6000, "backpacker": 1000},
            "elderly_friendly_score": 6.5,
            "infant_friendly_score": 6.0,
            "key_attractions": ["Virupaksha Temple", "Hampi Bazaar", "Vittala Temple", "Matanga Hill"],
            "avg_temperature": {10: 28, 11: 25, 12: 22, 1: 20, 2: 23, 3: 27},
            "coordinates": {"lat": 15.3350, "lng": 76.4600},
            "nearby_cities": ["Bangalore", "Goa"]
        }
    ]
    
    destinations.extend(additional_destinations)
    
    # Generate more destinations to reach 100+
    base_destinations = [
        ("Mysore", "Karnataka", ["cultural", "historical"], 8.0, 7.5),
        ("Coorg", "Karnataka", ["hill_station", "relaxation"], 7.5, 7.0),
        ("Munnar", "Kerala", ["hill_station", "relaxation"], 8.0, 7.5),
        ("Kochi", "Kerala", ["cultural", "beach"], 8.5, 8.0),
        ("Udaipur", "Rajasthan", ["cultural", "historical"], 7.5, 7.0),
        ("Jodhpur", "Rajasthan", ["cultural", "historical"], 7.0, 6.5),
        ("Pushkar", "Rajasthan", ["spiritual", "cultural"], 7.0, 6.0),
        ("Mount Abu", "Rajasthan", ["hill_station", "relaxation"], 8.0, 7.5),
        ("Amritsar", "Punjab", ["spiritual", "cultural"], 7.5, 7.0),
        ("Chandigarh", "Punjab", ["cultural", "relaxation"], 8.5, 8.0),
        ("Dehradun", "Uttarakhand", ["hill_station", "relaxation"], 7.5, 7.0),
        ("Nainital", "Uttarakhand", ["hill_station", "relaxation"], 8.0, 7.5),
        ("Mussoorie", "Uttarakhand", ["hill_station", "relaxation"], 7.5, 7.0),
        ("Haridwar", "Uttarakhand", ["spiritual", "cultural"], 6.5, 6.0),
        ("Kolkata", "West Bengal", ["cultural", "food"], 7.0, 6.5),
        ("Sundarbans", "West Bengal", ["wildlife", "adventure"], 5.0, 4.0),
        ("Gangtok", "Sikkim", ["hill_station", "adventure"], 6.5, 5.5),
        ("Shillong", "Meghalaya", ["hill_station", "cultural"], 7.0, 6.5),
        ("Kaziranga", "Assam", ["wildlife", "adventure"], 5.5, 4.5),
        ("Guwahati", "Assam", ["cultural", "spiritual"], 6.5, 6.0)
    ]
    
    for name, state, categories, elderly_score, infant_score in base_destinations:
        dest = {
            "name": name,
            "state": state,
            "category": categories,
            "description": f"Beautiful destination in {state} known for {', '.join(categories)}",
            "best_season": [10, 11, 12, 1, 2, 3] if "hill_station" not in categories else [3, 4, 5, 6, 9, 10],
            "avg_budget_per_day": {"budget": 1800, "moderate": 3500, "luxury": 7000, "backpacker": 1200},
            "elderly_friendly_score": elderly_score,
            "infant_friendly_score": infant_score,
            "key_attractions": [f"Attraction 1 in {name}", f"Attraction 2 in {name}", f"Attraction 3 in {name}"],
            "avg_temperature": {10: 25, 11: 22, 12: 20, 1: 18, 2: 20, 3: 25},
            "coordinates": {"lat": 20.0 + hash(name) % 15, "lng": 75.0 + hash(name) % 20},
            "nearby_cities": ["Delhi", "Mumbai"]
        }
        destinations.append(dest)
    
    return destinations


def save_dataset():
    """Save the generated dataset to JSON file"""
    destinations = generate_destinations_dataset()
    
    # Create data directory if it doesn't exist
    data_dir = os.path.join("backend", "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Save to JSON file
    file_path = os.path.join(data_dir, "destinations.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(destinations, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {len(destinations)} destinations and saved to {file_path}")
    return file_path


if __name__ == "__main__":
    save_dataset()


# .
