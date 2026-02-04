// Real API client for FastAPI backend
// Normalizes backend responses to match Figma component expectations

import axios from 'axios';

// Use environment variable or default to localhost
const API_BASE_URL = process.env.REACT_APP_API_URL || 
  (process.env.NODE_ENV === 'production' 
    ? 'https://elicitron-backend.onrender.com'
    : 'http://localhost:8000');

// Type definitions matching Figma components
export interface Agent {
  id: number;
  name: string;
  age?: number;
  gender?: 'Male' | 'Female' | 'Non-binary';
  description: string;
  reasoning: string;
}

export interface Experience {
  agent_id: number;
  steps: {
    step: number;
    action: string;
    observation: string;
    challenge: string;
  }[];
}

export interface Interview {
  agent_id: number;
  interview: {
    question: string;
    answer: string;
  }[];
}

export interface Need {
  category: 'Functional' | 'Usability' | 'Performance' | 'Safety' | 'Emotional' | 'Social' | 'Accessibility';
  need_statement: string;
  evidence: string;
  priority: 'High' | 'Medium' | 'Low';
  design_implication: string;
  agent_id?: number;
  question?: string;
}

export interface AnalyticsData {
  overview: {
    total_duration: number;
    total_api_calls: number;
    successful_calls: number;
    failed_calls: number;
    total_tokens: number;
    total_cost: number;
    avg_latency: number;
    tokens_per_second: number;
  };
  stage_breakdown: {
    [stage: string]: {
      duration: number;
      items: number;
      api_calls: number;
      tokens: number;
      cost: number;
    };
  };
  agent_performance: Array<{
    agent_id: string;
    total_duration: number;
    total_cost: number;
    total_tokens: number;
    stages: {
      [stage: string]: {
        duration: number;
        tokens: number;
        cost: number;
      };
    };
  }>;
  api_calls: Array<{
    call_id: string;
    stage: string;
    agent_id: string | null;
    timestamp: string;
    duration: number;
    input_tokens: number;
    output_tokens: number;
    total_tokens: number;
    model: string;
    cost: number;
    status: string;
    error: string | null;
    retry_count: number;
  }>;
  activity_log: Array<{
    timestamp: string;
    type: string;
    message: string;
    metadata: any;
  }>;
  extremes: {
    slowest_call: any;
    fastest_call: any;
    most_expensive_agent: any;
    fastest_agent: any;
  };
}

export interface ProgressData {
  status: 'processing' | 'completed' | 'failed';
  progress: {
    stage: string;
    stage_number: number;
    total_stages: number;
    message: string;
    completed: boolean;
  };
  intermediate_results: {
    agents: Agent[];
    experiences: Experience[];
    interviews: Interview[];
    needs: Need[];
  };
  analytics?: AnalyticsData;
}

export interface JobResponse {
  job_id: string;
  status: string;
}

// Parse agent text into structured format
function parseAgent(agentText: string, index: number): Agent {
  const nameMatch = agentText.match(/\*\*Name\*\*:\s*(.+)/);
  const ageMatch = agentText.match(/\*\*Age\*\*:\s*(\d+)/);
  const genderMatch = agentText.match(/\*\*Gender\*\*:\s*(Male|Female|Non-binary)/i);
  const descMatch = agentText.match(/\*\*Description\*\*:\s*(.+?)(?:\n|$)/s);
  const reasoningMatch = agentText.match(/\*\*Reasoning\*\*:\s*(.+?)(?:\n\n|$)/s);
  
  return {
    id: index,
    name: nameMatch ? nameMatch[1].trim() : `Agent ${index + 1}`,
    age: ageMatch ? parseInt(ageMatch[1], 10) : undefined,
    gender: genderMatch ? (genderMatch[1].charAt(0).toUpperCase() + genderMatch[1].slice(1).toLowerCase()) as 'Male' | 'Female' | 'Non-binary' : undefined,
    description: descMatch ? descMatch[1].trim() : agentText,
    reasoning: reasoningMatch ? reasoningMatch[1].trim() : ''
  };
}

