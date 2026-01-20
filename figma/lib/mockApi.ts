// Mock API to simulate backend behavior
// In production, replace with real API calls to FastAPI backend

export interface Agent {
  id: number;
  name: string;
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
}

export interface JobResponse {
  job_id: string;
  status: string;
}

// Simulated data generation
const mockAgents: Omit<Agent, 'id'>[] = [
  {
    name: "Sarah Chen",
    description: "Senior Product Manager at a SaaS company, 8 years experience in B2B software",
    reasoning: "Represents power users who need advanced features and efficiency"
  },
  {
    name: "Marcus Thompson",
    description: "Small business owner with limited technical background, runs a local retail shop",
    reasoning: "Represents non-technical users who need intuitive, simple solutions"
  },
  {
    name: "Dr. Aisha Patel",
    description: "Researcher at a university, uses tools for data analysis and collaboration",
    reasoning: "Represents academic users with specific workflow requirements"
  },
  {
    name: "Jamie Rodriguez",
    description: "College student and part-time freelancer, tech-savvy early adopter",
    reasoning: "Represents younger demographic with high digital literacy expectations"
  },
  {
    name: "Robert Kim",
    description: "Enterprise IT administrator managing tools for 500+ employees",
    reasoning: "Represents decision-makers focused on scalability and security"
  }
];

const mockExperiences: Record<number, Omit<Experience, 'agent_id'>> = {
  0: {
    steps: [
      {
        step: 1,
        action: "Attempted to set up initial account and configure team settings",
        observation: "Interface had many options but unclear hierarchy of what to configure first",
        challenge: "Spent extra time determining which settings were critical vs. optional"
      },
      {
        step: 2,
        action: "Tried to import existing data from previous tool",
        observation: "Import feature was buried in settings menu, not prominent during onboarding",
        challenge: "Had to search documentation to find the import functionality"
      },
      {
        step: 3,
        action: "Attempted to create first project and invite team members",
        observation: "Permission system was complex with many granular options",
        challenge: "Uncertain about optimal permission structure for team"
      }
    ]
  },
  1: {
    steps: [
      {
        step: 1,
        action: "Opened the application and tried to complete the first task",
        observation: "Many technical terms and jargon that were unfamiliar",
        challenge: "Felt overwhelmed by the number of features presented upfront"
      },
      {
        step: 2,
        action: "Looked for help or tutorial to understand basic functions",
        observation: "Help documentation was comprehensive but very technical",
        challenge: "Needed simpler, step-by-step guidance for basic operations"
      },
      {
        step: 3,
        action: "Attempted to complete a common task without assistance",
        observation: "Process required multiple steps that weren't clearly indicated",
        challenge: "Had to use trial and error to discover the correct workflow"
      }
    ]
  },
  2: {
    steps: [
      {
        step: 1,
        action: "Set up a new research project with multiple collaborators",
        observation: "Collaboration features were present but lacked real-time sync indicators",
        challenge: "Uncertain whether team members could see changes immediately"
      },
      {
        step: 2,
        action: "Tried to export data in specific format required for publication",
        observation: "Limited export format options, missing some academic standards",
        challenge: "Had to use workarounds to convert data to required format"
      },
      {
        step: 3,
        action: "Attempted to set up version control for research documentation",
        observation: "Version history existed but was not detailed enough for research needs",
        challenge: "Could not track specific changes or revert to precise earlier states"
      }
    ]
  },
  3: {
    steps: [
      {
        step: 1,
        action: "Downloaded and installed the application on mobile device",
        observation: "Mobile app felt like a scaled-down version, missing key features",
        challenge: "Had to switch to desktop for important tasks, disrupting workflow"
      },
      {
        step: 2,
        action: "Tried to use keyboard shortcuts for efficiency",
        observation: "Few keyboard shortcuts available, not customizable",
        challenge: "Slower than expected for power user workflows"
      },
      {
        step: 3,
        action: "Attempted to integrate with other tools in workflow",
        observation: "Integration options were limited to major platforms only",
        challenge: "Could not connect with preferred niche tools"
      }
    ]
  },
  4: {
    steps: [
      {
        step: 1,
        action: "Evaluated security and compliance features for enterprise deployment",
        observation: "Security documentation was scattered across multiple pages",
        challenge: "Difficult to assess complete security posture quickly"
      },
      {
        step: 2,
        action: "Tested bulk user provisioning and management features",
        observation: "Bulk operations were available but had rate limits that seemed low",
        challenge: "Would need multiple operations to onboard entire organization"
      },
      {
        step: 3,
        action: "Attempted to set up Single Sign-On (SSO) for organization",
        observation: "SSO configuration required contacting sales for enterprise plan",
        challenge: "Could not test critical security feature during evaluation"
      }
    ]
  }
};

