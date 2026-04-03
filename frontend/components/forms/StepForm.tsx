'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { cn } from '@/lib/utils';

interface Step {
  id: string;
  title: string;
  description?: string;
}

interface StepFormProps {
  steps: Step[];
  children: React.ReactNode[];
  onComplete: () => void;
  onStepChange?: (step: number) => void;
}

export const StepForm: React.FC<StepFormProps> = ({
  steps,
  children,
  onComplete,
  onStepChange,
}) => {
  const [currentStep, setCurrentStep] = useState(0);

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      const nextStep = currentStep + 1;
      setCurrentStep(nextStep);
      onStepChange?.(nextStep);
    } else {
      onComplete();
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      const prevStep = currentStep - 1;
      setCurrentStep(prevStep);
      onStepChange?.(prevStep);
    }
  };

  return (
    <div className="w-full">
      {/* Progress Bar */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-2">
          {steps.map((step, index) => (
            <React.Fragment key={step.id}>
              <div className="flex flex-col items-center flex-1">
                <div
                  className={cn(
                    'w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-colors',
                    index <= currentStep
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-200 text-gray-600'
                  )}
                >
                  {index + 1}
                </div>
                <span
                  className={cn(
                    'text-xs mt-2 text-center',
                    index <= currentStep ? 'text-blue-600 font-medium' : 'text-gray-500'
                  )}
                >
                  {step.title}
                </span>
              </div>
              {index < steps.length - 1 && (
                <div
                  className={cn(
                    'flex-1 h-1 mx-2 rounded transition-colors',
                    index < currentStep ? 'bg-blue-600' : 'bg-gray-200'
                  )}
                />
              )}
            </React.Fragment>
          ))}
        </div>
      </div>

      {/* Current Step Description */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          {steps[currentStep].title}
        </h2>
        {steps[currentStep].description && (
          <p className="text-gray-600">{steps[currentStep].description}</p>
        )}
      </div>

      {/* Step Content */}
      <div className="mb-8">{children[currentStep]}</div>

      {/* Navigation Buttons */}
      <div className="flex justify-between">
        <Button
          variant="outline"
          onClick={handleBack}
          disabled={currentStep === 0}
        >
          Back
        </Button>
        <Button onClick={handleNext}>
          {currentStep === steps.length - 1 ? 'Generate Itinerary' : 'Next'}
        </Button>
      </div>
    </div>
  );
};

// Made with Bob
