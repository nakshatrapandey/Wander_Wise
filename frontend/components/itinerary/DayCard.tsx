import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Activity } from '@/lib/types';
import { formatCurrency } from '@/lib/utils';

interface DayCardProps {
  dayNumber: number;
  location: string;
  activities: Activity[];
  accommodation?: {
    name: string;
    type: string;
    price: number;
  };
  transport?: {
    mode: string;
    from: string;
    to: string;
    price: number;
  };
  totalCost: number;
}

export const DayCard: React.FC<DayCardProps> = ({
  dayNumber,
  location,
  activities,
  accommodation,
  transport,
  totalCost,
}) => {
  const [isExpanded, setIsExpanded] = useState(true);

  return (
    <Card className="mb-4" hover>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
              {dayNumber}
            </div>
            <div>
              <CardTitle>Day {dayNumber}</CardTitle>
              <p className="text-sm text-gray-600">{location}</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="text-right">
              <p className="text-sm text-gray-600">Daily Cost</p>
              <p className="text-lg font-semibold text-gray-900">
                {formatCurrency(totalCost)}
              </p>
            </div>
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <svg
                className={`w-5 h-5 text-gray-600 transition-transform ${
                  isExpanded ? 'rotate-180' : ''
                }`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </button>
          </div>
        </div>
      </CardHeader>

      {isExpanded && (
        <CardContent>
          {/* Transport */}
          {transport && (
            <div className="mb-4 p-3 bg-blue-50 rounded-lg border border-blue-100">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  <div>
                    <p className="font-medium text-gray-900">{transport.mode}</p>
                    <p className="text-sm text-gray-600">
                      {transport.from} → {transport.to}
                    </p>
                  </div>
                </div>
                <p className="font-semibold text-blue-600">
                  {formatCurrency(transport.price)}
                </p>
              </div>
            </div>
          )}

          {/* Activities */}
          <div className="space-y-3 mb-4">
            <h4 className="font-semibold text-gray-900 flex items-center">
              <svg className="w-5 h-5 mr-2 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Activities
            </h4>
            {activities.map((activity, index) => (
              <div
                key={index}
                className="p-3 bg-gray-50 rounded-lg border border-gray-200"
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex-1">
                    <h5 className="font-medium text-gray-900">{activity.name}</h5>
                    <p className="text-sm text-gray-600 mt-1">
                      {activity.description}
                    </p>
                  </div>
                  <p className="font-semibold text-gray-900 ml-4">
                    {formatCurrency(activity.estimated_cost)}
                  </p>
                </div>
                <div className="flex items-center space-x-4 text-xs text-gray-500">
                  <span className="flex items-center">
                    <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    {activity.duration}
                  </span>
                  <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded">
                    {activity.category}
                  </span>
                  {activity.is_elderly_friendly && (
                    <span className="px-2 py-1 bg-green-100 text-green-700 rounded">
                      Elderly Friendly
                    </span>
                  )}
                  {activity.is_infant_friendly && (
                    <span className="px-2 py-1 bg-purple-100 text-purple-700 rounded">
                      Infant Friendly
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* Accommodation */}
          {accommodation && (
            <div className="p-3 bg-green-50 rounded-lg border border-green-100">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                  </svg>
                  <div>
                    <p className="font-medium text-gray-900">{accommodation.name}</p>
                    <p className="text-sm text-gray-600">{accommodation.type}</p>
                  </div>
                </div>
                <p className="font-semibold text-green-600">
                  {formatCurrency(accommodation.price)}
                </p>
              </div>
            </div>
          )}
        </CardContent>
      )}
    </Card>
  );
};

// Made with Bob
