import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';
import config from './config';

const API_BASE_URL = config.apiUrl;

function App() {
  const [product, setProduct] = useState('');
  const [designContext, setDesignContext] = useState('');
  const [nAgents, setNAgents] = useState(1);
  const [, setJobId] = useState(null);
  const [, setStatus] = useState(null);
  const [progress, setProgress] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Intermediate results state
  const [agents, setAgents] = useState([]);
  const [experiences, setExperiences] = useState([]);
  const [interviews, setInterviews] = useState([]);
  const [needs, setNeeds] = useState([]);
  const [pollInterval, setPollInterval] = useState(null);
  
  // UI state for collapsible sections
  const [expandedAgents, setExpandedAgents] = useState({});
  const [expandedNeeds, setExpandedNeeds] = useState({});
  const [viewMode, setViewMode] = useState('summary'); // 'summary' or 'details'
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState('all');
  const [filterPriority, setFilterPriority] = useState('all');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResults(null);
    // Reset intermediate results
    setAgents([]);
    setExperiences([]);
    setInterviews([]);
    setNeeds([]);

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

        // Update intermediate results
        if (response.data.intermediate_results) {
          const intermediate = response.data.intermediate_results;
          if (intermediate.agents && intermediate.agents.length > agents.length) {
            setAgents(intermediate.agents);
          }
          if (intermediate.experiences && intermediate.experiences.length > experiences.length) {
            setExperiences(intermediate.experiences);
          }
          if (intermediate.interviews && intermediate.interviews.length > interviews.length) {
            setInterviews(intermediate.interviews);
          }
          if (intermediate.needs && intermediate.needs.length > needs.length) {
            setNeeds(intermediate.needs);
          }
        }

        if (response.data.status === 'completed') {
          clearInterval(interval);
          setPollInterval(null);
          fetchResults(id);
        } else if (response.data.status === 'failed') {
          clearInterval(interval);
          setPollInterval(null);
          setError(response.data.error || 'Analysis failed');
          setLoading(false);
        }
      } catch (err) {
        clearInterval(interval);
        setPollInterval(null);
        setError('Failed to fetch status');
        setLoading(false);
      }
    }, 2000);
    setPollInterval(interval);
  };

  useEffect(() => {
    return () => {
      if (pollInterval) {
        clearInterval(pollInterval);
      }
    };
  }, [pollInterval]);

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
    setAgents([]);
    setExperiences([]);
    setInterviews([]);
    setNeeds([]);
    if (pollInterval) {
      clearInterval(pollInterval);
      setPollInterval(null);
    }
  };

  // Helper function to parse agent text
  const parseAgent = (agentText) => {
    const nameMatch = agentText.match(/\*\*Name\*\*:\s*(.+)/);
    const descMatch = agentText.match(/\*\*Description\*\*:\s*(.+?)(?:\n|$)/);
    return {
      name: nameMatch ? nameMatch[1].trim() : 'Agent',
      description: descMatch ? descMatch[1].trim() : agentText.substring(0, 150) + '...',
      full: agentText
    };
  };

  // Helper to truncate text
  const truncateText = (text, maxLength) => {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  // Helper to extract first sentence
  const getFirstSentence = (text) => {
    if (!text) return '';
    const match = text.match(/^[^.!?]+[.!?]/);
    return match ? match[0] : truncateText(text, 100);
  };

  // Filter needs based on search and filters
  const filterNeeds = (needsList) => {
    if (!needsList) return [];
    return needsList.filter(need => {
      const matchesSearch = !searchTerm || 
        need.need_statement?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        need.evidence?.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesCategory = filterCategory === 'all' || need.category === filterCategory;
      const matchesPriority = filterPriority === 'all' || need.priority === filterPriority;
      return matchesSearch && matchesCategory && matchesPriority;
    });
  };

  // Get category colors
  const getCategoryColor = (category) => {
    const colors = {
      'Accessibility': '#667eea',
      'Functional': '#764ba2',
      'Usability': '#f093fb',
      'Safety': '#4facfe',
      'Emotional': '#feca57',
      'Social': '#48dbfb',
      'Performance': '#ff6b6b'
    };
    return colors[category] || '#999';
  };

  const getStageInfo = (stage) => {
    const stages = {
      'generating_agents': { number: 1, name: 'Agent Generation', icon: '👥', color: '#667eea' },
      'simulating_experiences': { number: 2, name: 'Experience Simulation', icon: '🎭', color: '#764ba2' },
      'conducting_interviews': { number: 3, name: 'Interview', icon: '💬', color: '#f093fb' },
      'extracting_needs': { number: 4, name: 'Need Extraction', icon: '🎯', color: '#4facfe' }
    };
    return stages[stage] || { number: 0, name: 'Initializing', icon: '⏳', color: '#999' };
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎯 Elicitron</h1>
        <p>AI-Powered Requirements Elicitation</p>
      </header>

      <main className="container">
        {!results ? (
          <>
            {!loading ? (
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
                    <label htmlFor="nAgents">Number of Agent Personas: {nAgents}</label>
                    <div className="slider-container">
                      <input
                        id="nAgents"
                        type="range"
                        min="1"
                        max="5"
                        value={nAgents}
                        onChange={(e) => setNAgents(e.target.value)}
                        disabled={loading}
                        className="slider"
                      />
                      <div className="slider-labels">
                        <span>1</span>
                        <span>2</span>
                        <span>3</span>
                        <span>4</span>
                        <span>5</span>
                      </div>
                    </div>
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
              </div>
            ) : (
              <div className="progress-dashboard">
                <div className="dashboard-header">
                  <h2>⏳ Analysis in Progress</h2>
                  <p className="current-message">{progress?.message || 'Initializing...'}</p>
                </div>

                {/* Stage Progress Tracker */}
                <div className="stage-tracker">
                  {[1, 2, 3, 4].map((stageNum) => {
                    const stageKeys = ['generating_agents', 'simulating_experiences', 'conducting_interviews', 'extracting_needs'];
                    const stageKey = stageKeys[stageNum - 1];
                    const stageInfo = getStageInfo(stageKey);
                    const isActive = progress?.stage_number === stageNum;
                    const isCompleted = progress?.stage_number > stageNum || (progress?.stage === stageKey && progress?.completed);

                    return (
                      <div key={stageNum} className={`stage-item ${isActive ? 'active' : ''} ${isCompleted ? 'completed' : ''}`}>
                        <div className="stage-icon">{stageInfo.icon}</div>
                        <div className="stage-label">{stageInfo.name}</div>
                        {isActive && <div className="stage-pulse"></div>}
                      </div>
                    );
                  })}
                </div>

                {/* Progress Bar */}
                <div className="progress-bar-container">
                  <div
                    className="progress-bar-fill"
                    style={{ width: `${((progress?.stage_number || 0) / 4) * 100}%` }}
                  ></div>
                </div>

                {/* Agents Section */}
                {agents.length > 0 && (
                  <div className="results-section real-time">
                    <h3>👥 Generated Agents ({agents.length}/{nAgents})</h3>
                    <div className="agents-grid">
                      {agents.map((agent, idx) => {
                        const parsed = parseAgent(agent);
                        return (
                          <div key={idx} className="agent-card fade-in">
                            <div className="agent-header">
                              <span className="agent-number">#{idx + 1}</span>
                              <h4>{parsed.name}</h4>
                            </div>
                            <p className="agent-description">{truncateText(parsed.description, 120)}</p>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}

                {/* Experiences Section */}
                {experiences.length > 0 && (
                  <div className="results-section real-time">
                    <h3>🎭 Simulated Experiences ({experiences.length}/{nAgents})</h3>
                    <div className="experiences-list">
                      {experiences.map((exp, idx) => (
                        <div key={idx} className="experience-card fade-in">
                          <div className="experience-header">
                            <span className="experience-label">Agent {exp.agent_id}</span>
                          </div>
                          <div className="experience-content">
                            <p>{getFirstSentence(exp.experience)}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Interviews Section */}
                {interviews.length > 0 && (
                  <div className="results-section real-time">
                    <h3>💬 Interviews ({interviews.length}/{nAgents})</h3>
                    <div className="interviews-list">
                      {interviews.map((interview, idx) => (
                        <div key={idx} className="interview-card fade-in">
                          <div className="interview-header">
                            <span className="interview-label">Agent {interview.agent_id}</span>
                            <span className="qa-count">{interview.interview?.length || 0} Q&A pairs</span>
                          </div>
                          {interview.interview && interview.interview.slice(0, 1).map((qa, qaIdx) => (
                            <div key={qaIdx} className="qa-pair">
                              <div className="question">❓ {qa.question}</div>
                              <div className="answer">💭 {truncateText(qa.answer, 150)}</div>
                            </div>
                          ))}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Needs Section */}
                {needs.length > 0 && (
                  <div className="results-section real-time">
                    <h3>🎯 Extracted Needs ({needs.length})</h3>
                    <div className="needs-grid">
                      {needs.slice(0, 12).map((need, idx) => (
                        <div key={idx} className="need-card-mini fade-in">
                          <div className="need-header-mini">
                            <span className={`category-badge category-${need.category?.toLowerCase()}`}>
                              {need.category}
                            </span>
                            <span className={`priority-badge priority-${need.priority?.toLowerCase()}`}>
                              {need.priority}
                            </span>
                          </div>
                          <p className="need-statement-mini">{need.need_statement}</p>
                        </div>
                      ))}
                    </div>
                    {needs.length > 12 && (
                      <p className="more-needs">+ {needs.length - 12} more needs being extracted...</p>
                    )}
                  </div>
                )}

                {/* Loading Spinner */}
                <div className="loading-spinner-container">
                  <div className="spinner"></div>
                </div>
              </div>
            )}
          </>
        ) : (
          <div className="results-container">
            <div className="results-header">
              <h2>✅ Analysis Complete</h2>
              <div className="results-header-actions">
                <div className="view-mode-toggle">
                  <button 
                    className={viewMode === 'summary' ? 'active' : ''} 
                    onClick={() => setViewMode('summary')}
                  >
                    📊 Summary
                  </button>
                  <button 
                    className={viewMode === 'details' ? 'active' : ''} 
                    onClick={() => setViewMode('details')}
                  >
                    📄 Details
                  </button>
                </div>
                <button onClick={resetForm} className="btn-secondary">
                  ← New Analysis
                </button>
              </div>
            </div>

            {/* Executive Summary Dashboard */}
            <div className="executive-summary">
              <div className="summary-grid">
                <div className="summary-metric">
                  <div className="metric-icon">👥</div>
                  <div className="metric-value">{results.metadata.n_agents}</div>
                  <div className="metric-label">Agent Personas</div>
                </div>
                <div className="summary-metric">
                  <div className="metric-icon">🎯</div>
                  <div className="metric-value">{results.aggregated_needs.total_needs}</div>
                  <div className="metric-label">Total Needs</div>
                </div>
                <div className="summary-metric">
                  <div className="metric-icon">🔴</div>
                  <div className="metric-value">
                    {Object.values(results.aggregated_needs.categories).flat().filter(n => n.priority === 'High').length}
                  </div>
                  <div className="metric-label">High Priority</div>
                </div>
                <div className="summary-metric">
                  <div className="metric-icon">📂</div>
                  <div className="metric-value">{Object.keys(results.aggregated_needs.categories).length}</div>
                  <div className="metric-label">Categories</div>
                </div>
              </div>

              {/* Key Highlights */}
              <div className="key-highlights">
                <h4>🌟 Key Highlights</h4>
                <ul>
                  <li>Product: <strong>{results.metadata.product}</strong> ({results.metadata.design_context})</li>
                  <li>Most common category: <strong>
                    {Object.entries(results.aggregated_needs.categories)
                      .sort((a, b) => b[1].length - a[1].length)[0]?.[0]}</strong> ({Object.entries(results.aggregated_needs.categories)
                      .sort((a, b) => b[1].length - a[1].length)[0]?.[1].length} needs)
                  </li>
                  <li>Analyzed through {results.metadata.n_agents} diverse user persona{results.metadata.n_agents > 1 ? 's' : ''}</li>
                </ul>
              </div>

              {/* Needs by Category Chart */}
              <div className="category-chart">
                <h4>📊 Needs Distribution</h4>
                <div className="chart-bars">
                  {Object.entries(results.aggregated_needs.categories)
                    .sort((a, b) => b[1].length - a[1].length)
                    .map(([category, needs]) => (
                      <div key={category} className="chart-bar-item">
                        <div className="chart-label">{category}</div>
                        <div className="chart-bar-container">
                          <div 
                            className="chart-bar"
                            style={{ 
                              width: `${(needs.length / results.aggregated_needs.total_needs) * 100}%`,
                              backgroundColor: getCategoryColor(category)
                            }}
                          >
                            <span className="chart-value">{needs.length}</span>
                          </div>
                        </div>
                      </div>
                    ))}
                </div>
              </div>
            </div>

            <div className="results-summary">
              <div className="summary-card">
                <h3>📋 Analysis Details</h3>
                <p><strong>Product:</strong> {results.metadata.product}</p>
                <p><strong>Context:</strong> {results.metadata.design_context}</p>
                <p><strong>Completed:</strong> {new Date().toLocaleDateString()}</p>
              </div>
            </div>

            <div className="results-section">
              <h3>👥 Agent Personas ({results.agents.length})</h3>
              <div className="agents-grid">
                {results.agents.map((agent, idx) => {
                  const parsed = parseAgent(agent);
                  const isExpanded = expandedAgents[idx];
                  return (
                    <div key={idx} className="agent-card collapsible">
                      <div className="agent-header" onClick={() => setExpandedAgents({...expandedAgents, [idx]: !isExpanded})}>
                        <div>
                          <span className="agent-number">#{idx + 1}</span>
                          <h4>{parsed.name}</h4>
                        </div>
                        <button className="expand-btn">{isExpanded ? '▼' : '▶'}</button>
                      </div>
                      <p className="agent-description-short">{parsed.description}</p>
                      {isExpanded && viewMode === 'details' && (
                        <div className="agent-details">
                          <div className="details-content" dangerouslySetInnerHTML={{ __html: parsed.full.replace(/\n/g, '<br/>') }} />
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>

            <div className="results-section">
              <div className="needs-header">
                <h3>🎯 Extracted Needs ({results.aggregated_needs.total_needs})</h3>
                
                {/* Search and Filter Controls */}
                <div className="needs-controls">
                  <input
                    type="text"
                    placeholder="🔍 Search needs..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="search-input"
                  />
                  <select 
                    value={filterCategory} 
                    onChange={(e) => setFilterCategory(e.target.value)}
                    className="filter-select"
                  >
                    <option value="all">All Categories</option>
                    {Object.keys(results.aggregated_needs.categories).map(cat => (
                      <option key={cat} value={cat}>{cat}</option>
                    ))}
                  </select>
                  <select 
                    value={filterPriority} 
                    onChange={(e) => setFilterPriority(e.target.value)}
                    className="filter-select"
                  >
                    <option value="all">All Priorities</option>
                    <option value="High">High</option>
                    <option value="Medium">Medium</option>
                    <option value="Low">Low</option>
                  </select>
                </div>
              </div>

              {Object.entries(results.aggregated_needs.categories).map(([category, categoryNeeds]) => {
                const filteredNeeds = filterNeeds(categoryNeeds);
                if (filteredNeeds.length === 0) return null;

                return (
                  <div key={category} className="category-section">
                    <h4>
                      <span className={`category-badge category-${category.toLowerCase()}`}>
                        {category}
                      </span>
                      ({filteredNeeds.length})
                    </h4>
                    <div className="needs-grid">
                      {filteredNeeds.map((need, idx) => {
                        const needKey = `${category}-${idx}`;
                        const isExpanded = expandedNeeds[needKey];
                        
                        return (
                          <div key={idx} className="need-card collapsible">
                            <div className="need-header">
                              <span className={`priority-badge priority-${need.priority?.toLowerCase()}`}>
                                {need.priority}
                              </span>
                              <button 
                                className="expand-btn-small" 
                                onClick={() => setExpandedNeeds({...expandedNeeds, [needKey]: !isExpanded})}
                              >
                                {isExpanded ? '▼' : '▶'}
                              </button>
                            </div>
                            <p className="need-statement"><strong>{need.need_statement}</strong></p>
                            <p className="need-evidence">
                              <em>Evidence:</em> {truncateText(need.evidence, 100)}
                            </p>
                            
                            {isExpanded && viewMode === 'details' && (
                              <div className="need-details">
                                <p className="need-evidence-full">
                                  <em>Full Evidence:</em> {need.evidence}
                                </p>
                                <p className="need-implication">
                                  <em>Design Implication:</em> {need.design_implication}
                                </p>
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                );
              })}
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