// Parse experience text into structured format
function parseExperience(experienceText: string, agentId: number): Experience {
  const steps: Experience['steps'] = [];
  
  if (!experienceText) {
    return { agent_id: agentId, steps: [] };
  }
  
  // Try to parse structured format with Step 1, Step 2, etc.
  // Pattern: **Step 1:** or **Step 1:** followed by Action/Observation/Challenge
  const stepPattern = /\*\*Step\s+(\d+):?\*\*\s*\n-?\s*\*\*Action\*\*:\s*(.+?)(?=\n-?\s*\*\*Observation|\n-?\s*\*\*Challenge|\n\n|\*\*Step|$)/gs;
  const obsPattern = /\*\*Observation\*\*:\s*(.+?)(?=\n-?\s*\*\*Challenge|\n\n|\*\*Step|$)/gs;
  const challengePattern = /\*\*Challenge\*\*:\s*(.+?)(?=\n\n|\*\*Step|$)/gs;
  
  // Find all step numbers
  const stepNumbers: number[] = [];
  let stepMatch;
  const stepRegex = /\*\*Step\s+(\d+):?\*\*/g;
  while ((stepMatch = stepRegex.exec(experienceText)) !== null) {
    stepNumbers.push(parseInt(stepMatch[1]));
  }
  
  // Parse each step
  for (let i = 0; i < stepNumbers.length; i++) {
    const stepNum = stepNumbers[i];
    const nextStepNum = stepNumbers[i + 1];
    
    // Extract section for this step
    const stepStart = experienceText.indexOf(`**Step ${stepNum}**`);
    const stepEnd = nextStepNum ? experienceText.indexOf(`**Step ${nextStepNum}**`) : experienceText.length;
    const stepSection = experienceText.substring(stepStart, stepEnd);
    
    // Extract Action
    const actionMatch = stepSection.match(/\*\*Action\*\*:\s*(.+?)(?=\n-?\s*\*\*Observation|\n-?\s*\*\*Challenge|\n\n|$)/s);
    const action = actionMatch ? actionMatch[1].trim() : '';
    
    // Extract Observation
    const obsMatch = stepSection.match(/\*\*Observation\*\*:\s*(.+?)(?=\n-?\s*\*\*Challenge|\n\n|$)/s);
    const observation = obsMatch ? obsMatch[1].trim() : '';
    
    // Extract Challenge
    const challengeMatch = stepSection.match(/\*\*Challenge\*\*:\s*(.+?)(?=\n\n|$)/s);
    const challenge = challengeMatch ? challengeMatch[1].trim() : '';
    
    if (action || observation || challenge) {
      steps.push({
        step: stepNum,
        action: action || '',
        observation: observation || '',
        challenge: challenge || ''
      });
    }
  }
  
  // Fallback: if no structured format, create a single step with full text
  if (steps.length === 0) {
    steps.push({
      step: 1,
      action: experienceText.substring(0, 500),
      observation: '',
      challenge: ''
    });
  }
  
  return {
    agent_id: agentId,
    steps
  };
}

// Normalize needs from backend
function normalizeNeeds(needs: any[]): Need[] {
  return needs.map((need, idx) => ({
    category: need.category || 'Functional',
    need_statement: need.need_statement || '',
    evidence: need.evidence || '',
    priority: need.priority || 'Medium',
    design_implication: need.design_implication || '',
    agent_id: need.agent_id,
    question: need.question
  }));
}

// Normalize intermediate results from backend
function normalizeIntermediateResults(data: any): ProgressData['intermediate_results'] {
  const agents: Agent[] = (data.agents || []).map((agent: string, idx: number) => 
    parseAgent(agent, idx)
  );
  
  const experiences: Experience[] = (data.experiences || []).map((exp: any) => {
    if (typeof exp.experience === 'string') {
      return parseExperience(exp.experience, exp.agent_id - 1);
    }
    return {
      agent_id: exp.agent_id - 1,
      steps: []
    };
  });
  
  const interviews: Interview[] = (data.interviews || []).map((int: any) => ({
    agent_id: int.agent_id - 1,
    interview: int.interview || []
  }));
  
  const needs: Need[] = normalizeNeeds(data.needs || []);
  
  return {
    agents,
    experiences,
    interviews,
    needs
  };
}

// Submit analysis request
export async function submitAnalysis(data: {
  product: string;
  design_context: string;
  n_agents: number;
  pipeline_mode?: string;
}): Promise<JobResponse> {
  const response = await axios.post(`${API_BASE_URL}/api/analyze`, {
    product: data.product,
    design_context: data.design_context,
    n_agents: data.n_agents,
    pipeline_mode: data.pipeline_mode || 'sequential'
  });
  
  return {
    job_id: response.data.job_id,
    status: response.data.status
  };
}

