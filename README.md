# NhsClinicAssists
# AI Triage & Follow-Up Assistant for NHS Clinics

## Overview
A full-stack assistant to support AI-driven triage and patient follow-up using Azure OpenAI & VectorDB.

## Features
- 📤 Chat with file upload (Flask + SCSS UI)
- 🔌 WebSocket-powered backend (FastAPI)
- 🤖 Azure API inference with secure API key

## Setup

### 1. Frontend (Flask)
```bash
cd frontend
pip install -r ../requirements.txt
python app.py

####2. Backend FASTApi
cd backend
export AZURE_API_KEY=your_api_key
uvicorn main:app --reload
