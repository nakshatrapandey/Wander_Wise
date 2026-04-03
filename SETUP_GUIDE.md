# WanderWise - Complete Setup Guide

## 📋 Prerequisites

### Required Software
- **Python:** 3.10 or higher
- **Node.js:** 18.0 or higher
- **MongoDB:** 4.4 or higher (local or Atlas)
- **Git:** Latest version

### API Keys (Optional for Testing)
- Google Maps API Key
- Google Places API Key
- OpenWeather API Key
- Razorpay Key ID & Secret

**Note:** The system works in simulation mode without API keys for testing.

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone <repository-url>
cd wanderwise
```

### 2. Backend Setup

#### Step 1: Navigate to Backend
```bash
cd backend
```

#### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Create Environment File
Create `.env` file in `backend/` directory:

```env
# MongoDB
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=wanderwise

# API Keys (Optional - works without them)
GOOGLE_MAPS_API_KEY=your_key_here
GOOGLE_PLACES_API_KEY=your_key_here
OPENWEATHER_API_KEY=your_key_here

# Razorpay (Optional)
RAZORPAY_KEY_ID=your_key_here
RAZORPAY_KEY_SECRET=your_secret_here

# Security
SECRET_KEY=your-secret-key-change-in-production-use-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
```

#### Step 5: Generate Dataset (Already Done)
```bash
python -m app.utils.generate_dataset
```

#### Step 6: Start MongoDB
```bash
# If using local MongoDB
mongod

# Or use MongoDB Atlas (cloud)
# Update MONGODB_URL in .env with Atlas connection string
```

#### Step 7: Run Backend Server
```bash
uvicorn main:app --reload --port 8000
```

Backend will be available at:
- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### 3. Frontend Setup

#### Step 1: Navigate to Frontend
```bash
cd frontend
```

#### Step 2: Install Dependencies
```bash
npm install

# Install additional dependencies
npm install zustand axios recharts lucide-react @headlessui/react react-hook-form zod
```

#### Step 3: Create Environment File
Create `.env.local` file in `frontend/` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Step 4: Run Frontend Server
```bash
npm run dev
```

Frontend will be available at:
- **App:** http://localhost:3000

## 📁 Project Structure

```
wanderwise/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Configuration
│   │   ├── models/           # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   ├── ml/               # ML models
│   │   └── utils/            # Utilities
│   ├── data/
│   │   └── destinations.json # Dataset
│   ├── .env                  # Environment variables
│   ├── main.py               # FastAPI app
│   └── requirements.txt      # Python dependencies
│
├── frontend/
│   ├── app/                  # Next.js pages
│   ├── components/           # React components
│   ├── lib/                  # Utilities
│   ├── store/                # State management
│   ├── .env.local            # Environment variables
│   └── package.json          # Node dependencies
│
├── BACKEND_IMPLEMENTATION.md # Backend docs
├── FRONTEND_PLAN.md          # Frontend plan
├── PROJECT_STATUS.md         # Status report
├── SETUP_GUIDE.md            # This file
└── README.md                 # Project overview
```

## 🧪 Testing the System

### 1. Test Backend API

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Generate Itinerary
```bash
curl -X POST http://localhost:8000/api/itinerary/generate \
  -H "Content-Type: application/json" \
  -d '{
    "budget": 50000,
    "days": 5,
    "starting_city": "Delhi",
    "interests": ["beach", "relaxation"],
    "travel_style": "moderate",
    "month": 12,
    "num_travelers": 2,
    "has_elderly": false,
    "has_infant": false
  }'
