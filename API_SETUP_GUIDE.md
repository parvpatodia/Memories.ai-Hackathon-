# API Keys & Database Setup Guide

## What You Need to Provide

### 1. **Memories.ai API Key**
**What it is:** AI service for video processing and object detection
**Where to get it:**
1. Visit [https://memories.ai](https://memories.ai)
2. Create an account
3. Go to API settings/dashboard
4. Generate an API key
5. Copy the key

**Add to your `.env` file:**
```bash
MEMORIES_AI_API_KEY=your_memories_ai_api_key_here
```

### 2. **Supabase Database**
**What it is:** PostgreSQL database for storing tracked objects
**Where to get it:**
1. Visit [https://supabase.com](https://supabase.com)
2. Create an account
3. Create a new project
4. Go to Settings > API
5. Copy the URL and anon key

**Add to your `.env` file:**
```bash
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 3. **Database Table Setup**
**Run this SQL in Supabase SQL Editor:**
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

-- Create indexes for better performance
CREATE INDEX idx_tracked_objects_name ON tracked_objects(name);
CREATE INDEX idx_tracked_objects_created_at ON tracked_objects(created_at);
```

## Complete Setup Steps

### Step 1: Create Environment File
Create `.env` file in `/Users/parvpatodia/Desktop/WhereDidI/backend/`:

```bash
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key_here

# Memories.ai Configuration  
MEMORIES_AI_API_KEY=your_memories_ai_api_key_here

# Application Configuration
DEBUG=True
PORT=8000
```

### Step 2: Test Backend
```bash
cd /Users/parvpatodia/Desktop/WhereDidI/backend
source venv/bin/activate
python main.py
```

**Expected output:**
- No warnings about missing API keys
- Server running on http://localhost:8000
- Visit http://localhost:8000/docs for API documentation

### Step 3: Test Frontend
```bash
cd /Users/parvpatodia/Desktop/WhereDidI/frontend
npm start
```

**Expected output:**
- React app running on http://localhost:3000
- File upload component visible
- Can upload video files

## Testing Your Setup

### Backend API Testing:
```bash
# Health check
curl http://localhost:8000/health

# Upload health check
curl http://localhost:8000/api/upload/health
```

### Frontend Testing:
1. Open http://localhost:3000
2. Try uploading a small video file
3. Check browser console for any errors
4. Verify upload success message

## Troubleshooting

### Common Issues:

**1. "API key not found" warnings:**
- This is normal without real API keys
- App will use mock responses for testing

**2. Database connection errors:**
- Check Supabase URL and key are correct
- Ensure database table is created
- Verify Supabase project is active

**3. Upload failures:**
- Check file size (max 50MB)
- Check file type (MP4, AVI, MOV, etc.)
- Check browser console for errors

## What Each Service Does

### Memories.ai
- **Purpose:** AI video processing and object detection
- **Features:** Upload videos, search for objects, get location details
- **Cost:** Check their pricing page
- **Mock Mode:** Works without API key for testing

### Supabase
- **Purpose:** Database for storing tracked objects
- **Features:** PostgreSQL database, real-time updates, API
- **Cost:** Free tier available
- **Required:** Must have valid credentials

## Next Steps After Setup

1. **Test with real API keys** - Get actual responses
2. **Upload test videos** - Try different file types
3. **Test search functionality** - Search for objects in videos
4. **Add more features** - Object management, search UI

## Support

If you need help:
1. Check the console logs for error messages
2. Verify all API keys are correct
3. Ensure database table is created
4. Test with small video files first

Your app is ready to go!
