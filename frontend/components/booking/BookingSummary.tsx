import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { formatCurrency } from '@/lib/utils';
import { BookingSummary as BookingSummaryType } from '@/lib/types';

interface BookingSummaryProps {
  summary: BookingSummaryType;
}

export const BookingSummary: React.FC<BookingSummaryProps> = ({ summary }) => {
  return (
    <div className="space-y-6">
      {/* Flights/Trains */}
      {summary.flights && summary.flights.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
              Flights & Trains
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {summary.flights.map((flight, index) => (
                <div key={index} className="p-4 bg-blue-50 rounded-lg border border-blue-100">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <p className="font-semibold text-gray-900">{flight.flight_number}</p>
                      <p className="text-sm text-gray-600">{flight.airline}</p>
                    </div>
                    <p className="font-bold text-blue-600">{formatCurrency(flight.price)}</p>
                  </div>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <p className="text-gray-600">Departure</p>
                      <p className="font-medium">{flight.departure}</p>
                      <p className="text-gray-500">{flight.departure_time}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Arrival</p>
                      <p className="font-medium">{flight.arrival}</p>
                      <p className="text-gray-500">{flight.arrival_time}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Hotels */}
      {summary.hotels && summary.hotels.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              Hotels
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {summary.hotels.map((hotel, index) => (
                <div key={index} className="p-4 bg-green-50 rounded-lg border border-green-100">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <p className="font-semibold text-gray-900">{hotel.hotel_name}</p>
                      <p className="text-sm text-gray-600">{hotel.location}</p>
                      <p className="text-sm text-gray-600">{hotel.room_type}</p>
                    </div>
                    <p className="font-bold text-green-600">{formatCurrency(hotel.total_price)}</p>
                  </div>
                  <div className="grid grid-cols-2 gap-4 text-sm mt-2">
                    <div>
                      <p className="text-gray-600">Check-in</p>
                      <p className="font-medium">{hotel.check_in}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Check-out</p>
                      <p className="font-medium">{hotel.check_out}</p>
                    </div>
                  </div>
                  <p className="text-sm text-gray-600 mt-2">
                    {hotel.total_nights} night(s) × {formatCurrency(hotel.price_per_night)}
                  </p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Local Transport */}
      {summary.transports && summary.transports.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
              </svg>
              Local Transport
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {summary.transports.map((transport, index) => (
                <div key={index} className="p-3 bg-purple-50 rounded-lg border border-purple-100 flex justify-between items-center">
                  <div>
                    <p className="font-medium text-gray-900">{transport.type}</p>
                    <p className="text-sm text-gray-600">
                      {transport.from_location} → {transport.to_location}
                    </p>
                    <p className="text-xs text-gray-500">{transport.date}</p>
                  </div>
                  <p className="font-semibold text-purple-600">{formatCurrency(transport.price)}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Activities */}
      {summary.activities_cost > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Activities & Experiences
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="p-4 bg-yellow-50 rounded-lg border border-yellow-100">
              <div className="flex justify-between items-center">
                <p className="text-gray-700">Total activities cost</p>
                <p className="font-bold text-yellow-600">{formatCurrency(summary.activities_cost)}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Grand Total */}
      <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-200">
        <CardContent className="p-6">
          <div className="flex justify-between items-center">
            <div>
              <p className="text-lg font-semibold text-gray-900">Grand Total</p>
              <p className="text-sm text-gray-600">All bookings included</p>
            </div>
            <p className="text-3xl font-bold text-blue-600">{formatCurrency(summary.total_cost)}</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

// Made with Bob
