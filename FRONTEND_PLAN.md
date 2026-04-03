# WanderWise Frontend - Implementation Plan

## 🎯 Frontend Architecture

### Technology Stack
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **State Management:** Zustand
- **HTTP Client:** Axios
- **UI Components:** Custom + Headless UI
- **Icons:** Lucide React

## 📁 Project Structure

```
frontend/
├── app/
│   ├── layout.tsx                 # Root layout
│   ├── page.tsx                   # Home page
│   ├── plan/
│   │   └── page.tsx              # Multi-step input form
│   ├── itinerary/
│   │   └── [id]/
│   │       └── page.tsx          # Itinerary display
│   ├── refine/
│   │   └── [id]/
│   │       └── page.tsx          # AI refinement interface
│   ├── budget/
│   │   └── [id]/
│   │       └── page.tsx          # Budget dashboard
│   ├── booking/
│   │   └── [id]/
│   │       └── page.tsx          # Booking summary
│   ├── payment/
│   │   └── [id]/
│   │       └── page.tsx          # Payment QR page
│   └── confirmation/
│       └── [id]/
│           └── page.tsx          # Booking confirmation
├── components/
│   ├── layout/
│   │   ├── Navbar.tsx
│   │   └── Footer.tsx
│   ├── forms/
│   │   ├── StepForm.tsx
│   │   ├── PreferencesForm.tsx
│   │   └── FormStep.tsx
│   ├── itinerary/
│   │   ├── ItineraryCard.tsx
│   │   ├── DayCard.tsx
│   │   ├── ActivityCard.tsx
│   │   └── ItineraryTimeline.tsx
│   ├── chat/
│   │   ├── ChatBox.tsx
│   │   ├── ChatMessage.tsx
│   │   └── ChatInput.tsx
│   ├── budget/
│   │   ├── BudgetChart.tsx
│   │   ├── BudgetBreakdown.tsx
│   │   └── CostSummary.tsx
│   ├── booking/
│   │   ├── BookingSummary.tsx
│   │   ├── FlightCard.tsx
│   │   ├── HotelCard.tsx
│   │   └── TransportCard.tsx
│   ├── payment/
│   │   ├── QRDisplay.tsx
│   │   └── PaymentStatus.tsx
│   └── ui/
│       ├── Button.tsx
│       ├── Card.tsx
│       ├── Input.tsx
│       ├── Select.tsx
│       ├── LoadingSpinner.tsx
│       └── ErrorMessage.tsx
├── lib/
│   ├── api.ts                    # API client
│   ├── types.ts                  # TypeScript types
│   └── utils.ts                  # Utility functions
├── store/
│   ├── usePreferencesStore.ts    # User preferences state
│   ├── useItineraryStore.ts      # Itinerary state
│   └── useBookingStore.ts        # Booking state
└── styles/
    └── globals.css               # Global styles
```

## 🎨 Pages Implementation

### 1. Home Page (`/`)
**Purpose:** Landing page with project introduction

**Components:**
- Hero section with CTA
- Feature highlights
- "Start Planning" button → `/plan`

**Design:**
- Modern, clean layout
- Gradient backgrounds
- Travel-themed imagery

### 2. Planning Page (`/plan`)
**Purpose:** Multi-step form for user preferences

**Steps:**
1. **Basic Info**
   - Budget (INR)
   - Number of days
   - Starting city
   - Number of travelers

2. **Preferences**
   - Interests (multi-select)
   - Travel style (budget/moderate/luxury)
   - Month of travel

3. **Special Requirements**
   - Traveling with elderly?
   - Traveling with infant?
   - Additional preferences (textarea)

**Features:**
- Progress indicator
- Form validation
- Back/Next navigation
- Submit → Generate itinerary

### 3. Itinerary Page (`/itinerary/[id]`)
**Purpose:** Display generated itinerary

**Layout:**
- **Header:** Destination names, total days, budget
- **Timeline:** Day-by-day breakdown
- **Day Cards:**
  - Day number and location
  - Activities list with costs
  - Accommodation details
  - Transport info
  - Daily total cost

