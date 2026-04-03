# WanderWise – Smart Adaptive AI Travel Planner

A production-grade AI-powered travel planning application with iterative refinement capabilities.

## Features

- 🤖 AI-powered personalized itinerary generation
- 💬 Chat-based iterative refinement
- 👴👶 Adaptive logic for elderly/infant travelers
- 💰 ML-based budget prediction
- 🗺️ Route optimization using Dijkstra's algorithm
- 🏨 Real-world data integration (Google Maps, Places, Weather)
- 💳 Unified QR-based payment simulation

## Tech Stack

### Frontend
- Next.js 14
- React 18
- Tailwind CSS
- Axios

### Backend
- FastAPI
- Python 3.10+
- MongoDB
- scikit-learn
- pandas

### External APIs
- Google Maps API
- Google Places API
- OpenWeather API
- Razorpay API

## Project Structure

```
wanderwise/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   ├── ml/
│   │   └── utils/
│   ├── data/
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── services/
│   │   └── utils/
│   ├── package.json
│   └── next.config.js
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB
- API Keys (Google Maps, Places, OpenWeather, Razorpay)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=wanderwise
GOOGLE_MAPS_API_KEY=your_key_here
GOOGLE_PLACES_API_KEY=your_key_here
OPENWEATHER_API_KEY=your_key_here
RAZORPAY_KEY_ID=your_key_here
RAZORPAY_KEY_SECRET=your_secret_here
```

5. Run backend:
```bash
uvicorn main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local` file:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Run frontend:
```bash
npm run dev
```

### Access Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Usage Flow

1. **Input Preferences**: Fill multi-step form with travel details
2. **Generate Itinerary**: AI creates personalized day-wise plan
3. **Refine Iteratively**: Chat with AI to modify itinerary
4. **Review & Book**: View final plan with budget breakdown
5. **Payment**: Scan QR code for simulated payment
6. **Confirmation**: Receive booking confirmations

## Development

### Generate Dataset
```bash
cd backend
python -m app.utils.generate_dataset
```

### Train ML Models
```bash
python -m app.ml.train_models
```

## License

MIT
