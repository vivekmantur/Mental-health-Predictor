# AI Mental Health Platform (PHQ-9 Based)

## Overview

This project is a full-stack mental health assessment platform built around the PHQ-9 (Patient Health Questionnaire-9) framework. It combines deterministic clinical scoring with AI-driven insights to provide users with structured mental health evaluations.

The system supports role-based workflows for patients and doctors, including assessment submission, review, trend analysis, and dashboard visualization.

---

## Key Features

### PHQ-9 Assessment Engine

* Standard PHQ-9 questionnaire with 9 responses (0–3 scale)
* Deterministic scoring logic (0–27 total score)
* Severity classification (Minimal to Severe)

### AI-Assisted Insights

* LLM-generated insights based on score, severity, and user notes
* Actionable recommendations tailored to user condition
* Robust fallback handling for LLM failures

### DSM-Based Classification

* Semantic matching using SentenceTransformers
* Maps user notes to:

  * Category
  * Subcategory
  * Disorder
* Uses cosine similarity with threshold filtering

### Role-Based Access Control

* OTP-based authentication (phone + email)
* JWT-based authorization
* User roles:

  * Patient → submit and view assessments
  * Doctor → review and update assessments

### Doctor Workflow

* View patient assessments
* Update:

  * Insight
  * Recommendation
  * Status (pending / success)
  * Doctor notes
* Approval tracking with timestamps

### Trend Analysis

* Compares latest and previous assessments
* Generates AI-based trend insights
* Provides condition progression analysis

### Dashboard APIs

* Latest assessment summary
* Historical assessment data
* Trend insights and recommendations

---

## Architecture

```
Frontend (React)
   |
   | REST API
   v
Backend (FastAPI)
   ├── Auth Layer (OTP + JWT)
   ├── PHQ-9 Service (Scoring + Submission)
   ├── Doctor Service (Review + Updates)
   ├── AI Services (Insight, Recommendation, Trend)
   ├── Embedding Service (DSM Classification)
   |
   ├── Database (PostgreSQL / SQL Server)
   |
   └── LLM (Groq - LLaMA 3.1)
```

---

## Technology Stack

### Backend

* FastAPI
* Python 3.11+
* SQLAlchemy ORM
* Pydantic

### AI & ML

* Groq (LLaMA 3.1 models)
* SentenceTransformers (all-MiniLM-L6-v2)
* Cosine similarity (scikit-learn)

### Frontend

* React.js
* Axios
* Recharts (for visualization)

### Infrastructure

* Docker
* Docker Compose

---

## API Endpoints

### Authentication

* `POST /api/v1/auth/request-otp`
* `POST /api/v1/auth/verify-otp`
* `POST /api/v1/auth/register-otp`
* `POST /api/v1/auth/register`

### PHQ-9

* `POST /api/v1/phq9/submit`
* `GET /api/v1/phq9/my-assessments`
* `GET /api/v1/phq9/trend-analysis`
* `GET /api/v1/phq9/dashboard`

### Doctor

* `GET /api/v1/doctor/patients`
* `GET /api/v1/doctor/assessments`
* `PUT /api/v1/doctor/assessments/{id}`
* `PUT /api/v1/doctor/assessments/{id}/status`

---

## Sample Request

### Submit Assessment

```
POST /api/v1/phq9/submit
```

```json
{
  "answers": [0, 1, 2, 3, 1, 0, 2, 1, 0],
  "notes": "Feeling low and having trouble sleeping"
}
```

### Sample Response

```json
{
  "score": 10,
  "severity": "Moderate",
  "status": "pending"
}
```

---

## Scoring Logic

PHQ-9 scoring is implemented using deterministic logic:

| Score Range | Severity          |
| ----------- | ----------------- |
| 0           | None              |
| 1–4         | Minimal           |
| 5–9         | Mild              |
| 10–14       | Moderate          |
| 15–19       | Moderately Severe |
| 20–27       | Severe            |

---

## Project Structure

```
backend/
│
├── api/                # FastAPI routers
├── auth/               # JWT, OTP handling
├── db/                 # Database configuration
├── models/             # ORM models
├── repositories/       # DB operations
├── services/           # Business logic (AI, scoring, trend)
├── schemas/            # Request/response models
└── main.py             # Application entry point

frontend/
│
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   └── styles/
```

---

## Installation

### Using Docker

```
docker-compose up --build
```

### Manual Setup

#### Backend

```
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend

```
cd frontend
npm install
npm start
```

---

## Configuration

Create a `.env` file in the backend:

```
GROQ_API_KEY=your_api_key
OTP_EXPIRE_SECONDS=300
```

---

## Design Principles

* Deterministic scoring separated from AI logic
* Fail-safe handling for LLM outputs
* Layered architecture (router → service → repository)
* Role-based access control
* Modular and extensible service design

---

## Future Improvements

* Database migrations (Alembic)
* Async processing for LLM calls
* Caching for embeddings and model responses
* Deployment to cloud platforms (Azure / AWS)
* Enhanced analytics dashboard

---

## License

MIT License
