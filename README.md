# Mental Health Predictor (PHQ-9 AI Powered)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.x-61DAFB?style=flat&logo=react&logoColor=white)](https://reactjs.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com)

> **A full-stack AI-powered web application that evaluates user responses using the PHQ-9 framework, generates structured scores, and presents complete mental health reports with visual dashboards.**

**Version:** 1.0.0  

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Method 1: Docker (Recommended)](#method-1-docker-recommended)
  - [Method 2: Manual Setup](#method-2-manual-setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Scoring & Logic Detail](#scoring--logic-detail)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## Overview

The **Mental Health Predictor** is an AI-powered solution designed to evaluate user inputs against the PHQ-9 depression screening framework. By combining traditional clinical scoring logic with large language models, the application accurately infers severity levels from free-text inputs, especially identifying critical behavioral insights (such as self-harm). It surfaces these findings through a stunning glassmorphism interface, providing users with immediate actionable recommendations.

---

## Key Features

### Comprehensive Assessment
* Structured PHQ-9 questionnaire format (9 questions).
* Rich text input support, enabling expressive, unstructured user narratives.
* Mandatory validation for all responses to ensure complete data context.

### AI Scoring Engine
* Translates free-text answers into deterministic PHQ-9 scores (0–3) using a prompt-engineered LLM.
* Recognizes both **explicit frequency keywords** and draws **contextual inferences** when clear keywords are missing.
* Critical safety rule: Mentions of self-harm automatically trigger a minimum Q9 score of 1.

### Results Dashboard
* **Score & Severity:** Provides a total score (0–27) mapped directly to severity brackets (Minimal to Severe) with a visual progress bar.
* **Radar Chart:** Maps five dimensions of well-being: Mood, Energy, Sleep, Focus, and Self-worth.
* **Bar Chart:** Illustrates the intensity of individual problem areas for easy interpretation.

### Actionable Insights
* AI-generated summaries interpreting the user's emotional state and behavioral patterns.
* Tailored "What You Can Do" section featuring lifestyle improvements, journaling cues, exercise guidance, and professional help resources.

---

## Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React UI)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Assessment   │  │   Dashboard  │  │   Insights   │     │
│  │    Form      │  │ (Recharts)   │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API
┌────────────────────────┴────────────────────────────────────┐
│                   Backend (FastAPI)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ API Endpoints│  │ Scoring Logic│  │ Request Val. │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────┬───────────────────────────────┬────────────────────┘
         │                               │
    ┌────┴────┐                     ┌────┴────┐
    │ Database│                     │   LLM   │
    │(Options)│                     │(120b)   │
    └─────────┘                     └─────────┘
```

---

## Technology Stack

### Backend Support
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **AI Integration**: Custom LLM integration (e.g., openai/gpt-oss-120b)

### Frontend Support
- **Framework**: React.js, React Router
- **Visualization**: Recharts (Radar + Bar charts)
- **Editor Integration**: react-simple-wysiwyg
- **HTTP Client**: Axios
- **Design System**: Vanilla CSS / Glassmorphism layouts

### DevOps & Infrastructure
- **Containerization**: Docker, Docker Compose

---

## Prerequisites

Before you start, ensure you have the following installed:

- **Docker Desktop** (For containerized deployment)
- **Node.js** v16+ (If running frontend manually)
- **Python** 3.11+ (If running backend manually)
- An active connection/access key for your intended LLM (e.g. `gpt-oss-120b`) if self-hosting the model is not done locally.

---

## Installation

### Method 1: Docker (Recommended)

The quickest way to bring the entire stack online.

```bash
# 1. Clone the repository
git clone https://github.com/your-org/mental-health-predictor.git
cd mental-health-predictor

# 2. Build and run containers
docker-compose up --build
```
- Frontend → http://localhost:3000
- Backend → http://localhost:8000

---

### Method 2: Manual Setup

#### Step 1: Start the Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the API server
uvicorn main:app --reload
```

#### Step 2: Start the Frontend

```bash
cd mental-health-ui

# Install Node dependencies
npm install

# Start the dev server
npm start
```

---

## Configuration

Basic configurations can be set via `.env` files in your backend directory:

```env
# Backend .env
LLM_MODEL=openai/gpt-oss-120b
LLM_TEMPERATURE=0
API_V1_STR=/api/v1
CORS_ORIGINS=["http://localhost:3000"]
```

---

## Usage

1. **Self-Assessment**: Open the frontend (http://localhost:3000). Fill out the 9 prompted responses. You can use rich text descriptions if needed.
2. **Analysis**: Hit 'Submit'. The request is passed to the FastAPI backend, which sequences prompts to the LLM. 
3. **Review**: The system will display your **Severity Label**, generate a **Radar Chart**, provide **Written Insights**, and give you a comprehensive **Action Plan**.

---

## API Documentation

Once running, interactive API docs are available automatically via FastAPI:
- **Swagger UI:** `http://localhost:8000/docs`

### Submit Assessment

**Endpoint:** `POST /api/v1/phq9/submit`

**Sample Request Payload:**
```json
{
  "user_id": "user_ai_1",
  "answers_text": [
    "I've been feeling quite low lately...",
    "Sleeping has been very difficult."
  ]
}
```

**Sample Response payload:**
```json
{
  "score": 8,
  "severity": "Mild",
  "radar_data": {
    "Mood": 2,
    "Energy": 1,
    "Sleep": 1,
    "Focus": 1,
    "Self-worth": 1
  },
  "bar_data": [...],
  "insights": [...],
  "recommendations": [...]
}
```

---

## Project Structure

```text
MENTAL-HEALTH-PREDICTOR/
│
├── backend/                # FastAPI application
│   ├── main.py             # App entry point
│   ├── api/                # API router components
│   ├── ai/                 # LLM connection & custom scoring logic
│   └── requirements.txt    # Python dependencies
│
├── mental-health-ui/       # React application frontend
│   ├── src/                # Components and layout
│   ├── public/             # Static web assets
│   └── package.json        
│
├── docs/                   # Additional documentation
├── infra/                  # Specific deployment configurations
│
├── docker-compose.yml      # Orchestration config
└── Dockerfile              # Setup images
```

---

## Scoring & Logic Detail

### Baseline Clinical Scoring
| Score Range | Severity Status   |
| ----------- | ----------------- |
| 0–4         | Minimal           |
| 5–9         | Mild              |
| 10–14       | Moderate          |
| 15–19       | Moderately Severe |
| 20–27       | Severe            |

### LLM Prompt Evaluation Matrix
When evaluating user responses, the LLM forces an integer output adhering to:
* **0** → Not at all
* **1** → Several days
* **2** → More than half the days
* **3** → Nearly every day

### Critical Catch Rule
**Any user mention of self-harm in `Q9` overrides normal logic and automatically assigns a minimum score of 1** for that specific subset, ensuring no self-harm signals are overlooked.

---

## Future Enhancements

* **User Authentication**: Implement JWT flows to store data privately per user.
* **Historical Tracking**: Enable users to view a timeline dashboard of how their scores change over weeks or months.
* **Interactive AI Chatbot**: Add responsive support agents that navigate difficult emotional responses in real-time.
* **Azure Deployment**: Move container configurations to Azure App Service / AKS.
* **Fine-Tuned Modeling**: Train a specific PHQ-9 specialized lightweight model to replace massive general-purpose arrays constraints.

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.
