# NhsClinicAssists
# AI Triage & Follow-Up Assistant for NHS Clinics

## Overview
A full-stack assistant to support AI-driven triage and patient follow-up using Azure OpenAI & VectorDB.

## Features
- 📤 Chat with file upload (Flask + SCSS UI)
- 🔌 WebSocket-powered backend (FastAPI)
- 🤖 Azure API inference with secure API key

<img width="1192" alt="Screenshot 2025-05-06 at 1 27 59 AM" src="https://github.com/user-attachments/assets/78df4438-48cb-494f-b13b-da7cd8876eed" />


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
