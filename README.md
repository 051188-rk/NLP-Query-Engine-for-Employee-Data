# NLP Query Engine - Flask + React (Ekam Apps Assignment)

> **Note:** This project is developed as part of the Ekam Apps assignment.

## System Architecture

![System Architecture](https://raw.githubusercontent.com/051188-rk//NLP-Query-Engine-for-Employee-Data/main/frontend/public/ss.png)

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

docker run --name nlp-pg -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=company_db -p 5432:5432 -d postgres:14
# Wait a few seconds, then load sample schema:
psql postgresql://postgres:postgres@localhost:5432/company_db -f backend/sample_data/schema.sql

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

## Technical Details

### Backend Architecture
The backend is built with Flask and implements a modular architecture:

**API Routes:**
- **Schema Discovery** (`schema.py`): Automatically analyzes database structure and relationships
- **Document Ingestion** (`ingestion.py`): Handles file uploads and document processing
- **Query Processing** (`query.py`): Processes natural language queries and returns results

**Core Services:**
- **SchemaDiscovery** (`schema_discovery.py`): Inspects PostgreSQL database schema and generates metadata
- **DocumentProcessor** (`document_processor.py`): Extracts text from PDF/DOCX files, creates embeddings using sentence-transformers
- **QueryEngine** (`query_engine.py`): Orchestrates query processing, handles both SQL and document-based queries

**Key Technologies:**
- **Flask**: Web framework for API endpoints
- **SQLAlchemy**: Database ORM for schema inspection
- **PyPDF/DOCX**: Document text extraction
- **Sentence-Transformers**: Local embedding model (all-MiniLM-L6-v2)
- **Google Generative AI**: Gemini 2.5-Pro for advanced NL-to-SQL conversion
- **FAISS**: In-memory vector similarity search

### Frontend Architecture
The frontend is a React application with the following key components:

- **DatabaseConnector**: Manages database connection settings
- **DocumentUploader**: Handles file upload interface
- **QueryPanel**: Natural language query input and processing
- **ResultsView**: Displays query results and document search results
- **SchemaVisualizer**: Shows database schema structure
- **MetricsDashboard**: Performance monitoring and statistics

**Key Technologies:**
- **React**: Frontend framework
- **Axios**: HTTP client for API communication
- **CSS3**: Custom styling

### Data Flow
1. **Schema Discovery**: Automatically detect database tables and relationships
2. **Document Ingestion**: Upload and process documents into searchable chunks
3. **Query Processing**:
   - Natural language → SQL conversion (via Gemini or heuristics)
   - Document similarity search (via embeddings)
   - Results caching and history tracking

## Gemini Integration
Set `GEMINI_API_KEY` in `.env` to enable Gemini. The backend will use `google-genai` client if installed; otherwise it falls back to a local sentence-transformers model for embeddings and basic NL-to-SQL heuristics.

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
