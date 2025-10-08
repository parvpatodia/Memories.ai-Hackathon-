# WhereDidI - Object Finder Setup Guide

## Completed Tasks

### 1. Backend Setup 
- **main.py**: FastAPI application with CORS middleware
- **Dependencies**: All required packages installed (fastapi, uvicorn, supabase, etc.)
- **Virtual Environment**: Created and activated
- **Requirements.txt**: Generated with all dependencies

### 2. Frontend Setup 
- **React App**: Created with create-react-app
- **Dependencies**: axios, react-router-dom installed
- **API Service**: Created `src/services/api.js` with health check and upload functions

### 3. Database Setup 
- **Supabase Integration**: Database connection configured
- **Table Schema**: `tracked_objects` table structure defined
- **Environment Variables**: Template created for API keys

## How to Run the Project

### Backend (Terminal 1):
```bash
cd /Users/parvpatodia/Desktop/WhereDidI/backend
source venv/bin/activate
python main.py
```
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Frontend (Terminal 2):
```bash
cd /Users/parvpatodia/Desktop/WhereDidI/frontend
npm start
```
- **React App**: http://localhost:3000

## 🔧 Environment Setup Required

### 1. Supabase Setup:
1. Create account at https://supabase.com
2. Create new project
3. Run this SQL in the SQL editor:
```sql
CREATE TABLE tracked_objects (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  alias TEXT NOT NULL,
  last_seen_timestamp BIGINT,
  location_phrase TEXT,
  video_no TEXT,
  confidence REAL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tracked_objects_name ON tracked_objects(name);
CREATE INDEX idx_tracked_objects_created_at ON tracked_objects(created_at);
```
4. Get API URL and anon key from Settings > API
5. Create `.env` file in backend/ with:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

### 2. Memories.ai Setup:
1. Create account at https://memories.ai
2. Get API key
3. Add to `.env` file:
```
MEMORIES_AI_API_KEY=your_memories_ai_api_key
```

## 📁 Project Structure
```
WhereDidI/
├── backend/
│   ├── main.py              FastAPI app
│   ├── models.py            Pydantic models
│   ├── database.py          Supabase connection
│   ├── requirements.txt     Dependencies
│   ├── venv/                Virtual environment
│   └── .env                 Create with your API keys
├── frontend/
│   ├── src/
│   │   └── services/
│   │       └── api.js       API service
│   └── package.json         Dependencies
└── SETUP_GUIDE.md           This guide
```

## Day 1 Deliverables Status

- Backend server running with FastAPI docs
- React frontend created and ready
- Supabase database schema ready
- All team members can run the project locally
- Need to add API keys to .env file
- Need to test full integration

## Testing Commands

```bash
# Test backend
cd backend && source venv/bin/activate && python main.py
# Visit http://localhost:8000/docs

# Test frontend
cd frontend && npm start
# Visit http://localhost:3000

# Test API connection
curl http://localhost:8000/health
```
