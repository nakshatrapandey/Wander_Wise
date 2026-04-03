'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { StepForm } from '@/components/forms/StepForm';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { ErrorMessage } from '@/components/ui/ErrorMessage';
import { usePreferencesStore } from '@/store/usePreferencesStore';
import { useItineraryStore } from '@/store/useItineraryStore';
import { api } from '@/lib/api';
import { InterestCategory, TravelStyle } from '@/lib/types';

const steps = [
  {
    id: 'basic',
    title: 'Basic Info',
    description: 'Tell us about your trip basics',
  },
  {
    id: 'preferences',
    title: 'Preferences',
    description: 'What are your interests and travel style?',
  },
  {
    id: 'special',
    title: 'Special Requirements',
    description: 'Any special considerations?',
  },
];

export default function PlanPage() {
  const router = useRouter();
  const store = usePreferencesStore();
  const { setItinerary, setLoading, setError } = useItineraryStore();
  
  const [formData, setFormData] = useState({
    budget: store.budget || 50000,
    days: store.days || 5,
    startingCity: store.starting_city || '',
    numTravelers: store.num_travelers || 2,
    interests: store.interests || [],
    travelStyle: store.travel_style || TravelStyle.MODERATE,
    month: store.month || new Date().getMonth() + 1,
    hasElderly: store.has_elderly || false,
    hasInfant: store.has_infant || false,
    additionalPreferences: store.additional_preferences || '',
  });

  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setErrorState] = useState<string | null>(null);

  const handleInputChange = (field: string, value: string | number | boolean) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleInterestToggle = (interest: InterestCategory) => {
    setFormData((prev) => ({
      ...prev,
      interests: prev.interests.includes(interest)
        ? prev.interests.filter((i: InterestCategory) => i !== interest)
        : [...prev.interests, interest],
    }));
  };

  const handleComplete = async () => {
    try {
      setIsGenerating(true);
      setErrorState(null);

      // Save preferences
      store.setPreferences({
        budget: formData.budget,
        days: formData.days,
        starting_city: formData.startingCity,
        num_travelers: formData.numTravelers,
        interests: formData.interests,
        travel_style: formData.travelStyle,
        month: formData.month,
        has_elderly: formData.hasElderly,
        has_infant: formData.hasInfant,
        additional_preferences: formData.additionalPreferences,
      });

      // Generate itinerary
      const itinerary = await api.generateItinerary({
        budget: formData.budget,
        days: formData.days,
        starting_city: formData.startingCity,
        interests: formData.interests,
        travel_style: formData.travelStyle,
        month: formData.month,
        num_travelers: formData.numTravelers,
        has_elderly: formData.hasElderly,
        has_infant: formData.hasInfant,
        additional_preferences: formData.additionalPreferences,
      });

      setItinerary(itinerary.itinerary);
      router.push(`/itinerary/${itinerary.itinerary.itinerary_id}`);
    } catch (err) {
      const error = err as Error;
      setErrorState(error.message || 'Failed to generate itinerary');
      setIsGenerating(false);
    }
  };

  if (isGenerating) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" text="Generating your perfect itinerary..." />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <Card padding="lg">
          {error && (
            <div className="mb-6">
              <ErrorMessage
                message={error}
                onRetry={() => setErrorState(null)}
              />
            </div>
          )}

          <StepForm steps={steps} onComplete={handleComplete}>
            {/* Step 1: Basic Info */}
            <div className="space-y-6">
              <Input
                label="Budget (INR)"
                type="number"
                value={formData.budget}
                onChange={(e) => handleInputChange('budget', Number(e.target.value))}
                required
                helperText="Total budget for your entire trip"
              />

              <Input
                label="Number of Days"
                type="number"
                value={formData.days}
                onChange={(e) => handleInputChange('days', Number(e.target.value))}
                required
                min={1}
                max={30}
              />

              <Input
                label="Starting City"
                type="text"
                value={formData.startingCity}
                onChange={(e) => handleInputChange('startingCity', e.target.value)}
                required
                placeholder="e.g., Mumbai, Delhi, Bangalore"
              />

              <Input
                label="Number of Travelers"
                type="number"
                value={formData.numTravelers}
                onChange={(e) => handleInputChange('numTravelers', Number(e.target.value))}
                required
                min={1}
                max={20}
              />
            </div>

            {/* Step 2: Preferences */}
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Interests <span className="text-red-500">*</span>
                </label>
                <div className="grid grid-cols-2 gap-3">
                  {Object.values(InterestCategory).map((interest) => (
                    <button
                      key={interest}
                      type="button"
                      onClick={() => handleInterestToggle(interest)}
                      className={`p-3 rounded-lg border-2 text-sm font-medium transition-colors ${
                        formData.interests.includes(interest)
                          ? 'border-blue-600 bg-blue-50 text-blue-700'
                          : 'border-gray-200 bg-white text-gray-700 hover:border-gray-300'
                      }`}
                    >
                      {interest}
                    </button>
                  ))}
                </div>
              </div>

              <Select
                label="Travel Style"
                value={formData.travelStyle}
                onChange={(e) => handleInputChange('travelStyle', e.target.value)}
                required
                options={Object.values(TravelStyle).map((style) => ({
                  value: style,
                  label: style.charAt(0) + style.slice(1).toLowerCase(),
                }))}
              />

              <Select
                label="Month of Travel"
                value={formData.month}
                onChange={(e) => handleInputChange('month', Number(e.target.value))}
                required
                options={[
                  { value: 1, label: 'January' },
                  { value: 2, label: 'February' },
                  { value: 3, label: 'March' },
                  { value: 4, label: 'April' },
                  { value: 5, label: 'May' },
                  { value: 6, label: 'June' },
                  { value: 7, label: 'July' },
                  { value: 8, label: 'August' },
                  { value: 9, label: 'September' },
                  { value: 10, label: 'October' },
                  { value: 11, label: 'November' },
                  { value: 12, label: 'December' },
                ]}
              />
            </div>

            {/* Step 3: Special Requirements */}
            <div className="space-y-6">
              <div className="space-y-4">
                <label className="flex items-center space-x-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.hasElderly}
                    onChange={(e) => handleInputChange('hasElderly', e.target.checked)}
                    className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  <span className="text-gray-700">Traveling with elderly person(s)</span>
                </label>

                <label className="flex items-center space-x-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.hasInfant}
                    onChange={(e) => handleInputChange('hasInfant', e.target.checked)}
                    className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  <span className="text-gray-700">Traveling with infant(s)</span>
                </label>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Additional Preferences
                </label>
                <textarea
                  value={formData.additionalPreferences}
                  onChange={(e) => handleInputChange('additionalPreferences', e.target.value)}
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Any specific requirements, dietary restrictions, accessibility needs, etc."
                />
              </div>

              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h4 className="font-semibold text-blue-900 mb-2">Ready to generate!</h4>
                <p className="text-sm text-blue-700">
                  Click "Generate Itinerary" to create your personalized travel plan using AI.
                </p>
              </div>
            </div>
          </StepForm>
        </Card>
      </div>
    </div>
  );
}

// Made with Bob
