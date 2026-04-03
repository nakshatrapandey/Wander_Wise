"""
Route Optimization Utility
Implements Dijkstra's algorithm for optimal route planning
"""
import heapq
from typing import List, Dict, Tuple, Optional, Set, Any
import math


class RouteOptimizer:
    """
    Route optimizer using Dijkstra's algorithm
    Optimizes routes based on distance or cost
    """
    
    def __init__(self):
        self.graph: Dict[str, Dict[str, float]] = {}
    
    def add_edge(self, from_city: str, to_city: str, weight: float):
        """
        Add an edge to the graph (bidirectional)
        Weight can be distance (km) or cost (INR)
        """
        if from_city not in self.graph:
            self.graph[from_city] = {}
        if to_city not in self.graph:
            self.graph[to_city] = {}
        
        self.graph[from_city][to_city] = weight
        self.graph[to_city][from_city] = weight  # Bidirectional
    
    def build_graph_from_destinations(
        self,
        destinations: List[str],
        distance_matrix: Optional[Dict[str, Dict[str, float]]] = None
    ):
        """
        Build graph from list of destinations
        If distance_matrix not provided, uses estimated distances
        """
        if distance_matrix:
            for from_city in destinations:
                for to_city in destinations:
                    if from_city != to_city and from_city in distance_matrix:
                        if to_city in distance_matrix[from_city]:
                            self.add_edge(
                                from_city,
                                to_city,
                                distance_matrix[from_city][to_city]
                            )
        else:
            # Create fully connected graph with estimated distances
            for i, from_city in enumerate(destinations):
                for j, to_city in enumerate(destinations):
                    if i < j:
                        # Estimate distance (simplified)
                        estimated_distance = self._estimate_distance(from_city, to_city)
                        self.add_edge(from_city, to_city, estimated_distance)
    
    def dijkstra(
        self,
        start: str,
        end: Optional[str] = None
    ) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
        """
        Dijkstra's algorithm implementation
        Returns: (distances, previous_nodes)
        """
        # Initialize distances and previous nodes
        distances: Dict[str, float] = {node: float('infinity') for node in self.graph}
        previous: Dict[str, Optional[str]] = {node: None for node in self.graph}
        distances[start] = 0
        
        # Priority queue: (distance, node)
        pq: List[Tuple[float, str]] = [(0, start)]
        visited: Set[str] = set()
        
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            # Skip if already visited
            if current_node in visited:
                continue
            
            visited.add(current_node)
            
            # Early termination if we reached the end
            if end and current_node == end:
                break
            
            # Skip if we found a better path already
            if current_distance > distances[current_node]:
                continue
            
            # Check neighbors
            for neighbor, weight in self.graph.get(current_node, {}).items():
                distance = current_distance + weight
                
                # If we found a shorter path
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))
        
        return distances, previous
    
    def find_shortest_path(
        self,
        start: str,
        end: str
    ) -> Tuple[List[str], float]:
        """
        Find shortest path between two nodes
        Returns: (path, total_distance)
        """
        if start not in self.graph or end not in self.graph:
            return [], float('infinity')
        
        distances, previous = self.dijkstra(start, end)
        
        # Reconstruct path
        path = []
        current = end
        
        while current is not None:
            path.append(current)
            current = previous[current]
        
        path.reverse()
        
        # Check if path is valid
        if not path or path[0] != start:
            return [], float('infinity')
        
        return path, distances[end]
    
    def optimize_multi_city_route(
        self,
        start: str,
        cities: List[str],
        return_to_start: bool = False
    ) -> Tuple[List[str], float]:
        """
        Optimize route through multiple cities (Traveling Salesman Problem approximation)
        Uses nearest neighbor heuristic
        Returns: (optimized_route, total_distance)
        """
        if not cities:
            return [start], 0.0
        
        route = [start]
        remaining = set(cities)
        total_distance = 0.0
        current = start
        
        # Nearest neighbor algorithm
        while remaining:
            nearest = None
            min_distance = float('infinity')
            
            for city in remaining:
                if city in self.graph.get(current, {}):
                    distance = self.graph[current][city]
                    if distance < min_distance:
                        min_distance = distance
                        nearest = city
            
            if nearest is None:
                # No path found, add remaining cities anyway
                route.extend(list(remaining))
                break
            
            route.append(nearest)
            total_distance += min_distance
            remaining.remove(nearest)
            current = nearest
        
        # Return to start if required
        if return_to_start and current != start:
            if start in self.graph.get(current, {}):
                route.append(start)
                total_distance += self.graph[current][start]
        
        return route, total_distance
    
    def optimize_route_with_constraints(
        self,
        start: str,
        destinations: List[str],
        max_distance_per_day: float = 300.0,
        max_days: Optional[int] = None
    ) -> List[List[str]]:
        """
        Optimize route with daily distance constraints
        Returns list of daily routes
        """
        if not destinations:
            return [[start]]
        
        # Get optimized route
        optimized_route, _ = self.optimize_multi_city_route(start, destinations)
        
        # Split into daily segments based on distance constraint
        daily_routes = []
        current_day = [optimized_route[0]]
        daily_distance = 0.0
        
        for i in range(1, len(optimized_route)):
            from_city = optimized_route[i-1]
            to_city = optimized_route[i]
            
            distance = self.graph.get(from_city, {}).get(to_city, 0)
            
            if daily_distance + distance > max_distance_per_day:
                # Start new day
                daily_routes.append(current_day)
                current_day = [to_city]
                daily_distance = 0.0
                
                # Check max days constraint
                if max_days and len(daily_routes) >= max_days:
                    break
            else:
                current_day.append(to_city)
                daily_distance += distance
        
        # Add last day
        if current_day:
            daily_routes.append(current_day)
        
        return daily_routes
    
    def calculate_route_cost(
        self,
        route: List[str],
        cost_per_km: float = 10.0
    ) -> float:
        """
        Calculate total cost for a route
        """
        total_cost = 0.0
        
        for i in range(len(route) - 1):
            from_city = route[i]
            to_city = route[i + 1]
            
            if from_city in self.graph and to_city in self.graph[from_city]:
                distance = self.graph[from_city][to_city]
                total_cost += distance * cost_per_km
        
        return total_cost
    
    def _estimate_distance(self, city1: str, city2: str) -> float:
        """
        Estimate distance between two cities (simplified)
        In production, this would use actual coordinates
        """
        # Simple hash-based estimation for demo
        hash1 = sum(ord(c) for c in city1)
        hash2 = sum(ord(c) for c in city2)
        
        # Generate pseudo-random but consistent distance
        distance = abs(hash1 - hash2) % 500 + 100
        return float(distance)
    
    def get_route_statistics(
        self,
        route: List[str]
    ) -> Dict[str, Any]:
        """
        Get statistics for a route
        """
        if len(route) < 2:
            return {
                "total_distance": 0.0,
                "num_cities": len(route),
                "avg_distance_between_cities": 0.0,
                "longest_segment": 0.0,
                "shortest_segment": 0.0
            }
        
        distances = []
        total_distance = 0.0
        
        for i in range(len(route) - 1):
            from_city = route[i]
            to_city = route[i + 1]
            
            if from_city in self.graph and to_city in self.graph[from_city]:
                distance = self.graph[from_city][to_city]
                distances.append(distance)
                total_distance += distance
        
        return {
            "total_distance": total_distance,
            "num_cities": len(route),
            "avg_distance_between_cities": total_distance / len(distances) if distances else 0.0,
            "longest_segment": max(distances) if distances else 0.0,
            "shortest_segment": min(distances) if distances else 0.0,
            "segments": len(distances)
        }


# .
