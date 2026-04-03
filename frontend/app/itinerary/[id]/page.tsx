'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { ErrorMessage } from '@/components/ui/ErrorMessage';
import { DayCard } from '@/components/itinerary/DayCard';
import { useItineraryStore } from '@/store/useItineraryStore';
import { api } from '@/lib/api';
import { formatCurrency } from '@/lib/utils';
import { Itinerary } from '@/lib/types';

export default function ItineraryPage() {
  const params = useParams();
  const router = useRouter();
  const { current, setItinerary } = useItineraryStore();
  const [itinerary, setLocalItinerary] = useState<Itinerary | null>(current);
  const [loading, setLocalLoading] = useState(!current);
  const [error, setLocalError] = useState<string | null>(null);

  useEffect(() => {
    const fetchItinerary = async () => {
      if (current && current.itinerary_id === params.id) {
        setLocalItinerary(current);
        setLocalLoading(false);
        return;
      }

      try {
        setLocalLoading(true);
        const response = await api.getItinerary(params.id as string);
        setLocalItinerary(response.itinerary);
        setItinerary(response.itinerary);
      } catch (err) {
        const error = err as Error;
        setLocalError(error.message || 'Failed to load itinerary');
      } finally {
        setLocalLoading(false);
      }
    };

    if (params.id) {
      fetchItinerary();
    }
  }, [params.id]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" text="Loading your itinerary..." />
      </div>
    );
  }

  if (error || !itinerary) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <ErrorMessage
          message={error || 'Itinerary not found'}
          onRetry={() => window.location.reload()}
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <Card className="mb-6" padding="lg">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div className="mb-4 md:mb-0">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Your Travel Itinerary
              </h1>
              <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                <span className="flex items-center">
                  <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  {itinerary.destinations.join(' → ')}
                </span>
                <span className="flex items-center">
                  <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  {itinerary.days.length} Days
                </span>
                <span className="flex items-center">
                  <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {formatCurrency(itinerary.budget_breakdown.total)}
                </span>
              </div>
            </div>
            <div className="flex flex-col sm:flex-row gap-3">
              <Button
                variant="outline"
                onClick={() => router.push(`/refine/${itinerary.itinerary_id}`)}
              >
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
                Refine with AI
              </Button>
              <Button
                onClick={() => router.push(`/booking/${itinerary.itinerary_id}`)}
                disabled={itinerary.is_finalized}
              >
                {itinerary.is_finalized ? 'Finalized' : 'Finalize & Book'}
              </Button>
            </div>
          </div>
        </Card>

        {/* Budget Summary */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <Card padding="md">
            <p className="text-sm text-gray-600 mb-1">Accommodation</p>
            <p className="text-xl font-bold text-gray-900">
              {formatCurrency(itinerary.budget_breakdown.accommodation)}
            </p>
          </Card>
          <Card padding="md">
            <p className="text-sm text-gray-600 mb-1">Transport</p>
            <p className="text-xl font-bold text-gray-900">
              {formatCurrency(itinerary.budget_breakdown.transport)}
            </p>
          </Card>
          <Card padding="md">
            <p className="text-sm text-gray-600 mb-1">Activities</p>
            <p className="text-xl font-bold text-gray-900">
              {formatCurrency(itinerary.budget_breakdown.activities)}
            </p>
          </Card>
          <Card padding="md">
            <p className="text-sm text-gray-600 mb-1">Food & Misc</p>
            <p className="text-xl font-bold text-gray-900">
              {formatCurrency(itinerary.budget_breakdown.food + itinerary.budget_breakdown.miscellaneous)}
            </p>
          </Card>
        </div>

        {/* Day-by-Day Itinerary */}
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Day-by-Day Plan</h2>
          {itinerary.days.map((day) => (
            <DayCard
              key={day.day}
              dayNumber={day.day}
              location={day.location}
              activities={day.activities}
              accommodation={day.accommodation ? {
                name: day.accommodation.hotel_name,
                type: day.accommodation.room_type,
                price: day.accommodation.price_per_night,
              } : undefined}
              transport={day.transport}
              totalCost={day.total_cost}
            />
          ))}
        </div>

        {/* Notes Section */}
        <Card padding="lg">
          <CardHeader>
            <CardTitle>Travel Tips</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-700">
              Your personalized itinerary is ready! Use the "Refine with AI" button to make any adjustments.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

// Made with Bob
