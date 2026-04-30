"""
Main Application Entry Point

Initializes FastAPI app and configures:
- API routes (Auth, PHQ-9, Doctor)
- CORS middleware
- Database table creation

Design Notes:
- Acts as the central bootstrap for the backend
- Registers all routers under versioned API paths
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# API Routes
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import phq9
from app.api.v1.endpoints import doctor

# Database
from app.db.database import engine, Base

# Models (IMPORTANT: ensures table creation)
from app.models.assessment import Assessment


# ---------------------------------------------------------
# Initialize FastAPI Application
# ---------------------------------------------------------
app = FastAPI(title="AI Mental Health Platform")


# ---------------------------------------------------------
# Register API Routes
# ---------------------------------------------------------
# Auth routes (login, registration)
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["Auth"]
)

# PHQ-9 routes (submission, dashboard, trends)
app.include_router(
    phq9.router,
    prefix="/api/v1/phq9",
    tags=["PHQ9"]
)

# Doctor routes (review, update, patient management)
app.include_router(
    doctor.router,
    prefix="/api/v1/doctor",
    tags=["Doctor"]
)


# ---------------------------------------------------------
# CORS Middleware Configuration
# ---------------------------------------------------------
# Allows frontend (React) to communicate with backend

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # ⚠️ Allow all origins (restrict in production)
    allow_credentials=True,
    allow_methods=["*"],        # Allow all HTTP methods
    allow_headers=["*"],        # Allow all headers
)


# ---------------------------------------------------------
# Database Initialization
# ---------------------------------------------------------
# Creates tables automatically if they do not exist
# Runs at application startup

Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------
# ⚠️ Duplicate Router Registration (Retained as-is)
# ---------------------------------------------------------
# NOTE:
# PHQ-9 router is already registered above.
# This duplication may lead to:
# - Duplicate route exposure
# - Confusion in API docs (Swagger)

app.include_router(
    phq9.router,
    prefix="/api/v1/phq9",
    tags=["PHQ9"]
)