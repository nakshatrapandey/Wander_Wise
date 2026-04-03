/**
 * TypeScript types matching backend Pydantic schemas
 */

// Enums
export enum TravelStyle {
  BUDGET = "budget",
  MODERATE = "moderate",
  LUXURY = "luxury",
  BACKPACKER = "backpacker"
}

export enum InterestCategory {
  ADVENTURE = "adventure",
  BEACH = "beach",
  CULTURAL = "cultural",
  SPIRITUAL = "spiritual",
  WILDLIFE = "wildlife",
  HILL_STATION = "hill_station",
  HISTORICAL = "historical",
  FOOD = "food",
  SHOPPING = "shopping",
  RELAXATION = "relaxation"
}

// User Preferences
export interface UserPreferences {
  budget: number;
  days: number;
  starting_city: string;
  interests: InterestCategory[];
  travel_style: TravelStyle;
  month: number;
  num_travelers: number;
  has_elderly: boolean;
  has_infant: boolean;
  additional_preferences?: string;
}

// Activity
export interface Activity {
  name: string;
  description: string;
  duration: string;
  estimated_cost: number;
  category: string;
  location?: { lat: number; lng: number };
  is_elderly_friendly: boolean;
  is_infant_friendly: boolean;
}

// Day Plan
export interface DayPlan {
  day: number;
  date?: string;
  location: string;
  activities: Activity[];
  accommodation?: {
    hotel_name: string;
    location: string;
    room_type: string;
    price_per_night: number;
    amenities?: string[];
    rating?: number;
  };
  meals: Array<{ type: string; suggestion: string }>;
  transport?: {
    mode: string;
    from: string;
    to: string;
    price: number;
    duration: string;
    booking_required: boolean;
  };
  total_cost: number;
  notes?: string;
}

// Budget Breakdown
export interface BudgetBreakdown {
  accommodation: number;
  transport: number;
  activities: number;
  food: number;
  miscellaneous: number;
  total: number;
}

// Itinerary
export interface Itinerary {
  itinerary_id: string;
  user_id?: string;
  destinations: string[];
  days: DayPlan[];
  budget_breakdown: BudgetBreakdown;
  total_distance?: number;
  optimized_route?: string[];
  created_at: string;
  updated_at: string;
  version: number;
  is_finalized: boolean;
}

// Itinerary Response
export interface ItineraryResponse {
  success: boolean;
  itinerary: Itinerary;
  message: string;
  ml_predictions?: {
    budget_prediction: {
      predicted_budget: number;
      confidence: number;
      breakdown: Record<string, number>;
      factors: string[];
    };
  };
}

// Refinement
export interface RefinementRequest {
  itinerary_id: string;
  user_message: string;
  context?: Record<string, any>;
}

export interface RefinementResponse {
  success: boolean;
  itinerary: Itinerary;
  changes_made: string[];
  message: string;
}

// Booking
export interface FlightBooking {
  flight_number: string;
  airline: string;
  departure: string;
  arrival: string;
  departure_time: string;
  arrival_time: string;
  price: number;
  pnr?: string;
}

export interface HotelBooking {
  hotel_name: string;
  location: string;
  check_in: string;
  check_out: string;
  room_type: string;
  price_per_night: number;
  total_nights: number;
  total_price: number;
  booking_id?: string;
}

export interface TransportBooking {
  type: string;
  from_location: string;
  to_location: string;
  date: string;
  price: number;
  booking_id?: string;
}

export interface BookingSummary {
  itinerary_id: string;
  flights: FlightBooking[];
  hotels: HotelBooking[];
  transports: TransportBooking[];
  activities_cost: number;
  total_cost: number;
  payment_status: string;
  booking_reference?: string;
}

// Payment
export interface PaymentRequest {
  booking_summary_id: string;
  amount: number;
  currency: string;
}

export interface PaymentResponse {
  success: boolean;
  qr_code_url: string;
  payment_id: string;
  order_id: string;
  amount: number;
  currency: string;
}

// Booking Confirmation
export interface BookingConfirmation {
  booking_reference: string;
  itinerary_id: string;
  confirmations: Record<string, string[]>;
  total_paid: number;
  booking_date: string;
  status: string;
}

// API Error
export interface APIError {
  success: false;
  error: string;
  details?: Record<string, any>;
}

// Chat Message
export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

// Form Step
export interface FormStep {
  id: number;
  title: string;
  description: string;
}

// Made with Bob