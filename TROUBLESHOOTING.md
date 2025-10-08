# Troubleshooting Guide

## Port Already in Use Error

### Problem
When you see "Address already in use" error, it means there's already a server running on that port.

### Solution

#### 1. Check what's running on the ports:
```bash
# Check port 8000 (backend)
lsof -ti:8000

# Check port 3000 (frontend)
lsof -ti:3000
```

#### 2. Kill the processes:
```bash
# Kill backend processes
kill -9 $(lsof -ti:8000)

# Kill frontend processes  
kill -9 $(lsof -ti:3000)
```

#### 3. Restart the servers:
```bash
# Backend
cd /Users/parvpatodia/Desktop/WhereDidI/backend
source venv/bin/activate
python main.py

# Frontend (in a new terminal)
cd /Users/parvpatodia/Desktop/WhereDidI/frontend
npm start
```

## Quick Commands

### Stop all servers:
```bash
# Kill all processes on ports 8000 and 3000
kill -9 $(lsof -ti:8000) 2>/dev/null
kill -9 $(lsof -ti:3000) 2>/dev/null
```

### Start servers properly:
```bash
# Terminal 1 - Backend
cd /Users/parvpatodia/Desktop/WhereDidI/backend
source venv/bin/activate
python main.py

# Terminal 2 - Frontend
cd /Users/parvpatodia/Desktop/WhereDidI/frontend
npm start
```

### Check if servers are running:
```bash
# Check backend
curl http://localhost:8000/health

# Check frontend
curl http://localhost:3000
```

## Current Status

Both servers are now running:
- **Backend**: http://localhost:8000 (API docs at /docs)
- **Frontend**: http://localhost:3000

You can now:
1. Visit http://localhost:3000 to use the app
2. Visit http://localhost:8000/docs to test the API
3. Upload videos and teach objects about what to track