**Actions:**
- "Refine with AI" button → `/refine/[id]`
- "View Budget" button → `/budget/[id]`
- "Finalize & Book" button → `/booking/[id]`

### 4. Refinement Page (`/refine/[id]`)
**Purpose:** Chat-based itinerary refinement

**Layout:**
- **Left Panel:** Current itinerary (read-only)
- **Right Panel:** Chat interface

**Chat Features:**
- Message history
- User input box
- Send button
- Loading states
- Real-time updates

**Example Messages:**
- "Reduce budget by 20%"
- "Remove trekking activities"
- "Add more relaxation"
- "Make it elderly-friendly"

**Actions:**
- Apply changes → Update itinerary
- "Done Refining" → Back to itinerary

### 5. Budget Dashboard (`/budget/[id]`)
**Purpose:** Visualize budget breakdown

**Components:**
- **Pie Chart:** Category distribution
  - Accommodation
  - Transport
  - Activities
  - Food
  - Miscellaneous

- **Bar Chart:** Daily costs
- **Summary Cards:**
  - Total budget
  - Spent amount
  - Remaining

**Features:**
- Interactive charts
- Hover tooltips
- Export option

### 6. Booking Page (`/booking/[id]`)
**Purpose:** Review and confirm bookings

**Sections:**
1. **Flights/Trains**
   - Route, time, price
   - Airline/operator

2. **Hotels**
   - Name, location, nights
   - Check-in/out dates
   - Total price

3. **Transports**
   - Type, route, date
   - Price

4. **Activities**
   - Total activities cost

5. **Grand Total**
   - All costs combined

**Actions:**
- "Proceed to Payment" → `/payment/[id]`

### 7. Payment Page (`/payment/[id]`)
**Purpose:** Display QR code for payment

**Layout:**
- **QR Code:** Large, centered
- **Payment Details:**
  - Amount
  - Order ID
  - Booking reference

**Features:**
- QR code display
- Payment instructions
- "I've Paid" button → Verify → `/confirmation/[id]`

### 8. Confirmation Page (`/confirmation/[id]`)
**Purpose:** Show booking confirmations

**Display:**
- **Success Message**
- **Booking Reference**
- **Flight PNRs** (list)
- **Hotel Booking IDs** (list)
- **Transport Booking IDs** (list)
- **Total Paid**
- **Booking Date**

**Actions:**
- Download confirmation (PDF)
- Email confirmation
- "Plan Another Trip" → `/`

## 🧩 Component Details

### StepForm Component
```typescript
interface StepFormProps {
  steps: Step[];
  currentStep: number;
  onNext: () => void;
  onBack: () => void;
  onSubmit: (data: any) => void;
}
```

**Features:**
- Progress bar
- Step validation
- Data persistence
- Smooth transitions

### ChatBox Component
```typescript
interface ChatBoxProps {
  itineraryId: string;
  messages: Message[];
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}
```

**Features:**
- Auto-scroll to bottom
- Message timestamps
- User/AI message styling
- Loading indicator

### ItineraryCard Component
```typescript
interface ItineraryCardProps {
  itinerary: Itinerary;
  editable?: boolean;
  onRefine?: () => void;
}
```

**Features:**
- Collapsible days
- Activity details
- Cost display
- Action buttons

### BudgetChart Component
```typescript
interface BudgetChartProps {
  breakdown: BudgetBreakdown;
  type: 'pie' | 'bar' | 'line';
}
```

**Features:**
- Recharts integration
- Responsive design
- Interactive tooltips
- Color-coded categories

## 🔄 State Management (Zustand)

### Preferences Store
```typescript
interface PreferencesState {
  budget: number;
  days: number;
  startingCity: string;
  interests: string[];
  travelStyle: string;
  month: number;
  numTravelers: number;
  hasElderly: boolean;
  hasInfant: boolean;
  additionalPreferences: string;
  
  setPreferences: (prefs: Partial<PreferencesState>) => void;
  reset: () => void;
}
```