const mockInterviews: Record<number, Omit<Interview, 'agent_id'>> = {
  0: {
    interview: [
      {
        question: "What was the most frustrating aspect of your experience with this product?",
        answer: "The biggest frustration was the unclear onboarding flow. As someone who's implemented many tools, I expected a more guided setup process that prioritizes critical configurations. The data import feature should have been front and center during onboarding, not hidden in settings."
      },
      {
        question: "If you could change one thing about the product to better meet your needs, what would it be?",
        answer: "I'd redesign the permission system to have smart defaults with an 'advanced mode' toggle. Most teams need standard roles like Admin, Editor, Viewer. The current granular approach is powerful but overwhelming. Give me quick setup with the option to customize later."
      }
    ]
  },
  1: {
    interview: [
      {
        question: "What was the most frustrating aspect of your experience with this product?",
        answer: "I felt lost from the start. There were so many buttons and options, and I didn't know what half of them meant. I just wanted to do simple tasks, but everything seemed designed for tech experts. I almost gave up and went back to my old, simpler tool."
      },
      {
        question: "If you could change one thing about the product to better meet your needs, what would it be?",
        answer: "Make it simpler! Have a 'basic mode' that only shows what I need for everyday tasks. Maybe a wizard that walks me through common operations step by step. I don't need all the fancy features - I just need to get my work done without feeling stupid."
      }
    ]
  },
  2: {
    interview: [
      {
        question: "What was the most frustrating aspect of your experience with this product?",
        answer: "The lack of detailed version control and limited export formats. In academic work, we need precise tracking of every change for reproducibility and audit trails. Also, not supporting standard academic formats like BibTeX or specific data formats required by journals created extra work."
      },
      {
        question: "If you could change one thing about the product to better meet your needs, what would it be?",
        answer: "Add robust academic features: detailed version control with diff views, citation management, support for academic export formats, and better real-time collaboration with clear indicators of who's editing what. These are standard in academic tools but missing here."
      }
    ]
  },
  3: {
    interview: [
      {
        question: "What was the most frustrating aspect of your experience with this product?",
        answer: "The mobile experience was disappointing - it felt like an afterthought rather than a first-class experience. Also, the lack of customizable keyboard shortcuts and limited integrations held me back. I'm used to tools that let me work my way and connect everything in my workflow."
      },
      {
        question: "If you could change one thing about the product to better meet your needs, what would it be?",
        answer: "Build a truly mobile-first experience with feature parity, add extensive keyboard shortcut customization, and create an open API so I can build my own integrations. Let power users customize the tool to match their workflow, not force them into yours."
      }
    ]
  },
  4: {
    interview: [
      {
        question: "What was the most frustrating aspect of your experience with this product?",
        answer: "The inability to properly evaluate security features before commitment. Enterprise decisions involve significant due diligence, and hiding SSO behind a sales call is a red flag. Also, scattered security documentation and low rate limits for bulk operations suggest the product wasn't designed for enterprise scale."
      },
      {
        question: "If you could change one thing about the product to better meet your needs, what would it be?",
        answer: "Provide a comprehensive security center with all compliance certifications, security features, and architecture documentation in one place. Offer a trial of enterprise features including SSO. Increase bulk operation limits to enterprise scale. Show you understand enterprise needs upfront."
      }
    ]
  }
};

