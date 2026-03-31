from fastapi import FastAPI
from app.api.v1.endpoints import phq9

# ✅ ADD THESE LINES
from app.db.database import engine, Base
from app.models.assessment import Assessment  # 👈 THIS IS CRITICAL
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Mental Health Platform")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ✅ THIS WILL NOW CREATE TABLES
Base.metadata.create_all(bind=engine)

app.include_router(phq9.router, prefix="/api/v1/phq9", tags=["PHQ9"])