```

### 2. Test Frontend

1. Open http://localhost:3000
2. Click "Start Planning"
3. Fill in preferences
4. Generate itinerary
5. Try refinement
6. Complete booking flow

## 🔧 Troubleshooting

### Backend Issues

#### MongoDB Connection Error
```
Error: Could not connect to MongoDB
```
**Solution:**
- Ensure MongoDB is running
- Check MONGODB_URL in .env
- Verify MongoDB port (default: 27017)

#### Import Errors
```
ModuleNotFoundError: No module named 'fastapi'
```
**Solution:**
- Activate virtual environment
- Run `pip install -r requirements.txt`

#### API Key Warnings
```
Warning: Google Maps API key not configured
```
**Solution:**
- This is normal - system works in simulation mode
- Add API keys to .env if you want real data

### Frontend Issues

#### Port Already in Use
```
Error: Port 3000 is already in use
```
**Solution:**
```bash
# Use different port
npm run dev -- -p 3001
```

#### API Connection Error
```
Error: Network Error
```
**Solution:**
- Ensure backend is running on port 8000
- Check NEXT_PUBLIC_API_URL in .env.local
- Verify CORS settings in backend

## 🎯 Usage Flow

### Complete User Journey

1. **Home Page**
   - User lands on homepage
   - Clicks "Start Planning"

2. **Planning Form**
   - Fills multi-step form
   - Provides preferences
   - Submits

3. **Itinerary Generated**
   - Views day-wise plan
   - Sees activities, hotels, transport
   - Reviews budget

4. **Refinement (Optional)**
   - Chats with AI
   - "Reduce budget by 20%"
   - "Add more relaxation"
   - Itinerary updates

5. **Budget Review**
   - Views charts
   - Checks breakdown
   - Confirms budget

6. **Booking**
   - Reviews all bookings
   - Sees flights, hotels, transport
   - Confirms total cost

7. **Payment**
   - Scans QR code
   - Makes payment
   - Confirms

8. **Confirmation**
   - Receives PNRs
   - Gets booking IDs
   - Downloads confirmation

## 📊 API Endpoints Reference

### Itinerary
- `POST /api/itinerary/generate` - Generate itinerary
- `GET /api/itinerary/{id}` - Get itinerary
- `GET /api/itinerary/` - List itineraries
- `DELETE /api/itinerary/{id}` - Delete itinerary

### Refinement
- `POST /api/refinement/refine` - Refine itinerary
- `POST /api/refinement/finalize/{id}` - Finalize

### Booking
- `POST /api/booking/create-summary/{id}` - Create summary
- `POST /api/booking/payment/initiate` - Initiate payment
- `POST /api/booking/payment/verify/{id}` - Verify payment
- `POST /api/booking/confirm/{id}` - Confirm booking
- `GET /api/booking/confirmation/{ref}` - Get confirmation

## 🔐 Security Notes

### Production Deployment

1. **Change SECRET_KEY**
   ```bash
   # Generate secure key
   openssl rand -hex 32
   ```

2. **Use Environment Variables**
   - Never commit .env files
   - Use secrets management

3. **Enable HTTPS**
   - Use SSL certificates
   - Update CORS origins

4. **Secure MongoDB**
   - Use authentication
   - Restrict network access
   - Use MongoDB Atlas

5. **Rate Limiting**
   - Add rate limiting middleware
   - Protect against abuse

## 📈 Performance Tips

### Backend
- Use Redis for caching
- Enable database indexing
- Optimize queries
- Use connection pooling

### Frontend
- Enable Next.js image optimization
- Use dynamic imports
- Implement lazy loading
- Add service worker

## 🐛 Common Issues

### Issue: Slow Itinerary Generation
**Cause:** Large dataset or complex calculations
**Solution:** 
- Reduce dataset size
- Add caching
- Optimize algorithms

### Issue: Payment QR Not Displaying
**Cause:** Missing qrcode library or Razorpay keys
**Solution:**
- Install: `pip install qrcode[pil]`
- System works in simulation mode without keys

### Issue: Frontend Not Connecting to Backend
**Cause:** CORS or wrong API URL
**Solution:**
- Check ALLOWED_ORIGINS in backend .env
- Verify NEXT_PUBLIC_API_URL in frontend .env.local

## 📚 Additional Resources

### Documentation
- FastAPI: https://fastapi.tiangolo.com/
- Next.js: https://nextjs.org/docs
- MongoDB: https://docs.mongodb.com/
- Tailwind CSS: https://tailwindcss.com/docs

### API Documentation
- Google Maps: https://developers.google.com/maps
- OpenWeather: https://openweathermap.org/api
- Razorpay: https://razorpay.com/docs/

## 🎓 Development Tips

### Backend Development
```bash
# Run with auto-reload
uvicorn main:app --reload

# Run tests
pytest

# Format code
black app/

# Type checking
mypy app/
```

### Frontend Development
```bash
# Development mode
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

## 🚢 Deployment

### Backend (Railway/Render/Heroku)
1. Create Procfile
2. Set environment variables
3. Deploy from Git

### Frontend (Vercel/Netlify)
1. Connect Git repository
2. Set environment variables
3. Deploy automatically

### Database (MongoDB Atlas)
1. Create cluster
2. Get connection string
3. Update MONGODB_URL

## 📞 Support

For issues or questions:
1. Check documentation
2. Review error logs
3. Test in simulation mode
4. Verify environment variables

---

**Setup Complete!** 🎉

Your WanderWise application should now be running:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