### Itinerary Store
```typescript
interface ItineraryState {
  current: Itinerary | null;
  loading: boolean;
  error: string | null;
  
  setItinerary: (itinerary: Itinerary) => void;
  updateItinerary: (updates: Partial<Itinerary>) => void;
  clearItinerary: () => void;
}
```

### Booking Store
```typescript
interface BookingState {
  summary: BookingSummary | null;
  confirmation: BookingConfirmation | null;
  paymentStatus: string;
  
  setBookingSummary: (summary: BookingSummary) => void;
  setConfirmation: (confirmation: BookingConfirmation) => void;
  updatePaymentStatus: (status: string) => void;
}
```

## 🌐 API Integration

### API Client (`lib/api.ts`)
```typescript
class WanderWiseAPI {
  private baseURL: string;
  private axios: AxiosInstance;
  
  // Itinerary
  generateItinerary(preferences: UserPreferences): Promise<Itinerary>
  getItinerary(id: string): Promise<Itinerary>
  
  // Refinement
  refineItinerary(id: string, message: string): Promise<Itinerary>
  finalizeItinerary(id: string): Promise<void>
  
  // Booking
  createBookingSummary(id: string): Promise<BookingSummary>
  initiatePayment(bookingId: string, amount: number): Promise<PaymentResponse>
  confirmBooking(bookingId: string): Promise<BookingConfirmation>
}
```

## 🎨 UI/UX Guidelines

### Design Principles
1. **Clean & Modern:** Minimalist design with focus on content
2. **Responsive:** Mobile-first approach
3. **Accessible:** WCAG 2.1 AA compliance
4. **Fast:** Optimized loading and transitions

### Color Scheme
- **Primary:** Blue (#3B82F6)
- **Secondary:** Indigo (#6366F1)
- **Success:** Green (#10B981)
- **Warning:** Yellow (#F59E0B)
- **Error:** Red (#EF4444)
- **Neutral:** Gray shades

### Typography
- **Headings:** Inter (Bold)
- **Body:** Inter (Regular)
- **Monospace:** JetBrains Mono

### Spacing
- Use Tailwind's spacing scale (4px base)
- Consistent padding/margins
- Generous whitespace

## 📱 Responsive Design

### Breakpoints
- **Mobile:** < 640px
- **Tablet:** 640px - 1024px
- **Desktop:** > 1024px

### Mobile Optimizations
- Hamburger menu
- Stacked layouts
- Touch-friendly buttons
- Simplified charts

## ⚡ Performance Optimizations

1. **Code Splitting:** Dynamic imports for heavy components
2. **Image Optimization:** Next.js Image component
3. **Lazy Loading:** Load components on demand
4. **Caching:** SWR for data fetching
5. **Minification:** Production builds

## 🧪 Testing Strategy

1. **Unit Tests:** Component testing with Jest
2. **Integration Tests:** API integration tests
3. **E2E Tests:** User flow testing with Playwright
4. **Accessibility Tests:** axe-core integration

## 📦 Additional Dependencies

```json
{
  "dependencies": {
    "zustand": "^4.5.0",
    "axios": "^1.6.0",
    "recharts": "^2.10.0",
    "lucide-react": "^0.300.0",
    "@headlessui/react": "^1.7.0",
    "react-hook-form": "^7.49.0",
    "zod": "^3.22.0"
  }
}
```

## 🚀 Implementation Order

1. ✅ Setup Next.js project
2. ⏳ Install dependencies
3. ⏳ Create base layout (Navbar, Footer)
4. ⏳ Implement Home page
5. ⏳ Build StepForm component
6. ⏳ Create Planning page
7. ⏳ Implement API client
8. ⏳ Build Itinerary page
9. ⏳ Create ChatBox component
10. ⏳ Implement Refinement page
11. ⏳ Build Budget dashboard
12. ⏳ Create Booking page
13. ⏳ Implement Payment page
14. ⏳ Build Confirmation page
15. ⏳ Add loading states
16. ⏳ Implement error handling
17. ⏳ Polish UI/UX
18. ⏳ Test end-to-end flow

---

**Status:** Ready to implement frontend components
