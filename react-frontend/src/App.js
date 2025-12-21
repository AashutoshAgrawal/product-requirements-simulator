import React, { useState } from 'react';
import './App.css';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [product, setProduct] = useState('');
  const [designContext, setDesignContext] = useState('');
  const [nAgents, setNAgents] = useState(1);
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState(null);
  const [progress, setProgress] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/analyze`, {
        product,
        design_context: designContext,
        n_agents: parseInt(nAgents)
      });

      setJobId(response.data.job_id);
      setStatus('queued');
      pollStatus(response.data.job_id);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to start analysis');
      setLoading(false);
    }
  };

  const pollStatus = async (id) => {
    const interval = setInterval(async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/api/status/${id}`);
        setStatus(response.data.status);
        setProgress(response.data.progress);

        if (response.data.status === 'completed') {
          clearInterval(interval);
          fetchResults(id);
        } else if (response.data.status === 'failed') {
          clearInterval(interval);
          setError(response.data.error || 'Analysis failed');
          setLoading(false);
        }
      } catch (err) {
        clearInterval(interval);
        setError('Failed to fetch status');
        setLoading(false);
      }
    }, 2000);
  };

  const fetchResults = async (id) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/results/${id}`);
      setResults(response.data.results);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch results');
      setLoading(false);
    }
  };

  const resetForm = () => {
    setProduct('');
    setDesignContext('');
    setNAgents(1);
    setJobId(null);
    setStatus(null);
    setProgress(null);
    setResults(null);
    setError(null);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎯 Elicitron</h1>
        <p>AI-Powered Requirements Elicitation</p>
      </header>

      <main className="container">
        {!results ? (
          <div className="form-container">
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="product">Product Name *</label>
                <input
                  id="product"
                  type="text"
                  value={product}
                  onChange={(e) => setProduct(e.target.value)}
                  placeholder="e.g., camping tent, smartphone, office chair"
                  required
                  disabled={loading}
                />
              </div>

              <div className="form-group">
                <label htmlFor="designContext">Design Context *</label>
                <textarea
                  id="designContext"
                  value={designContext}
                  onChange={(e) => setDesignContext(e.target.value)}
                  placeholder="e.g., ultralight backpacking in alpine conditions"
                  required
                  disabled={loading}
                  rows="4"
                />
              </div>

              <div className="form-group">
                <label htmlFor="nAgents">Number of Agent Personas</label>
                <input
                  id="nAgents"
                  type="number"
                  value={nAgents}
                  onChange={(e) => setNAgents(e.target.value)}
                  min="1"
                  max="5"
                  disabled={loading}
                />
                <small>1-5 personas (more personas = more comprehensive analysis)</small>
              </div>

              {error && (
                <div className="error-message">
                  ❌ {error}
                </div>
              )}

              <button type="submit" disabled={loading} className="btn-primary">
                {loading ? 'Analyzing...' : '🚀 Start Analysis'}
              </button>
            </form>

            {loading && progress && (
              <div className="progress-container">
                <h3>⏳ Analysis in Progress</h3>
                <div className="progress-stage">
                  <strong>Stage:</strong> {progress.stage?.replace(/_/g, ' ').toUpperCase()}
                </div>
                <div className="progress-message">
                  {progress.message}
                </div>
                <div className="spinner"></div>
              </div>
            )}
          </div>
        ) : (
          <div className="results-container">
            <div className="results-header">
              <h2>✅ Analysis Complete</h2>
              <button onClick={resetForm} className="btn-secondary">
                ← New Analysis
              </button>
            </div>

            <div className="results-summary">
              <div className="summary-card">
                <h3>📊 Summary</h3>
                <p><strong>Product:</strong> {results.metadata.product}</p>
                <p><strong>Context:</strong> {results.metadata.design_context}</p>
                <p><strong>Agents:</strong> {results.metadata.n_agents}</p>
                <p><strong>Total Needs:</strong> {results.aggregated_needs.total_needs}</p>
              </div>
            </div>

            <div className="results-section">
              <h3>👥 Agent Personas ({results.agents.length})</h3>
              {results.agents.map((agent, idx) => (
                <div key={idx} className="card">
                  <div dangerouslySetInnerHTML={{ __html: agent.replace(/\n/g, '<br/>') }} />
                </div>
              ))}
            </div>

            <div className="results-section">
              <h3>🎯 Extracted Needs</h3>
              {Object.entries(results.aggregated_needs.categories).map(([category, needs]) => (
                <div key={category} className="category-section">
                  <h4>{category} ({needs.length})</h4>
                  {needs.map((need, idx) => (
                    <div key={idx} className="need-card">
                      <div className="need-priority">{need.priority} Priority</div>
                      <p className="need-statement"><strong>{need.need_statement}</strong></p>
                      <p className="need-evidence"><em>Evidence:</em> {need.evidence.substring(0, 200)}...</p>
                      <p className="need-implication"><em>Design Implication:</em> {need.design_implication}</p>
                    </div>
                  ))}
                </div>
              ))}
            </div>

            <div className="results-actions">
              <button
                onClick={() => {
                  const dataStr = JSON.stringify(results, null, 2);
                  const dataBlob = new Blob([dataStr], { type: 'application/json' });
                  const url = URL.createObjectURL(dataBlob);
                  const link = document.createElement('a');
                  link.href = url;
                  link.download = `elicitron_results_${Date.now()}.json`;
                  link.click();
                }}
                className="btn-primary"
              >
                📥 Download Results (JSON)
              </button>
            </div>
          </div>
        )}
      </main>

      <footer>
        <p>Powered by FastAPI + React | <a href={`${API_BASE_URL}/docs`} target="_blank" rel="noopener noreferrer">API Docs</a></p>
      </footer>
    </div>
  );
}

export default App;
