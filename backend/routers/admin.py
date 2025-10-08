from fastapi import APIRouter, Depends
from utils.performance import perf_monitor, search_cache
from typing import Dict, Any
import time

router = APIRouter(prefix="/api/admin", tags=["admin"])

# Store app start time for uptime calculation
app_start_time = time.time()

@router.get("/metrics")
async def get_performance_metrics() -> Dict[str, Any]:
    """Get performance metrics for monitoring"""
    return {
        "performance_metrics": perf_monitor.get_metrics(),
        "cache_stats": {
            "search_cache_size": len(search_cache.cache),
            "search_cache_max_size": search_cache.max_size,
            "search_cache_ttl": search_cache.ttl_seconds
        },
        "system_info": {
            "timestamp": time.time(),
            "uptime_seconds": time.time() - app_start_time
        }
    }

@router.post("/cache/clear")
async def clear_cache():
    """Clear all caches"""
    search_cache.clear()
    return {"message": "Cache cleared successfully"}

@router.post("/metrics/reset")
async def reset_metrics():
    """Reset performance metrics"""
    perf_monitor.reset_metrics()
    return {"message": "Metrics reset successfully"}
