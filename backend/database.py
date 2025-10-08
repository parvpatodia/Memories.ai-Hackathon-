from supabase import create_client, Client
import os
from typing import List, Optional, Dict, Any
from models import TrackedObject, TrackedObjectCreate
from dotenv import load_dotenv
import asyncio
from datetime import datetime

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_ANON_KEY")
        
        if not self.url or not self.key:
            raise ValueError("Supabase credentials not found in environment variables")
        
        self.client: Client = create_client(self.url, self.key)
    
    async def create_tracked_object(self, obj: TrackedObjectCreate) -> TrackedObject:
        """Create a new tracked object"""
        try:
            # Check if object already exists
            existing = self.client.table("tracked_objects")\
                .select("*")\
                .eq("name", obj.name.lower())\
                .execute()
            
            if existing.data:
                raise ValueError(f"Object '{obj.name}' already exists")
            
            # Insert new object
            result = self.client.table("tracked_objects")\
                .insert({
                    "name": obj.name.lower(),
                    "alias": obj.alias
                })\
                .execute()
            
            if result.data:
                return TrackedObject(**result.data[0])
            else:
                raise Exception("Failed to create object")
                
        except Exception as e:
            print(f"Database error creating object: {e}")
            raise
    
    async def get_tracked_objects(self) -> List[TrackedObject]:
        """Get all tracked objects"""
        try:
            result = self.client.table("tracked_objects")\
                .select("*")\
                .order("created_at", desc=True)\
                .execute()
            
            return [TrackedObject(**obj) for obj in result.data]
            
        except Exception as e:
            print(f"Database error fetching objects: {e}")
            return []
    
    async def find_matching_objects(self, query: str) -> List[TrackedObject]:
        """Find objects that match the search query"""
        try:
            # Search in both name and alias fields
            result = self.client.table("tracked_objects")\
                .select("*")\
                .or_(f"name.ilike.%{query}%,alias.ilike.%{query}%")\
                .execute()
            
            return [TrackedObject(**obj) for obj in result.data]
            
        except Exception as e:
            print(f"Database error searching objects: {e}")
            return []
    
    async def update_object_location(self, object_id: int, video_no: str, 
                                   location: str, confidence: float, 
                                   timestamp: int) -> bool:
        """Update object's last seen location"""
        try:
            result = self.client.table("tracked_objects")\
                .update({
                    "last_seen_timestamp": timestamp,
                    "location_phrase": location,
                    "video_no": video_no,
                    "confidence": confidence
                })\
                .eq("id", object_id)\
                .execute()
            
            return len(result.data) > 0
            
        except Exception as e:
            print(f"Database error updating location: {e}")
            return False
    
    async def delete_tracked_object(self, object_id: int) -> bool:
        """Delete a tracked object"""
        try:
            result = self.client.table("tracked_objects")\
                .delete()\
                .eq("id", object_id)\
                .execute()
            
            return len(result.data) > 0
            
        except Exception as e:
            print(f"Database error deleting object: {e}")
            return False

# Global database instance (will be created when needed)
db = None

def get_db():
    global db
    if db is None:
        db = DatabaseManager()
    return db