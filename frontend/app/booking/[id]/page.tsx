'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { ErrorMessage } from '@/components/ui/ErrorMessage';
import { BookingSummary as BookingSummaryComponent } from '@/components/booking/BookingSummary';
import { useBookingStore } from '@/store/useBookingStore';
import { api } from '@/lib/api';
import { BookingSummary } from '@/lib/types';

export default function BookingPage() {
  const params = useParams();
  const router = useRouter();
  const { summary: storedSummary, setSummary } = useBookingStore();
  
  const [summary, setLocalSummary] = useState<BookingSummary | null>(storedSummary);
  const [loading, setLoading] = useState(!storedSummary);
  const [error, setError] = useState<string | null>(null);
  const [processing, setProcessing] = useState(false);

  useEffect(() => {
    const fetchBookingSummary = async () => {
      try {
        setLoading(true);
        const data = await api.createBookingSummary(params.id as string);
        setLocalSummary(data);
        setSummary(data);
      } catch (err) {
        const error = err as Error;
        setError(error.message || 'Failed to create booking summary');
      } finally {
        setLoading(false);
      }
    };

    if (!storedSummary) {
      fetchBookingSummary();
    }
  }, [params.id]);

  const handleProceedToPayment = async () => {
    if (!summary) return;

    try {
      setProcessing(true);
      // Navigate to payment page
      router.push(`/payment/${params.id}`);
    } catch (err) {
      const error = err as Error;
      setError(error.message || 'Failed to proceed to payment');
    } finally {
      setProcessing(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" text="Preparing your booking..." />
      </div>
    );
  }

  if (error || !summary) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <ErrorMessage
          message={error || 'Booking summary not found'}
          onRetry={() => window.location.reload()}
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Booking Summary
          </h1>
          <p className="text-gray-600">
            Review your bookings before proceeding to payment
          </p>
        </div>

        {/* Booking Summary */}
        <BookingSummaryComponent summary={summary} />

        {/* Important Information */}
        <Card className="mt-6 bg-blue-50 border-blue-200">
          <div className="p-4">
            <h3 className="font-semibold text-blue-900 mb-2 flex items-center">
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
              Important Information
            </h3>
            <ul className="text-sm text-blue-800 space-y-1 ml-7">
              <li>• This is a simulated booking for demonstration purposes</li>
              <li>• No actual charges will be made</li>
              <li>• Booking confirmations are for reference only</li>
              <li>• All prices are estimates and may vary</li>
            </ul>
          </div>
        </Card>

        {/* Action Buttons */}
        <div className="mt-8 flex flex-col sm:flex-row gap-4">
          <Button
            variant="outline"
            onClick={() => router.push(`/itinerary/${params.id}`)}
            className="flex-1"
          >
            Back to Itinerary
          </Button>
          <Button
            onClick={handleProceedToPayment}
            isLoading={processing}
            className="flex-1"
          >
            Proceed to Payment
          </Button>
        </div>
      </div>
    </div>
  );
}

// Made with Bob