// Get status with normalized intermediate results
export async function getStatus(job_id: string): Promise<ProgressData> {
  const response = await axios.get(`${API_BASE_URL}/api/status/${job_id}`);
  
  const intermediateResults = normalizeIntermediateResults(
    response.data.intermediate_results || {}
  );
  
  return {
    status: response.data.status,
    progress: {
      stage: response.data.progress?.stage || 'initializing',
      stage_number: response.data.progress?.stage_number || 0,
      total_stages: response.data.progress?.total_stages || 4,
      message: response.data.progress?.message || 'Initializing...',
      completed: response.data.progress?.completed || false
    },
    intermediate_results: intermediateResults
  };
}

// Get final results
export async function getResults(job_id: string): Promise<ProgressData | null> {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/results/${job_id}`);
    const results = response.data.results;
    
    // Flatten needs from aggregated_needs.categories if needed
    let allNeeds: Need[] = [];
    if (results.aggregated_needs?.categories) {
      Object.values(results.aggregated_needs.categories).forEach((categoryNeeds: any) => {
        allNeeds.push(...normalizeNeeds(categoryNeeds));
      });
    } else if (results.aggregated_needs?.all_needs) {
      allNeeds = normalizeNeeds(results.aggregated_needs.all_needs);
    }
    
    const agents: Agent[] = (results.agents || []).map((agent: string, idx: number) => 
      parseAgent(agent, idx)
    );
    
    const experiences: Experience[] = (results.experiences || []).map((exp: any) => {
      if (typeof exp.experience === 'string') {
        return parseExperience(exp.experience, exp.agent_id - 1);
      }
      return {
        agent_id: exp.agent_id - 1,
        steps: []
      };
    });
    
    const interviews: Interview[] = (results.interviews || []).map((int: any) => ({
      agent_id: int.agent_id - 1,
      interview: int.interview || []
    }));
    
    return {
      status: 'completed',
      progress: {
        stage: 'completed',
        stage_number: 4,
        total_stages: 4,
        message: 'Analysis complete!',
        completed: true
      },
      intermediate_results: {
        agents,
        experiences,
        interviews,
        needs: allNeeds
      },
      analytics: results.analytics || undefined
    };
  } catch (error) {
    console.error('Error fetching results:', error);
    return null;
  }
}

// ==================== Reproducibility Testing API ====================

export interface ReproducibilityJobResponse {
  job_id: string;
  status: string;
  message: string;
}

export interface ReproducibilityStatusResponse {
  job_id: string;
  status: 'queued' | 'processing' | 'completed' | 'failed';
  progress?: {
    iteration: number;
    total: number;
    message: string;
  };
  error?: string;
  results?: any;
}

// Start a reproducibility test
export async function startReproducibilityTest(data: {
  product: string;
  design_context: string;
  n_agents: number;
  n_iterations: number;
}): Promise<ReproducibilityJobResponse> {
  console.log('API: startReproducibilityTest called with:', data);
  try {
    const response = await axios.post(`${API_BASE_URL}/api/reproducibility/test`, {
      product: data.product,
      design_context: data.design_context,
      n_agents: data.n_agents,
      n_iterations: data.n_iterations
    });
    console.log('API: Response received:', response.data);
    
    return {
      job_id: response.data.job_id,
      status: response.data.status,
      message: response.data.message
    };
  } catch (error) {
    console.error('API: Error in startReproducibilityTest:', error);
    throw error;
  }
}

// Get reproducibility test status
export async function getReproducibilityStatus(job_id: string): Promise<ReproducibilityStatusResponse> {
  const response = await axios.get(`${API_BASE_URL}/api/reproducibility/status/${job_id}`);
  
  return {
    job_id: response.data.job_id,
    status: response.data.status,
    progress: response.data.progress,
    error: response.data.error,
    results: response.data.results
  };
}

// Get reproducibility test results
export async function getReproducibilityResults(job_id: string): Promise<any> {
  const response = await axios.get(`${API_BASE_URL}/api/reproducibility/results/${job_id}`);
  return response.data.results;
}

