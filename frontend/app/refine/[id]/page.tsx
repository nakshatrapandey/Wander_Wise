'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { ErrorMessage } from '@/components/ui/ErrorMessage';
import { ChatBox } from '@/components/chat/ChatBox';
import { DayCard } from '@/components/itinerary/DayCard';
import { useItineraryStore } from '@/store/useItineraryStore';
import { api } from '@/lib/api';
import { ChatMessage, Itinerary } from '@/lib/types';

export default function RefinePage() {
  const params = useParams();
  const router = useRouter();
  const { current, setItinerary } = useItineraryStore();
  
  const [itinerary, setLocalItinerary] = useState<Itinerary | null>(current);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(!current);
  const [refining, setRefining] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchItinerary = async () => {
      if (current && current.itinerary_id === params.id) {
        setLocalItinerary(current);
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const response = await api.getItinerary(params.id as string);
        setLocalItinerary(response.itinerary);
        setItinerary(response.itinerary);
      } catch (err) {
        const error = err as Error;
        setError(error.message || 'Failed to load itinerary');
      } finally {
        setLoading(false);
      }
    };

    if (params.id) {
      fetchItinerary();
    }
  }, [params.id]);

  const handleSendMessage = async (message: string) => {
    if (!itinerary) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: message,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setRefining(true);

    try {
      const response = await api.refineItinerary({
        itinerary_id: itinerary.itinerary_id,
        user_message: message,
      });
      
      const aiMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.message || 'Itinerary updated successfully!',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, aiMessage]);
      setLocalItinerary(response.itinerary);
      setItinerary(response.itinerary);
    } catch (err) {
      const error = err as Error;
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `Sorry, I couldn't process that request: ${error.message}`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setRefining(false);
    }
  };

  const handleFinalize = async () => {
    if (!itinerary) return;

    try {
      await api.finalizeItinerary(itinerary.itinerary_id);
      router.push(`/booking/${itinerary.itinerary_id}`);
    } catch (err) {
      const error = err as Error;
      setError(error.message || 'Failed to finalize itinerary');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" text="Loading itinerary..." />
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
    <div className="min-h-screen bg-gray-50">
      <div className="h-screen flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 px-4 py-4">
          <div className="max-w-7xl mx-auto flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Refine Your Itinerary</h1>
              <p className="text-sm text-gray-600">
                Chat with AI to make changes to your travel plan
              </p>
            </div>
            <div className="flex space-x-3">
              <Button
                variant="outline"
                onClick={() => router.push(`/itinerary/${itinerary.itinerary_id}`)}
              >
                Back to Itinerary
              </Button>
              <Button onClick={handleFinalize}>
                Done Refining
              </Button>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 overflow-hidden">
          <div className="h-full max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-4 p-4">
            {/* Left: Current Itinerary */}
            <div className="overflow-y-auto">
              <Card padding="md" className="mb-4">
                <h2 className="text-lg font-semibold text-gray-900 mb-2">
                  Current Itinerary
                </h2>
                <p className="text-sm text-gray-600">
                  {itinerary.destinations.join(' → ')} • {itinerary.days.length} Days
                </p>
              </Card>

              <div className="space-y-4">
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
            </div>

            {/* Right: Chat Interface */}
            <div className="flex flex-col h-full">
              <Card padding="none" className="flex-1 flex flex-col overflow-hidden">
                <ChatBox
                  messages={messages}
                  onSendMessage={handleSendMessage}
                  isLoading={refining}
                />
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Made with Bob
