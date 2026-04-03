/**
 * Booking Store
 * Manages booking and payment state
 */
import { create } from 'zustand';
import { BookingSummary, BookingConfirmation, PaymentResponse } from '@/lib/types';

interface BookingState {
  // State
  summary: BookingSummary | null;
  confirmation: BookingConfirmation | null;
  payment: PaymentResponse | null;
  paymentStatus: 'pending' | 'processing' | 'completed' | 'failed';
  loading: boolean;
  error: string | null;
  
  // Actions
  setBookingSummary: (summary: BookingSummary) => void;
  setConfirmation: (confirmation: BookingConfirmation) => void;
  setPayment: (payment: PaymentResponse) => void;
  setPaymentStatus: (status: 'pending' | 'processing' | 'completed' | 'failed') => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearBooking: () => void;
  
  // Computed
  getTotalCost: () => number;
  hasFlights: () => boolean;
  hasHotels: () => boolean;
  hasTransports: () => boolean;
}

export const useBookingStore = create<BookingState>((set, get) => ({
  // Initial state
  summary: null,
  confirmation: null,
  payment: null,
  paymentStatus: 'pending',
  loading: false,
  error: null,

  // Actions
  setBookingSummary: (summary) => set({ 
    summary, 
    loading: false, 
    error: null 
  }),

  setConfirmation: (confirmation) => set({ 
    confirmation, 
    paymentStatus: 'completed',
    loading: false, 
    error: null 
  }),

  setPayment: (payment) => set({ 
    payment, 
    paymentStatus: 'processing',
    loading: false, 
    error: null 
  }),

  setPaymentStatus: (paymentStatus) => set({ paymentStatus }),

  setLoading: (loading) => set({ loading }),

  setError: (error) => set({ error, loading: false }),

  clearBooking: () => set({
    summary: null,
    confirmation: null,
    payment: null,
    paymentStatus: 'pending',
    loading: false,
    error: null,
  }),

  // Computed
  getTotalCost: () => {
    const state = get();
    return state.summary?.total_cost || 0;
  },

  hasFlights: () => {
    const state = get();
    return (state.summary?.flights.length || 0) > 0;
  },

  hasHotels: () => {
    const state = get();
    return (state.summary?.hotels.length || 0) > 0;
  },

  hasTransports: () => {
    const state = get();
    return (state.summary?.transports.length || 0) > 0;
  },
}));

// Made with Bob