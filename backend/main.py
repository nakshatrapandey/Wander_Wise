"""
WanderWise Backend - Main Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.api import itinerary, refinement, booking, destinations, ml_predict


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    await connect_to_mongo()
    print("✅ Connected to MongoDB")
    yield
    # Shutdown
    await close_mongo_connection()
    print("❌ Closed MongoDB connection")


# Initialize FastAPI app
app = FastAPI(
    title="WanderWise API",
    description="Smart Adaptive AI Travel Planner API",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "WanderWise API is running",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Include routers
app.include_router(itinerary.router, prefix="/api/itinerary", tags=["Itinerary"])
app.include_router(refinement.router, prefix="/api/refinement", tags=["Refinement"])
app.include_router(booking.router, prefix="/api/booking", tags=["Booking"])
app.include_router(destinations.router, prefix="/api/destinations", tags=["Destinations"])
app.include_router(ml_predict.router, prefix="/api/ml", tags=["Machine Learning"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# .
