/**
 * Itinerary Store
 * Manages itinerary state and operations
 */
import { create } from 'zustand';
import { Itinerary, ChatMessage } from '@/lib/types';

interface ItineraryState {
  // State
  current: Itinerary | null;
  loading: boolean;
  error: string | null;
  chatMessages: ChatMessage[];
  
  // Actions
  setItinerary: (itinerary: Itinerary) => void;
  updateItinerary: (updates: Partial<Itinerary>) => void;
  clearItinerary: () => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  
  // Chat actions
  addChatMessage: (message: ChatMessage) => void;
  clearChatMessages: () => void;
  
  // Computed
  isFinalized: () => boolean;
  getTotalCost: () => number;
  getDayCount: () => number;
}

export const useItineraryStore = create<ItineraryState>((set, get) => ({
  // Initial state
  current: null,
  loading: false,
  error: null,
  chatMessages: [],

  // Actions
  setItinerary: (itinerary) => set({ 
    current: itinerary, 
    loading: false, 
    error: null 
  }),

  updateItinerary: (updates) => set((state) => ({
    current: state.current ? { ...state.current, ...updates } : null,
  })),

  clearItinerary: () => set({ 
    current: null, 
    loading: false, 
    error: null,
    chatMessages: []
  }),

  setLoading: (loading) => set({ loading }),

  setError: (error) => set({ error, loading: false }),

  // Chat actions
  addChatMessage: (message) => set((state) => ({
    chatMessages: [...state.chatMessages, message],
  })),

  clearChatMessages: () => set({ chatMessages: [] }),

  // Computed
  isFinalized: () => {
    const state = get();
    return state.current?.is_finalized || false;
  },

  getTotalCost: () => {
    const state = get();
    return state.current?.budget_breakdown.total || 0;
  },

  getDayCount: () => {
    const state = get();
    return state.current?.days.length || 0;
  },
}));

// Made with Bob