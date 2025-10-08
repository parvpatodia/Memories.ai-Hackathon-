from fastapi import APIRouter, HTTPException
from database import get_db
from services.memories_api import memories_api
from models import SearchQuery, SearchResult
import re
from typing import Dict, Any

router = APIRouter(prefix="/api/search", tags=["search"])

class SearchEnhancer:
    """Enhance search queries for better results"""
    
    @staticmethod
    def extract_object_name(query: str) -> str:
        """Extract the main object name from natural language query"""
        # Convert "Where are my keys?" -> "keys"
        # Convert "I can't find my wallet" -> "wallet"
        query_lower = query.lower().strip()
        
        # Remove common question words
        query_lower = re.sub(r'\b(where|are|is|my|the|a|an|did|i|put|leave|place)\b', '', query_lower)
        query_lower = re.sub(r'[?!.]+', '', query_lower)  # Remove punctuation
        query_lower = query_lower.strip()
        
        # If we have remaining words, use the first meaningful one
        words = query_lower.split()
        if words:
            return words[0]  # Usually the object name
        
        return query.strip()
    
    @staticmethod
    def enhance_search_query(object_name: str, object_aliases: str) -> str:
        """Create enhanced search query using object aliases"""
        # Combine object name with its aliases for better search
        if object_aliases:
            return f"{object_name} {object_aliases}"
        return object_name
    
    @staticmethod
    def create_location_query(object_name: str) -> str:
        """Create a query for location description"""
        return f"Describe the exact location where you see the {object_name} in this video. Be specific about the surface, room, and nearby objects. Answer in one short sentence."

@router.post("/", response_model=SearchResult)
async def search_for_object(search_query: SearchQuery):
    """
    Search for an object in uploaded videos
    
    - **query**: Natural language search query (e.g., "Where are my keys?")
    
    Returns location information if found, or helpful message if not found
    """
    try:
        if not search_query.query.strip():
            raise HTTPException(status_code=400, detail="Search query cannot be empty")
        
        query = search_query.query.strip()
        print(f"Searching for: {query}")
        
        # Extract object name from natural language query
        object_name = SearchEnhancer.extract_object_name(query)
        print(f"Extracted object: {object_name}")
        
        # Find matching tracked objects
        db = get_db()
        tracked_objects = await db.find_matching_objects(object_name)
        
        if not tracked_objects:
            return SearchResult(
                found=False,
                message=f"'{object_name}' is not being tracked. Please teach this object first in the 'Teach Objects' section."
            )
        
        # Use the first matching object
        tracked_obj = tracked_objects[0]
        print(f"Found tracked object: {tracked_obj.name}")
        
        # Create enhanced search query using object aliases
        enhanced_query = SearchEnhancer.enhance_search_query(tracked_obj.name, tracked_obj.alias)
        print(f"Enhanced query: {enhanced_query}")
        
        # Search in uploaded videos using Memories.ai
        search_results = await memories_api.search_videos(enhanced_query, limit=3)
        
        if not search_results or len(search_results) == 0:
            return SearchResult(
                found=False,
                message=f"No videos found containing '{tracked_obj.name}'. Try uploading more videos of your spaces."
            )
        
        # Get the best result
        best_result = search_results[0]
        print(f"Best result: {best_result}")
        
        # Get detailed location description using video chat
        location_query = SearchEnhancer.create_location_query(tracked_obj.name)
        chat_response = await memories_api.chat_with_video(
            best_result.get("videoNo") or best_result.get("video_no", "unknown"),
            location_query
        )
        
        location_description = chat_response.get("response", "Location details not available")
        confidence = best_result.get("score", best_result.get("confidence", 0.8))
        timestamp = best_result.get("timestamp", best_result.get("time"))
        video_no = best_result.get("videoNo") or best_result.get("video_no")
        
        # Update database with last seen information
        if timestamp and video_no:
            await db.update_object_location(
                object_id=tracked_obj.id,
                video_no=video_no,
                location=location_description,
                confidence=confidence,
                timestamp=timestamp
            )
        
        return SearchResult(
            found=True,
            location=location_description,
            timestamp=timestamp,
            video_no=video_no,
            confidence=confidence,
            object_info=tracked_obj
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Search error: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Search failed. Please try again."
        )

@router.get("/history")
async def get_search_history():
    """Get recently found objects with their locations"""
    try:
        # Get objects that have been found (have location data)
        db = get_db()
        all_objects = await db.get_tracked_objects()
        found_objects = [
            obj for obj in all_objects 
            if obj.last_seen_timestamp and obj.location_phrase
        ]
        
        # Sort by last seen timestamp (most recent first)
        found_objects.sort(
            key=lambda x: x.last_seen_timestamp or 0, 
            reverse=True
        )
        
        return {
            "found_objects": found_objects[:10],  # Limit to 10 most recent
            "total_found": len(found_objects),
            "total_tracked": len(all_objects)
        }
        
    except Exception as e:
        print(f"Error fetching search history: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch search history"
        )

@router.get("/suggestions")
async def get_search_suggestions():
    """Get search query suggestions based on tracked objects"""
    try:
        db = get_db()
        tracked_objects = await db.get_tracked_objects()
        
        suggestions = []
        for obj in tracked_objects:
            suggestions.extend([
                f"Where are my {obj.name}?",
                f"Find my {obj.name}",
                f"I can't find my {obj.name}",
            ])
        
        # Add generic suggestions if no objects are tracked
        if not suggestions:
            suggestions = [
                "Where are my keys?",
                "Find my wallet",
                "Where did I put my phone?",
                "I can't find my glasses",
            ]
        
        return {
            "suggestions": suggestions[:8],  # Limit to 8 suggestions
            "tracked_objects_count": len(tracked_objects)
        }
        
    except Exception as e:
        print(f"Error fetching suggestions: {e}")
        return {"suggestions": [], "tracked_objects_count": 0}
