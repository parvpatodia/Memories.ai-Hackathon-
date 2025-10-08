import React, { useState, useEffect } from 'react';
import api from '../services/api';

const ObjectTeacher = () => {
  const [objectName, setObjectName] = useState('');
  const [objectAlias, setObjectAlias] = useState('');
  const [trackedObjects, setTrackedObjects] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [commonObjects, setCommonObjects] = useState([]);

  useEffect(() => {
    fetchTrackedObjects();
    fetchCommonObjects();
  }, []);

  const fetchTrackedObjects = async () => {
    try {
      const response = await api.get('/api/objects/');
      setTrackedObjects(response.data);
    } catch (error) {
      console.error('Failed to fetch objects:', error);
    }
  };

  const fetchCommonObjects = async () => {
    try {
      const response = await api.get('/api/objects/suggestions/common');
      setCommonObjects(response.data.common_objects);
    } catch (error) {
      console.error('Failed to fetch common objects:', error);
    }
  };

  const handleTeachObject = async (e) => {
    e.preventDefault();
    
    if (!objectName.trim() || !objectAlias.trim()) {
      setMessage('Please enter both name and description');
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      await api.post('/api/objects/', {
        name: objectName.trim(),
        alias: objectAlias.trim()
      });

      setObjectName('');
      setObjectAlias('');
      setMessage('Object taught successfully!');
      fetchTrackedObjects();
      
    } catch (error) {
      const errorMsg = error.response?.data?.detail || 'Failed to teach object';
      setMessage(`Error: ${errorMsg}`);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickAdd = (obj) => {
    setObjectName(obj.name);
    setObjectAlias(obj.alias);
  };

  const handleDeleteObject = async (objectId) => {
    if (!window.confirm('Are you sure you want to delete this object?')) {
      return;
    }

    try {
      await api.delete(`/api/objects/${objectId}`);
      setMessage('Object deleted successfully');
      fetchTrackedObjects();
    } catch (error) {
      setMessage('Failed to delete object');
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
      <h3>Teach Objects</h3>
      <p style={{ color: '#666', fontSize: '14px', marginBottom: '20px' }}>
        Tell the AI what objects to track and how to recognize them
      </p>

      <form onSubmit={handleTeachObject} style={{ marginBottom: '20px' }}>
        <div style={{ marginBottom: '15px' }}>
          <input
            type="text"
            placeholder="Object name (e.g., keys, wallet, phone)"
            value={objectName}
            onChange={(e) => setObjectName(e.target.value)}
            style={{
              width: '100%',
              padding: '10px',
              border: '1px solid #ddd',
              borderRadius: '4px',
              fontSize: '14px'
            }}
          />
        </div>

        <div style={{ marginBottom: '15px' }}>
          <textarea
            placeholder="Description with aliases (e.g., car keys, house keys, blue keychain with Honda logo)"
            value={objectAlias}
            onChange={(e) => setObjectAlias(e.target.value)}
            rows="3"
            style={{
              width: '100%',
              padding: '10px',
              border: '1px solid #ddd',
              borderRadius: '4px',
              fontSize: '14px',
              resize: 'vertical'
            }}
          />
        </div>

        <button
          type="submit"
          disabled={loading || !objectName.trim() || !objectAlias.trim()}
          style={{
            padding: '12px 24px',
            backgroundColor: loading ? '#ccc' : '#28a745',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer',
            fontSize: '16px'
          }}
        >
          {loading ? 'Teaching...' : 'Teach Object'}
        </button>
      </form>

      {message && (
        <div style={{
          padding: '10px',
          backgroundColor: message.includes('Error') ? '#f8d7da' : '#d4edda',
          border: `1px solid ${message.includes('Error') ? '#f5c6cb' : '#c3e6cb'}`,
          borderRadius: '4px',
          color: message.includes('Error') ? '#721c24' : '#155724',
          marginBottom: '15px'
        }}>
          {message}
        </div>
      )}

      {/* Quick add buttons */}
      {commonObjects.length > 0 && (
        <div style={{ marginBottom: '20px' }}>
          <h4 style={{ fontSize: '16px', marginBottom: '10px' }}>Quick Add Common Objects:</h4>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '5px' }}>
            {commonObjects.slice(0, 6).map((obj, index) => (
              <button
                key={index}
                onClick={() => handleQuickAdd(obj)}
                style={{
                  padding: '5px 10px',
                  backgroundColor: '#f8f9fa',
                  border: '1px solid #dee2e6',
                  borderRadius: '15px',
                  cursor: 'pointer',
                  fontSize: '12px',
                  transition: 'background-color 0.2s'
                }}
                onMouseEnter={(e) => e.target.style.backgroundColor = '#e9ecef'}
                onMouseLeave={(e) => e.target.style.backgroundColor = '#f8f9fa'}
              >
                {obj.name}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Tracked objects list */}
      {trackedObjects.length > 0 && (
        <div>
          <h4 style={{ fontSize: '16px', marginBottom: '10px' }}>
            Tracked Objects ({trackedObjects.length})
          </h4>
          <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
            {trackedObjects.map((obj) => (
              <div
                key={obj.id}
                style={{
                  padding: '12px',
                  backgroundColor: '#f8f9fa',
                  border: '1px solid #dee2e6',
                  borderRadius: '4px',
                  marginBottom: '8px'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div style={{ flex: 1 }}>
                    <strong style={{ color: '#28a745', fontSize: '14px' }}>
                      {obj.name}
                    </strong>
                    <p style={{ margin: '4px 0', fontSize: '12px', color: '#666' }}>
                      {obj.alias}
                    </p>
                    <div style={{ fontSize: '11px', color: '#999' }}>
                      Added: {formatDate(obj.created_at)}
                      {obj.last_seen_timestamp && (
                        <span style={{ marginLeft: '10px', color: '#007bff' }}>
                          Last seen: {obj.location_phrase}
                        </span>
                      )}
                    </div>
                  </div>
                  <button
                    onClick={() => handleDeleteObject(obj.id)}
                    style={{
                      padding: '4px 8px',
                      backgroundColor: '#dc3545',
                      color: 'white',
                      border: 'none',
                      borderRadius: '3px',
                      cursor: 'pointer',
                      fontSize: '11px'
                    }}
                    title="Delete object"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ObjectTeacher;
