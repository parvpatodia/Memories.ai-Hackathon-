import React, { useState, useEffect } from 'react';
import FileUpload from './components/FileUpload';
import ObjectTeacher from './components/ObjectTeacher';
import SearchInterface from './components/SearchInterface';
import { checkHealth } from './services/api';
import './App.css';
import ErrorBoundary from './components/ErrorBoundary';


function App() {
  const [apiStatus, setApiStatus] = useState('checking');
  const [stats, setStats] = useState({
    uploadsToday: 0,
    objectsTracked: 0,
    searchesPerformed: 0
  });

  useEffect(() => {
    checkApiHealth();
    // Refresh stats every 30 seconds
    const interval = setInterval(checkApiHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const checkApiHealth = async () => {
    try {
      const health = await checkHealth();
      setApiStatus(health.status);
    } catch (error) {
      console.error('API health check failed:', error);
      setApiStatus('error');
    }
  };

  const updateStats = (type) => {
    setStats(prev => ({
      ...prev,
      [type]: prev[type] + 1
    }));
  };

  return (
    <ErrorBoundary>
    <div className="App">
      {/* Header */}
      <header className="app-header">
        <div className="container">
          <div className="header-content">
            <div className="title-section">
              <h1 className="main-title">
                <span className="emoji">🔍</span>
                Object Finder
              </h1>
              <p className="subtitle">
                Never lose your stuff again! AI-powered object tracking for your everyday items.
              </p>
            </div>
            
            <div className="status-section">
              <div className={`api-status ${apiStatus}`}>
                <span className="status-dot"></span>
                API {apiStatus === 'healthy' ? 'Online' : apiStatus === 'checking' ? 'Checking...' : 'Offline'}
              </div>
              <div className="powered-by">
                Powered by <strong>Memories.ai</strong>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        <div className="container">
          {/* How it Works Section */}
          <section className="how-it-works">
            <h2>How It Works</h2>
            <div className="steps-grid">
              <div className="step">
                <div className="step-number">1</div>
                <h3>📹 Upload Videos</h3>
                <p>Record short clips of your spaces - bedroom, kitchen, office, anywhere you place items</p>
              </div>
              <div className="step">
                <div className="step-number">2</div>
                <h3>🧠 Teach Objects</h3>
                <p>Tell the AI what objects to track with detailed descriptions and aliases</p>
              </div>
              <div className="step">
                <div className="step-number">3</div>
                <h3>🔍 Find Anything</h3>
                <p>Ask where your items are using natural language - get instant location results</p>
              </div>
            </div>
          </section>

          {/* Main App Grid */}
          <div className="app-grid">
            <div className="app-card upload-card">
              <div className="card-header">
                <span className="card-number">1</span>
                <div className="card-title">
                  <h3>Upload Videos</h3>
                  <p>Record your spaces</p>
                </div>
              </div>
              <FileUpload onUpload={() => updateStats('uploadsToday')} />
            </div>

            <div className="app-card teach-card">
              <div className="card-header">
                <span className="card-number">2</span>
                <div className="card-title">
                  <h3>Teach Objects</h3>
                  <p>Define what to track</p>
                </div>
              </div>
              <ObjectTeacher onTeach={() => updateStats('objectsTracked')} />
            </div>

            <div className="app-card search-card">
              <div className="card-header">
                <span className="card-number">3</span>
                <div className="card-title">
                  <h3>Find Objects</h3>
                  <p>Ask where things are</p>
                </div>
              </div>
              <SearchInterface onSearch={() => updateStats('searchesPerformed')} />
            </div>
          </div>

          {/* Features Section */}
          <section className="features-section">
            <h2>Why Object Finder?</h2>
            <div className="features-grid">
              <div className="feature">
                <div className="feature-icon">🎥</div>
                <h4>Multimodal AI</h4>
                <p>Advanced video analysis combining visual, audio, and contextual understanding</p>
              </div>
              <div className="feature">
                <div className="feature-icon">🧠</div>
                <h4>Smart Memory</h4>
                <p>AI remembers where you put things with timestamp and location precision</p>
              </div>
              <div className="feature">
                <div className="feature-icon">💬</div>
                <h4>Natural Language</h4>
                <p>Ask questions like you would to a friend - no complex commands needed</p>
              </div>
              <div className="feature">
                <div className="feature-icon">⚡</div>
                <h4>Instant Results</h4>
                <p>Get location information in seconds with confidence scoring</p>
              </div>
            </div>
          </section>
        </div>
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-info">
              <p>Built for <strong>Memories.ai Global Hackathon 2025</strong></p>
              <p>Team: [Your Team Name] • Made with ❤️ and lots of ☕</p>
            </div>
            <div className="footer-stats">
              <div className="stat">
                <span className="stat-number">{stats.uploadsToday}</span>
                <span className="stat-label">Videos Uploaded</span>
              </div>
              <div className="stat">
                <span className="stat-number">{stats.objectsTracked}</span>
                <span className="stat-label">Objects Tracked</span>
              </div>
              <div className="stat">
                <span className="stat-number">{stats.searchesPerformed}</span>
                <span className="stat-label">Searches Done</span>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
    </ErrorBoundary>
  );
}


export default App;

