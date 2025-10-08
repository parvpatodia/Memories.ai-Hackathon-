import asyncio
import time
from functools import wraps
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
    
    def time_function(self, func_name: str):
        """Decorator to time function execution"""
        def decorator(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    self._record_metric(func_name, execution_time, 'success')
                    logger.info(f"⚡ {func_name} completed in {execution_time:.2f}s")
                    return result
                except Exception as e:
                    execution_time = time.time() - start_time
                    self._record_metric(func_name, execution_time, 'error')
                    logger.error(f"❌ {func_name} failed after {execution_time:.2f}s: {str(e)}")
                    raise
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    self._record_metric(func_name, execution_time, 'success')
                    logger.info(f"⚡ {func_name} completed in {execution_time:.2f}s")
                    return result
                except Exception as e:
                    execution_time = time.time() - start_time
                    self._record_metric(func_name, execution_time, 'error')
                    logger.error(f"❌ {func_name} failed after {execution_time:.2f}s: {str(e)}")
                    raise
            
            return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        return decorator
    
    def _record_metric(self, func_name: str, execution_time: float, status: str):
        """Record performance metric"""
        if func_name not in self.metrics:
            self.metrics[func_name] = {
                'calls': 0,
                'total_time': 0,
                'avg_time': 0,
                'min_time': float('inf'),
                'max_time': 0,
                'success_count': 0,
                'error_count': 0
            }
        
        metric = self.metrics[func_name]
        metric['calls'] += 1
        metric['total_time'] += execution_time
        metric['avg_time'] = metric['total_time'] / metric['calls']
        metric['min_time'] = min(metric['min_time'], execution_time)
        metric['max_time'] = max(metric['max_time'], execution_time)
        
        if status == 'success':
            metric['success_count'] += 1
        else:
            metric['error_count'] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        return self.metrics
    
    def reset_metrics(self):
        """Reset all metrics"""
        self.metrics = {}

# Global performance monitor
perf_monitor = PerformanceMonitor()

# Enhanced caching system
class SimpleCache:
    def __init__(self, max_size: int = 100, ttl_seconds: int = 300):
        self.cache = {}
        self.timestamps = {}
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
    
    def get(self, key: str) -> Any:
        """Get item from cache"""
        if key not in self.cache:
            return None
        
        # Check if expired
        if time.time() - self.timestamps[key] > self.ttl_seconds:
            del self.cache[key]
            del self.timestamps[key]
            return None
        
        return self.cache[key]
    
    def set(self, key: str, value: Any):
        """Set item in cache"""
        # Remove oldest items if cache is full
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.timestamps.keys(), key=self.timestamps.get)
            del self.cache[oldest_key]
            del self.timestamps[oldest_key]
        
        self.cache[key] = value
        self.timestamps[key] = time.time()
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
        self.timestamps.clear()

# Global cache instance
search_cache = SimpleCache(max_size=50, ttl_seconds=600)  # 10 minute TTL