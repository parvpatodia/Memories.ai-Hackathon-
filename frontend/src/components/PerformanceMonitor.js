import React, { useState, useEffect } from 'react';

const PerformanceMonitor = () => {
  const [metrics, setMetrics] = useState(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    // Show performance monitor in development
    if (process.env.NODE_ENV === 'development') {
      const fetchMetrics = async () => {
        try {
          const response = await fetch('http://localhost:8000/api/admin/metrics');
          const data = await response.json();
          setMetrics(data);
        } catch (error) {
          console.error('Failed to fetch metrics:', error);
        }
      };

      const interval = setInterval(fetchMetrics, 10000); // Update every 10 seconds
      return () => clearInterval(interval);
    }
  }, []);

  if (process.env.NODE_ENV !== 'development' || !metrics) {
    return null;
  }

  return (
    <div style={{
      position: 'fixed',
      bottom: '20px',
      right: '20px',
      zIndex: 1000
    }}>
      <button
        onClick={() => setVisible(!visible)}
        style={{
          padding: '10px',
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '50%',
          width: '50px',
          height: '50px',
          cursor: 'pointer',
          fontSize: '16px'
        }}
      >
        📊
      </button>
      
      {visible && (
        <div style={{
          position: 'absolute',
          bottom: '60px',
          right: '0',
          width: '400px',
          maxHeight: '500px',
          overflowY: 'auto',
          backgroundColor: 'white',
          border: '1px solid #ddd',
          borderRadius: '8px',
          padding: '15px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
          fontSize: '12px'
        }}>
          <h4>Performance Metrics</h4>
          
          <div style={{ marginBottom: '15px' }}>
            <strong>Cache Stats:</strong>
            <div>Search Cache: {metrics.cache_stats.search_cache_size}/{metrics.cache_stats.search_cache_max_size}</div>
            <div>TTL: {metrics.cache_stats.search_cache_ttl}s</div>
          </div>
          
          <div>
            <strong>API Performance:</strong>
            {Object.entries(metrics.performance_metrics).map(([func, stats]) => (
              <div key={func} style={{ marginBottom: '10px', padding: '8px', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
                <div style={{ fontWeight: 'bold' }}>{func}</div>
                <div>Calls: {stats.calls} | Avg: {stats.avg_time.toFixed(2)}s</div>
                <div>Min: {stats.min_time.toFixed(2)}s | Max: {stats.max_time.toFixed(2)}s</div>
                <div>Success: {stats.success_count} | Errors: {stats.error_count}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default PerformanceMonitor;
