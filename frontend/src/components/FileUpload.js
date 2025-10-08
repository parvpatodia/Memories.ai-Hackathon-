import React, { useState } from 'react';
import { uploadVideo } from '../services/api';

const FileUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadedVideos, setUploadedVideos] = useState([]);
  const [message, setMessage] = useState('');

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    
    if (file) {
      // Validate file type
      if (!file.type.startsWith('video/')) {
        setMessage('Please select a video file');
        return;
      }
      
      // Validate file size (50MB limit)
      if (file.size > 50 * 1024 * 1024) {
        setMessage('File too large. Maximum size is 50MB.');
        return;
      }
      
      setSelectedFile(file);
      setMessage('');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    setMessage('');

    try {
      const response = await uploadVideo(selectedFile);
      
      setUploadedVideos([...uploadedVideos, {
        videoNo: response.video_no,
        fileName: response.file_name,
        uploadedAt: new Date().toISOString()
      }]);
      
      setSelectedFile(null);
      setMessage('Video uploaded successfully!');
      
      // Reset file input
      document.getElementById('file-input').value = '';
      
    } catch (error) {
      setMessage(`Upload failed: ${error.response?.data?.detail || error.message}`);
    } finally {
      setUploading(false);
    }
  };

  const formatFileSize = (bytes) => {
    const mb = bytes / (1024 * 1024);
    return `${mb.toFixed(1)} MB`;
  };

  return (
    <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
      <h3>📹 Upload Videos</h3>
      <p style={{ color: '#666', fontSize: '14px' }}>
        Upload short clips of your spaces (bedroom, kitchen, desk, etc.)
      </p>
      
      <div style={{ marginBottom: '15px' }}>
        <input
          id="file-input"
          type="file"
          accept="video/*"
          onChange={handleFileChange}
          style={{ marginBottom: '10px' }}
        />
        
        {selectedFile && (
          <div style={{ 
            padding: '10px', 
            backgroundColor: '#f0f8ff', 
            border: '1px solid #bee5eb',
            borderRadius: '4px',
            fontSize: '14px'
          }}>
            <strong>Selected:</strong> {selectedFile.name} ({formatFileSize(selectedFile.size)})
          </div>
        )}
      </div>
      
      <button
        onClick={handleUpload}
        disabled={!selectedFile || uploading}
        style={{
          padding: '12px 24px',
          backgroundColor: uploading ? '#ccc' : '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: uploading ? 'not-allowed' : 'pointer',
          fontSize: '16px',
          marginBottom: '15px'
        }}
      >
        {uploading ? 'Uploading...' : 'Upload Video'}
      </button>
      
      {message && (
        <div style={{
          padding: '10px',
          backgroundColor: message.includes('failed') ? '#f8d7da' : '#d4edda',
          border: `1px solid ${message.includes('failed') ? '#f5c6cb' : '#c3e6cb'}`,
          borderRadius: '4px',
          color: message.includes('failed') ? '#721c24' : '#155724',
          marginBottom: '15px'
        }}>
          {message}
        </div>
      )}
      
      {uploadedVideos.length > 0 && (
        <div>
          <h4>📦 Uploaded Videos ({uploadedVideos.length})</h4>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {uploadedVideos.map((video, index) => (
              <li key={index} style={{
                padding: '8px',
                backgroundColor: '#f8f9fa',
                margin: '4px 0',
                borderRadius: '4px',
                fontSize: '14px'
              }}>
                <strong>🎥 {video.fileName}</strong>
                <br />
                <span style={{ color: '#666' }}>ID: {video.videoNo}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