const mockNeeds: Need[] = [
  {
    category: 'Usability',
    need_statement: 'Users need a guided onboarding flow that prioritizes critical setup steps so that they can configure the product efficiently without missing important features',
    evidence: 'Sarah: "The biggest frustration was the unclear onboarding flow...The data import feature should have been front and center"',
    priority: 'High',
    design_implication: 'Create a progressive onboarding wizard that surfaces critical features (like data import) first, with optional advanced configurations available later'
  },
  {
    category: 'Usability',
    need_statement: 'Non-technical users need a simplified interface mode so that they can accomplish common tasks without feeling overwhelmed by advanced features',
    evidence: 'Marcus: "I felt lost from the start...everything seemed designed for tech experts. I almost gave up"',
    priority: 'High',
    design_implication: 'Implement a "Basic Mode" toggle that shows only essential features, with contextual hints and step-by-step wizards for common workflows'
  },
  {
    category: 'Functional',
    need_statement: 'Academic users need detailed version control with diff views and standard academic export formats so that they can maintain reproducibility and comply with publication requirements',
    evidence: 'Dr. Patel: "lack of detailed version control and limited export formats...we need precise tracking of every change for reproducibility"',
    priority: 'Medium',
    design_implication: 'Add granular version control showing line-by-line changes, and support for BibTeX, CSV, and discipline-specific export formats'
  },
  {
    category: 'Functional',
    need_statement: 'Power users need customizable keyboard shortcuts and a mobile experience with feature parity so that they can work efficiently across devices',
    evidence: 'Jamie: "lack of customizable keyboard shortcuts...Mobile app felt like a scaled-down version, missing key features"',
    priority: 'Medium',
    design_implication: 'Build a keyboard shortcut customization panel and redesign mobile app for feature parity using responsive design patterns'
  },
  {
    category: 'Functional',
    need_statement: 'Users need permission management with smart defaults and simple role templates so that they can quickly set up team access without complexity',
    evidence: 'Sarah: "Permission system was complex...Uncertain about optimal permission structure for team"',
    priority: 'High',
    design_implication: 'Provide preset role templates (Admin, Editor, Viewer) with one-click setup, plus an "Advanced" mode for granular customization'
  },
  {
    category: 'Safety',
    need_statement: 'Enterprise administrators need transparent security documentation and trial access to security features so that they can evaluate compliance before commitment',
    evidence: 'Robert: "inability to properly evaluate security features...hiding SSO behind a sales call is a red flag"',
    priority: 'High',
    design_implication: 'Create a centralized Security Center with all certifications and architecture docs, and offer time-limited trials of enterprise features including SSO'
  },
  {
    category: 'Performance',
    need_statement: 'Enterprise users need higher rate limits for bulk operations so that they can onboard large organizations efficiently',
    evidence: 'Robert: "Bulk operations...had rate limits that seemed low...Would need multiple operations to onboard entire organization"',
    priority: 'Medium',
    design_implication: 'Implement tiered rate limits based on plan size, with enterprise plans supporting 1000+ bulk operations'
  },
  {
    category: 'Functional',
    need_statement: 'Users need an open API and expanded integration options so that they can connect the product with their existing workflow tools',
    evidence: 'Jamie: "Integration options were limited to major platforms...Could not connect with preferred niche tools"',
    priority: 'Medium',
    design_implication: 'Develop a comprehensive REST API with webhooks and create integration templates for popular tools, plus documentation for custom integrations'
  },
  {
    category: 'Usability',
    need_statement: 'Users need contextual help and progressive disclosure of features so that they can learn the product at their own pace',
    evidence: 'Marcus: "Help documentation was comprehensive but very technical...Needed simpler, step-by-step guidance"',
    priority: 'Medium',
    design_implication: 'Add in-app tooltips, interactive tutorials, and a simplified "Getting Started" guide separate from technical documentation'
  },
  {
    category: 'Functional',
    need_statement: 'Collaborative users need real-time sync indicators so that they can understand when their changes are visible to team members',
    evidence: 'Dr. Patel: "Collaboration features...lacked real-time sync indicators...Uncertain whether team members could see changes immediately"',
    priority: 'Low',
    design_implication: 'Add presence indicators showing active users and real-time sync status badges (e.g., "Synced", "Syncing", "Offline")'
  }
];

// Simulated job storage
const jobs: Map<string, {
  product: string;
  design_context: string;
  n_agents: number;
  startTime: number;
  currentStage: number;
  agentIndex: number;
}> = new Map();

