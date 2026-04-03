/**
 * API Client for WanderWise Backend
 */
import axios, { AxiosInstance, AxiosError } from 'axios';
import {
  UserPreferences,
  ItineraryResponse,
  RefinementRequest,
  RefinementResponse,
  BookingSummary,
  PaymentRequest,
  PaymentResponse,
  BookingConfirmation,
  APIError
} from './types';

class WanderWiseAPI {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000, // 30 seconds
    });

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError<APIError>) => {
        if (error.response) {
          // Server responded with error
          throw new Error(error.response.data.error || 'An error occurred');
        } else if (error.request) {
          // Request made but no response
          throw new Error('No response from server. Please check your connection.');
        } else {
          // Error in request setup
          throw new Error(error.message || 'An error occurred');
        }
      }
    );
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    const response = await this.client.get('/health');
    return response.data;
  }

  // ============= Itinerary Endpoints =============

  /**
   * Generate new itinerary based on user preferences
   */
  async generateItinerary(preferences: UserPreferences): Promise<ItineraryResponse> {
    const response = await this.client.post<ItineraryResponse>(
      '/api/itinerary/generate',
      preferences
    );
    return response.data;
  }

  /**
   * Get itinerary by ID
   */
  async getItinerary(id: string): Promise<ItineraryResponse> {
    const response = await this.client.get<ItineraryResponse>(
      `/api/itinerary/${id}`
    );
    return response.data;
  }

  /**
   * List all itineraries
   */
  async listItineraries(skip: number = 0, limit: number = 10): Promise<{
    success: boolean;
    itineraries: any[];
    count: number;
  }> {
    const response = await this.client.get('/api/itinerary/', {
      params: { skip, limit }
    });
    return response.data;
  }

  /**
   * Delete itinerary
   */
  async deleteItinerary(id: string): Promise<{ success: boolean; message: string }> {
    const response = await this.client.delete(`/api/itinerary/${id}`);
    return response.data;
  }

  // ============= Refinement Endpoints =============

  /**
   * Refine itinerary with natural language
   */
  async refineItinerary(request: RefinementRequest): Promise<RefinementResponse> {
    const response = await this.client.post<RefinementResponse>(
      '/api/refinement/refine',
      request
    );
    return response.data;
  }

  /**
   * Finalize itinerary (no more changes)
   */
  async finalizeItinerary(id: string): Promise<{ success: boolean; message: string }> {
    const response = await this.client.post(`/api/refinement/finalize/${id}`);
    return response.data;
  }

  // ============= Booking Endpoints =============

  /**
   * Create booking summary from finalized itinerary
   */
  async createBookingSummary(itineraryId: string): Promise<BookingSummary> {
    const response = await this.client.post<BookingSummary>(
      `/api/booking/create-summary/${itineraryId}`
    );
    return response.data;
  }

  /**
   * Initiate payment and get QR code
   */
  async initiatePayment(paymentRequest: PaymentRequest): Promise<PaymentResponse> {
    const response = await this.client.post<PaymentResponse>(
      '/api/booking/payment/initiate',
      paymentRequest
    );
    return response.data;
  }

  /**
   * Verify payment
   */
  async verifyPayment(paymentId: string, signature: string): Promise<{
    success: boolean;
    message: string;
  }> {
    const response = await this.client.post(
      `/api/booking/payment/verify/${paymentId}`,
      null,
      { params: { signature } }
    );
    return response.data;
  }

  /**
   * Confirm booking and get confirmation details
   */
  async confirmBooking(bookingId: string): Promise<BookingConfirmation> {
    const response = await this.client.post<BookingConfirmation>(
      `/api/booking/confirm/${bookingId}`
    );
    return response.data;
  }

  /**
   * Get booking confirmation by reference
   */
  async getConfirmation(bookingReference: string): Promise<BookingConfirmation> {
    const response = await this.client.get<BookingConfirmation>(
      `/api/booking/confirmation/${bookingReference}`
    );
    return response.data;
  }
}

// Export singleton instance
export const api = new WanderWiseAPI();

// Export class for testing
export default WanderWiseAPI;

// Made with Bob