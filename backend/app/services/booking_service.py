"""
Booking Service
Handles booking summary generation and confirmation
"""
import uuid
import random
import string
from typing import List, Dict, Any
from datetime import datetime, timedelta

from app.models.schemas import (
    Itinerary,
    BookingSummary,
    FlightBooking,
    HotelBooking,
    TransportBooking,
    BookingConfirmation
)


class BookingService:
    """Service for managing bookings"""
    
    async def create_summary(self, itinerary: Itinerary) -> BookingSummary:
        """
        Create booking summary from finalized itinerary
        """
        flights = await self._extract_flights(itinerary)
        hotels = await self._extract_hotels(itinerary)
        transports = await self._extract_transports(itinerary)
        
        # Calculate activities cost
        activities_cost = sum(
            sum(act.estimated_cost for act in day.activities)
            for day in itinerary.days
        )
        
        # Calculate total cost
        total_cost = (
            sum(f.price for f in flights) +
            sum(h.total_price for h in hotels) +
            sum(t.price for t in transports) +
            activities_cost
        )
        
        booking_summary = BookingSummary(
            itinerary_id=itinerary.itinerary_id,
            flights=flights,
            hotels=hotels,
            transports=transports,
            activities_cost=activities_cost,
            total_cost=total_cost,
            payment_status="pending",
            booking_reference=self._generate_booking_reference()
        )
        
        return booking_summary
    
    async def _extract_flights(self, itinerary: Itinerary) -> List[FlightBooking]:
        """Extract flight bookings from itinerary"""
        flights = []
        
        # Check for inter-city travel
        destinations = itinerary.destinations
        
        if len(destinations) > 1:
            for i in range(len(destinations) - 1):
                from_city = destinations[i]
                to_city = destinations[i + 1]
                
                # Generate fake flight details
                flight = FlightBooking(
                    flight_number=self._generate_flight_number(),
                    airline=random.choice(["Air India", "IndiGo", "SpiceJet", "Vistara"]),
                    departure=from_city,
                    arrival=to_city,
                    departure_time=self._generate_time(),
                    arrival_time=self._generate_time(hours_offset=2),
                    price=random.uniform(3000, 8000)
                )
                flights.append(flight)
        
        return flights
    
    async def _extract_hotels(self, itinerary: Itinerary) -> List[HotelBooking]:
        """Extract hotel bookings from itinerary"""
        hotels = []
        
        # Group consecutive days by location
        current_location = None
        check_in_day = None
        nights = 0
        price_per_night = 0
        
        for idx, day in enumerate(itinerary.days):
            if day.location != current_location:
                # Save previous hotel booking
                if current_location and check_in_day:
                    hotel = HotelBooking(
                        hotel_name=f"Hotel in {current_location}",
                        location=current_location,
                        check_in=check_in_day.strftime("%Y-%m-%d"),
                        check_out=(check_in_day + timedelta(days=nights)).strftime("%Y-%m-%d"),
                        room_type="Standard Room",
                        price_per_night=price_per_night,
                        total_nights=nights,
                        total_price=price_per_night * nights
                    )
                    hotels.append(hotel)
                
                # Start new hotel booking
                current_location = day.location
                check_in_day = datetime.utcnow() + timedelta(days=idx)
                nights = 1
                price_per_night = day.accommodation.get("price_per_night", 2000) if day.accommodation else 2000
            else:
                nights += 1
        
        # Add last hotel
        if current_location and check_in_day:
            hotel = HotelBooking(
                hotel_name=f"Hotel in {current_location}",
                location=current_location,
                check_in=check_in_day.strftime("%Y-%m-%d"),
                check_out=(check_in_day + timedelta(days=nights)).strftime("%Y-%m-%d"),
                room_type="Standard Room",
                price_per_night=price_per_night,
                total_nights=nights,
                total_price=price_per_night * nights
            )
            hotels.append(hotel)
        
        return hotels
    
    async def _extract_transports(self, itinerary: Itinerary) -> List[TransportBooking]:
        """Extract transport bookings from itinerary"""
        transports = []
        
        for day in itinerary.days:
            if day.transport:
                transport = TransportBooking(
                    type=day.transport.get("mode", "Train"),
                    from_location=day.transport.get("from", ""),
                    to_location=day.transport.get("to", ""),
                    date=(datetime.utcnow() + timedelta(days=day.day - 1)).strftime("%Y-%m-%d"),
                    price=day.transport.get("price", 1000)
                )
                transports.append(transport)
        
        return transports
    
    async def generate_confirmation(
        self,
        booking_summary: BookingSummary
    ) -> BookingConfirmation:
        """
        Generate final booking confirmation with fake PNRs and booking IDs
        """
        confirmations = {}
        
        # Generate flight PNRs
        if booking_summary.flights:
            flight_pnrs = [self._generate_pnr() for _ in booking_summary.flights]
            confirmations["flights"] = flight_pnrs
            
            # Update flight bookings with PNRs
            for flight, pnr in zip(booking_summary.flights, flight_pnrs):
                flight.pnr = pnr
        
        # Generate hotel booking IDs
        if booking_summary.hotels:
            hotel_ids = [self._generate_booking_id("HTL") for _ in booking_summary.hotels]
            confirmations["hotels"] = hotel_ids
            
            # Update hotel bookings with IDs
            for hotel, booking_id in zip(booking_summary.hotels, hotel_ids):
                hotel.booking_id = booking_id
        
        # Generate transport booking IDs
        if booking_summary.transports:
            transport_ids = [self._generate_booking_id("TRN") for _ in booking_summary.transports]
            confirmations["transports"] = transport_ids
            
            # Update transport bookings with IDs
            for transport, booking_id in zip(booking_summary.transports, transport_ids):
                transport.booking_id = booking_id
        
        confirmation = BookingConfirmation(
            booking_reference=booking_summary.booking_reference or self._generate_booking_reference(),
            itinerary_id=booking_summary.itinerary_id,
            confirmations=confirmations,
            total_paid=booking_summary.total_cost,
            booking_date=datetime.utcnow(),
            status="confirmed"
        )
        
        return confirmation
    
    def _generate_flight_number(self) -> str:
        """Generate fake flight number"""
        airline_codes = ["AI", "6E", "SG", "UK", "G8"]
        number = random.randint(100, 9999)
        return f"{random.choice(airline_codes)}{number}"
    
    def _generate_time(self, hours_offset: int = 0) -> str:
        """Generate fake time"""
        base_time = datetime.utcnow() + timedelta(hours=hours_offset)
        hour = random.randint(6, 22)
        minute = random.choice([0, 15, 30, 45])
        return f"{hour:02d}:{minute:02d}"
    
    def _generate_pnr(self) -> str:
        """Generate fake PNR (6 alphanumeric characters)"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    def _generate_booking_id(self, prefix: str) -> str:
        """Generate fake booking ID"""
        number = ''.join(random.choices(string.digits, k=8))
        return f"{prefix}{number}"
    
    def _generate_booking_reference(self) -> str:
        """Generate unique booking reference"""
        return f"WW{uuid.uuid4().hex[:8].upper()}"


# .