export async function submitAnalysis(data: {
  product: string;
  design_context: string;
  n_agents: number;
}): Promise<JobResponse> {
  const job_id = `job_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  
  jobs.set(job_id, {
    ...data,
    startTime: Date.now(),
    currentStage: 1,
    agentIndex: 0
  });

  return {
    job_id,
    status: 'queued'
  };
}

export async function getStatus(job_id: string): Promise<ProgressData> {
  const job = jobs.get(job_id);
  
  if (!job) {
    return {
      status: 'failed',
      progress: {
        stage: 'Error',
        stage_number: 0,
        total_stages: 4,
        message: 'Job not found',
        completed: false
      },
      intermediate_results: {
        agents: [],
        experiences: [],
        interviews: [],
        needs: []
      }
    };
  }

  const elapsed = Date.now() - job.startTime;
  const agents: Agent[] = [];
  const experiences: Experience[] = [];
  const interviews: Interview[] = [];
  const needs: Need[] = [];

  // Stage 1: Agent Generation (0-30s, ~6s per agent)
  const stage1Duration = job.n_agents * 6000;
  const stage2Duration = job.n_agents * 8000;
  const stage3Duration = job.n_agents * 10000;
  const stage4Duration = 15000;
  
  const stage1End = stage1Duration;
  const stage2End = stage1End + stage2Duration;
  const stage3End = stage2End + stage3Duration;
  const stage4End = stage3End + stage4Duration;

  let currentStage = 1;
  let stageName = 'Agent Generation';
  let message = 'Generating diverse user personas...';
  let completed = false;

  if (elapsed < stage1End) {
    // Stage 1: Agents appearing one by one
    const agentsGenerated = Math.min(
      Math.floor(elapsed / 6000),
      job.n_agents
    );
    for (let i = 0; i < agentsGenerated; i++) {
      agents.push({ id: i, ...mockAgents[i] });
    }
    message = `Generated ${agentsGenerated}/${job.n_agents} user personas...`;
  } else if (elapsed < stage2End) {
    // Stage 2: All agents, experiences appearing
    currentStage = 2;
    stageName = 'Experience Simulation';
    for (let i = 0; i < job.n_agents; i++) {
      agents.push({ id: i, ...mockAgents[i] });
    }
    const experiencesGenerated = Math.min(
      Math.floor((elapsed - stage1End) / 8000),
      job.n_agents
    );
    for (let i = 0; i < experiencesGenerated; i++) {
      experiences.push({ agent_id: i, ...mockExperiences[i] });
    }
    message = `Simulating product experiences ${experiencesGenerated}/${job.n_agents}...`;
  } else if (elapsed < stage3End) {
    // Stage 3: Interviews appearing
    currentStage = 3;
    stageName = 'Interview Simulation';
    for (let i = 0; i < job.n_agents; i++) {
      agents.push({ id: i, ...mockAgents[i] });
      experiences.push({ agent_id: i, ...mockExperiences[i] });
    }
    const interviewsGenerated = Math.min(
      Math.floor((elapsed - stage2End) / 10000),
      job.n_agents
    );
    for (let i = 0; i < interviewsGenerated; i++) {
      interviews.push({ agent_id: i, ...mockInterviews[i] });
    }
    message = `Conducting interviews ${interviewsGenerated}/${job.n_agents}...`;
  } else if (elapsed < stage4End) {
    // Stage 4: Needs extraction
    currentStage = 4;
    stageName = 'Latent Need Extraction';
    for (let i = 0; i < job.n_agents; i++) {
      agents.push({ id: i, ...mockAgents[i] });
      experiences.push({ agent_id: i, ...mockExperiences[i] });
      interviews.push({ agent_id: i, ...mockInterviews[i] });
    }
    const needsGenerated = Math.min(
      Math.floor((elapsed - stage3End) / 1500),
      mockNeeds.length
    );
    for (let i = 0; i < needsGenerated; i++) {
      needs.push(mockNeeds[i]);
    }
    message = `Extracting latent needs ${needsGenerated}/${mockNeeds.length}...`;
  } else {
    // Completed
    currentStage = 4;
    stageName = 'Completed';
    completed = true;
    for (let i = 0; i < job.n_agents; i++) {
      agents.push({ id: i, ...mockAgents[i] });
      experiences.push({ agent_id: i, ...mockExperiences[i] });
      interviews.push({ agent_id: i, ...mockInterviews[i] });
    }
    needs.push(...mockNeeds);
    message = 'Analysis complete!';
  }

  return {
    status: completed ? 'completed' : 'processing',
    progress: {
      stage: stageName,
      stage_number: currentStage,
      total_stages: 4,
      message,
      completed
    },
    intermediate_results: {
      agents,
      experiences,
      interviews,
      needs
    }
  };
}

export async function getResults(job_id: string): Promise<ProgressData | null> {
  return getStatus(job_id);
}
