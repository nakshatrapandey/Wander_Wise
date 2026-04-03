/**
 * User Preferences Store
 * Manages user travel preferences state
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { UserPreferences, TravelStyle, InterestCategory } from '@/lib/types';

interface PreferencesState extends UserPreferences {
  // Actions
  setPreferences: (prefs: Partial<UserPreferences>) => void;
  setBudget: (budget: number) => void;
  setDays: (days: number) => void;
  setStartingCity: (city: string) => void;
  setInterests: (interests: InterestCategory[]) => void;
  setTravelStyle: (style: TravelStyle) => void;
  setMonth: (month: number) => void;
  setNumTravelers: (num: number) => void;
  setHasElderly: (has: boolean) => void;
  setHasInfant: (has: boolean) => void;
  setAdditionalPreferences: (prefs: string) => void;
  reset: () => void;
  isComplete: () => boolean;
}

const initialState: UserPreferences = {
  budget: 50000,
  days: 5,
  starting_city: '',
  interests: [],
  travel_style: TravelStyle.MODERATE,
  month: new Date().getMonth() + 1,
  num_travelers: 2,
  has_elderly: false,
  has_infant: false,
  additional_preferences: '',
};

export const usePreferencesStore = create<PreferencesState>()(
  persist(
    (set, get) => ({
      ...initialState,

      setPreferences: (prefs) => set((state) => ({ ...state, ...prefs })),

      setBudget: (budget) => set({ budget }),

      setDays: (days) => set({ days }),

      setStartingCity: (starting_city) => set({ starting_city }),

      setInterests: (interests) => set({ interests }),

      setTravelStyle: (travel_style) => set({ travel_style }),

      setMonth: (month) => set({ month }),

      setNumTravelers: (num_travelers) => set({ num_travelers }),

      setHasElderly: (has_elderly) => set({ has_elderly }),

      setHasInfant: (has_infant) => set({ has_infant }),

      setAdditionalPreferences: (additional_preferences) => set({ additional_preferences }),

      reset: () => set(initialState),

      isComplete: () => {
        const state = get();
        return !!(
          state.budget > 0 &&
          state.days > 0 &&
          state.starting_city.trim() !== '' &&
          state.interests.length > 0
        );
      },
    }),
    {
      name: 'wanderwise-preferences',
    }
  )
);

// Made with Bob