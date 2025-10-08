import aiohttp
import os
from typing import Dict, Any, List
from fastapi import UploadFile
import asyncio
import json
from datetime import datetime
from utils.performance import perf_monitor, search_cache
import logging

logger = logging.getLogger(__name__)

class MemoriesAPIClient:
    def __init__(self):
        self.api_key = os.getenv("MEMORIES_AI_API_KEY")
        self.base_url = "https://mavi-backend.memories.ai/api/serve"
        self.timeout = aiohttp.ClientTimeout(total=300)  # 5 minute timeout
        
        if not self.api_key:
            print("⚠️  WARNING: MEMORIES_AI_API_KEY not found. Using mock responses.")

    @perf_monitor.time_function("memories_api_upload")
    async def upload_video(self, file: UploadFile) -> Dict[str, Any]:
        """Upload video to Memories.ai API"""
        try:
            if not self.api_key:
                return self._mock_upload_response(file)
            
            # Read file content
            file_content = await file.read()
            
            # Reset file position for potential re-use
            await file.seek(0)
            
            # Prepare multipart form data
            data = aiohttp.FormData()
            data.add_field('file', 
                          file_content, 
                          filename=file.filename,
                          content_type=file.content_type)
            
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(
                    f"{self.base_url}/video/upload",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    data=data
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "video_no": result.get("videoNo") or result.get("id") or f"video_{int(datetime.now().timestamp())}",
                            "status": result.get("status", "processing"),
                            "message": "Upload successful"
                        }
                    else:
                        error_text = await response.text()
                        print(f"Memories.ai API Error: {response.status} - {error_text}")
                        return self._mock_upload_response(file)
                        
        except asyncio.TimeoutError:
            print("Upload timeout - using mock response")
            return self._mock_upload_response(file)
        except Exception as e:
            print(f"Upload error: {e}")
            return self._mock_upload_response(file)
    
    @perf_monitor.time_function("memories_api_search")
    async def search_videos(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for objects in uploaded videos"""
        cache_key = f"search_{query}_{limit}"
        cached_result = search_cache.get(cache_key)
        if cached_result:
            logger.info(f"🎯 Cache hit for search: {query}")
            return cached_result

        try:
            if not self.api_key:
                return self._mock_search_response(query)
            
            payload = {
                "query": query,
                "limit": limit
            }
            
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(
                    f"{self.base_url}/video/searchAI",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                ) as response:
                    
                    if response.status == 200:
                        results = await response.json()
                        return results if isinstance(results, list) else []
                    else:
                        error_text = await response.text()
                        print(f"Search API Error: {response.status} - {error_text}")
                        return self._mock_search_response(query)
               
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    @perf_monitor.time_function("memories_api_chat")
    async def chat_with_video(self, video_no: str, query: str) -> Dict[str, Any]:
        """Get detailed information about video content"""
        try:
            if not self.api_key:
                return self._mock_chat_response(video_no, query)
            
            payload = {
                "videoNos": [video_no],
                "query": query
            }
            
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(
                    f"{self.base_url}/video/chat",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "response": result.get("response") or result.get("answer", "Location details not available")
                        }
                    else:
                        error_text = await response.text()
                        print(f"Chat API Error: {response.status} - {error_text}")
                        return self._mock_chat_response(video_no, query)
                        
        except Exception as e:
            print(f"Chat error: {e}")
            return self._mock_chat_response(video_no, query)
    
    def _mock_upload_response(self, file: UploadFile) -> Dict[str, Any]:
        """Mock response for development/testing"""
        timestamp = int(datetime.now().timestamp())
        return {
            "video_no": f"mock_{timestamp}_{file.filename}",
            "status": "processing",
            "message": "Mock upload successful (API key not configured)"
        }
    
    def _mock_search_response(self, query: str) -> List[Dict[str, Any]]:
        """Mock search response for development/testing"""
        locations = [
            "on the kitchen counter next to the coffee maker",
            "on the desk beside the computer monitor", 
            "on the nightstand next to the lamp",
            "on the dining table near the fruit bowl",
            "on the bookshelf between the novels"
        ]
        
        return [{
            "videoNo": f"mock_video_{int(datetime.now().timestamp())}",
            "timestamp": int(datetime.now().timestamp() * 1000) - 3600000,  # 1 hour ago
            "score": 0.92,
            "snippet": f"Mock search result for '{query}'"
        }]
    
    def _mock_chat_response(self, video_no: str, query: str) -> Dict[str, Any]:
        """Mock chat response for development/testing"""
        locations = [
            "on the kitchen counter next to the coffee maker",
            "on the wooden desk beside the computer monitor",
            "on the bedside nightstand next to the reading lamp", 
            "on the dining room table near the fruit bowl",
            "on the living room coffee table next to the remote control"
        ]
        
        import random
        return {
            "response": random.choice(locations)
        }

# Global API client instance
memories_api = MemoriesAPIClient()
