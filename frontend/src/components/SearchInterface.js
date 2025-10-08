import React, { useState, useEffect } from 'react';
import api from '../services/api';

const SearchInterface = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searching, setSearching] = useState(false);
  const [result, setResult] = useState(null);
  const [searchHistory, setSearchHistory] = useState([]);
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    fetchSuggestions();
    fetchSearchHistory();
  }, []);

  const fetchSuggestions = async () => {
    try {
      const response = await api.get('/api/search/suggestions');
      setSuggestions(response.data.suggestions);
    } catch (error) {
      console.error('Failed to fetch suggestions:', error);
    }
  };

  const fetchSearchHistory = async () => {
    try {
      const response = await api.get('/api/search/history');
      setSearchHistory(response.data.found_objects);
    } catch (error) {
      console.error('Failed to fetch search history:', error);
    }
  };

  const handleSearch = async (query = searchQuery) => {
    if (!query?.trim()) return;

    setSearching(true);
    setResult(null);

    try {
      const response = await api.post('/api/search/', {
        query: query.trim()
      });

      setResult(response.data);
      
      // Refresh search history if object was found
      if (response.data.found) {
        setTimeout(fetchSearchHistory, 1000);
      }

    } catch (error) {
      console.error('Search failed:', error);
      setResult({
        found: false,
        message: error.response?.data?.detail || 'Search failed. Please try again.'
      });
    } finally {
      setSearching(false);
    }
  };

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return 'Recently';
    
    const now = Date.now();
    const diff = now - timestamp;
    const minutes = Math.floor(diff / (1000 * 60));
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    
    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    if (hours < 24) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    return `${days} day${days > 1 ? 's' : ''} ago`;
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return '#28a745'; // Green
    if (confidence >= 0.6) return '#ffc107'; // Yellow
    return '#dc3545'; // Red
  };

  const getConfidenceText = (confidence) => {
    if (confidence >= 0.9) return 'Very Confident';
    if (confidence >= 0.7) return 'Confident';
    if (confidence >= 0.5) return 'Somewhat Confident';
    return 'Low Confidence';
  };

  return (
    <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
      <h3>Find Objects</h3>
      <p style={{ color: '#666', fontSize: '14px', marginBottom: '20px' }}>
        Ask where your objects are using natural language
      </p>

      {/* Search Input */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <input
          type="text"
          placeholder="Where are my keys?"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && !searching && handleSearch()}
          style={{
            flex: 1,
            padding: '12px',
            border: '1px solid #ddd',
            borderRadius: '6px',
            fontSize: '16px',
            outline: 'none'
          }}
          onFocus={(e) => e.target.style.borderColor = '#007bff'}
          onBlur={(e) => e.target.style.borderColor = '#ddd'}
        />
        <button
          onClick={() => handleSearch()}
          disabled={searching || !searchQuery.trim()}
          style={{
            padding: '12px 20px',
            backgroundColor: searching ? '#ccc' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: searching ? 'not-allowed' : 'pointer',
            fontSize: '16px',
            fontWeight: '600',
            minWidth: '100px'
          }}
        >
          {searching ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
              <div 
                style={{
                  width: '16px',
                  height: '16px',
                  border: '2px solid #ffffff40',
                  borderTop: '2px solid #ffffff',
                  borderRadius: '50%',
                  animation: 'spin 1s linear infinite'
                }}
              />
              Searching...
            </div>
          ) : (
            'Find It!'
          )}
        </button>
      </div>

      {/* Quick Search Suggestions */}
      {suggestions.length > 0 && (
        <div style={{ marginBottom: '20px' }}>
          <h4 style={{ fontSize: '14px', fontWeight: '600', marginBottom: '10px', color: '#666' }}>
            Quick Searches:
          </h4>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
            {suggestions.slice(0, 4).map((suggestion, index) => (
              <button
                key={index}
                onClick={() => handleSearch(suggestion)}
                disabled={searching}
                style={{
                  padding: '6px 12px',
                  backgroundColor: '#f8f9fa',
                  border: '1px solid #dee2e6',
                  borderRadius: '15px',
                  cursor: 'pointer',
                  fontSize: '12px',
                  color: '#495057',
                  transition: 'all 0.2s'
                }}
                onMouseEnter={(e) => {
                  e.target.style.backgroundColor = '#e9ecef';
                  e.target.style.borderColor = '#adb5bd';
                }}
                onMouseLeave={(e) => {
                  e.target.style.backgroundColor = '#f8f9fa';
                  e.target.style.borderColor = '#dee2e6';
                }}
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Search Result */}
      {result && (
        <div 
          style={{
            padding: '20px',
            border: `2px solid ${result.found ? '#28a745' : '#dc3545'}`,
            borderRadius: '8px',
            backgroundColor: result.found ? '#d4edda' : '#f8d7da',
            marginBottom: '20px'
          }}
        >
          {result.found ? (
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '15px' }}>
                <div 
                  style={{
                    width: '32px',
                    height: '32px',
                    backgroundColor: '#28a745',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '16px'
                  }}
                >
                  🎯
                </div>
                <h4 style={{ margin: 0, color: '#155724', fontSize: '20px' }}>Found It!</h4>
                {result.confidence && (
                  <span 
                    style={{
                      padding: '4px 8px',
                      backgroundColor: getConfidenceColor(result.confidence),
                      color: 'white',
                      borderRadius: '12px',
                      fontSize: '11px',
                      fontWeight: '600'
                    }}
                  >
                    {Math.round(result.confidence * 100)}% - {getConfidenceText(result.confidence)}
                  </span>
                )}
              </div>

              <div style={{ marginBottom: '15px' }}>
                <div style={{ fontSize: '18px', fontWeight: '500', color: '#155724', marginBottom: '8px' }}>
                  📍 {result.location}
                </div>
                
                <div style={{ fontSize: '14px', color: '#6c757d' }}>
                  ⏰ Last seen: {formatTimestamp(result.timestamp)}
                  {result.video_no && (
                    <span style={{ marginLeft: '15px' }}>
                      🎥 Video ID: {result.video_no.slice(0, 12)}...
                    </span>
                  )}
                </div>
              </div>

              {result.object_info && (
                <div style={{ 
                  fontSize: '12px', 
                  color: '#6c757d',
                  paddingTop: '10px',
                  borderTop: '1px solid #c3e6cb'
                }}>
                  Searching for: {result.object_info.alias}
                </div>
              )}
            </div>
          ) : (
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
                <div 
                  style={{
                    width: '32px',
                    height: '32px',
                    backgroundColor: '#dc3545',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '16px'
                  }}
                >
                  ❌
                </div>
                <h4 style={{ margin: 0, color: '#721c24', fontSize: '18px' }}>Not Found</h4>
              </div>
              <p style={{ color: '#721c24', margin: 0 }}>{result.message}</p>
            </div>
          )}
        </div>
      )}

      {/* Search History */}
      {searchHistory.length > 0 && (
        <div>
          <h4 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '12px', color: '#495057' }}>
            📚 Recent Finds ({searchHistory.length})
          </h4>
          <div style={{ maxHeight: '200px', overflowY: 'auto' }}>
            {searchHistory.map((obj, index) => (
              <div
                key={obj.id}
                style={{
                  padding: '10px',
                  backgroundColor: '#f8f9fa',
                  border: '1px solid #dee2e6',
                  borderRadius: '6px',
                  marginBottom: '6px',
                  cursor: 'pointer',
                  transition: 'background-color 0.2s'
                }}
                onClick={() => handleSearch(`Where is my ${obj.name}?`)}
                onMouseEnter={(e) => e.target.style.backgroundColor = '#e9ecef'}
                onMouseLeave={(e) => e.target.style.backgroundColor = '#f8f9fa'}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: '600', color: '#495057', fontSize: '14px' }}>
                      📦 {obj.name}
                    </div>
                    <div style={{ fontSize: '12px', color: '#6c757d', marginTop: '2px' }}>
                      📍 {obj.location_phrase}
                    </div>
                    <div style={{ fontSize: '11px', color: '#adb5bd', marginTop: '2px' }}>
                      {formatTimestamp(obj.last_seen_timestamp)}
                    </div>
                  </div>
                  {obj.confidence && (
                    <div 
                      style={{
                        width: '8px',
                        height: '8px',
                        backgroundColor: getConfidenceColor(obj.confidence),
                        borderRadius: '50%'
                      }}
                      title={`${Math.round(obj.confidence * 100)}% confidence`}
                    />
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Add CSS animation for spinner */}
      <style jsx>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default SearchInterface;
