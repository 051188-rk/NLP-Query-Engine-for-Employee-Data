# NLP Query Engine - Flask + React (Ekam Apps Assignment)

> **Note:** This project is developed as part of the Ekam Apps assignment.

## Overview
This project implements a demo NLP Query Engine for employee data:
- **Backend:** Flask (Python 3.8+)
- **Frontend:** React with plain CSS
- **Database:** PostgreSQL (demo SQL included)
- **LLM:** Google Gemini 2.5-Pro (integration points provided; requires API key)

This repository is packaged as a single ZIP that contains:
- `backend/` — Flask application with API endpoints
- `frontend/` — React application (create-react-app style)
- `.env.example` — example environment variables
- `README.md` — this file

> NOTE: Gemini usage requires a valid API key and network access. This project provides a safe fallback using open-source sentence-transformers if Gemini is not configured.

## Quickstart (Local, recommended)

### Prerequisites
- Python 3.8+
- Node 16+
- Docker (optional, recommended for PostgreSQL)
- Internet access to call Gemini (optional)

### 1. Start PostgreSQL (Docker)
```bash
docker run --name nlp-pg -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=company_db -p 5432:5432 -d postgres:14
# Wait a few seconds, then load sample schema:
psql postgresql://postgres:postgres@localhost:5432/company_db -f backend/sample_data/schema.sql
```

### 2. Backend setup
```bash
cd backend
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env to set DB connection and GEMINI_API_KEY if available
export FLASK_APP=main.py
flask run
# or: gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

### 3. Frontend setup
```bash
cd frontend
npm install
cp .env.example .env
npm start
# Open http://localhost:3000
```

## Files of interest
- `backend/main.py` - Flask app initialization
- `backend/api/routes/ingestion.py` - upload & ingestion endpoints
- `backend/api/routes/schema.py` - connect & schema discovery
- `backend/api/routes/query.py` - query endpoint
- `backend/services/schema_discovery.py` - logic for schema inspection
- `backend/services/document_processor.py` - document extraction and chunking
- `backend/services/query_engine.py` - NLP-to-SQL and retrieval orchestration
- `frontend/src/components/DatabaseConnector.js` - DB connection UI
- `frontend/src/components/DocumentUploader.js` - upload UI
- `frontend/src/components/QueryPanel.js` - query UI
- `frontend/src/components/ResultsView.js` - results display

## Gemini Integration
Set `GEMINI_API_KEY` in `.env` to enable Gemini. The backend will use `google-genai` client if installed; otherwise it falls back to a local sentence-transformers model for embeddings and basic NL-to-SQL heuristics.

## Limitations & Notes
- This is a functional demo tailored for the assignment. It includes sample schemas and a simple in-memory vector store (FAISS is not bundled).
- The assignment requires no authentication; for production you should add auth and secure database credentials.
- For large-scale production, replace the simple caching and in-memory stores with Redis and a proper vector DB.

