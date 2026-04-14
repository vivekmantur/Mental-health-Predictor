from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# API Routes
from app.api.v1.endpoints import phq9

# Database
from app.db.database import engine, Base

# Models (IMPORTANT: ensures table creation)
from app.models.assessment import Assessment


# ---------------------------------------------------------
# Initialize FastAPI Application
# ---------------------------------------------------------
app = FastAPI(title="AI Mental Health Platform")


# ---------------------------------------------------------
# CORS Middleware Configuration
# يسمح للـ frontend بالتواصل مع الـ backend
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow all origins (restrict in production)
    allow_credentials=True,
    allow_methods=["*"],        # Allow all HTTP methods
    allow_headers=["*"],        # Allow all headers
)


# ---------------------------------------------------------
# Create Database Tables
# NOTE: This runs at startup and creates tables if not exist
# ---------------------------------------------------------
Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------
# Register API Routes
# ---------------------------------------------------------
app.include_router(
    phq9.router,
    prefix="/api/v1/phq9",
    tags=["PHQ9"]
)