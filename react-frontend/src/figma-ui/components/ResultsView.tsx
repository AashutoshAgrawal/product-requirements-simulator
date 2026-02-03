import { useState, useMemo } from 'react';
import { ProgressData, Agent, Experience, Interview, Need } from '../lib/api';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from './ui/collapsible';
import { Badge } from './ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { 
  Download, 
  ChevronDown, 
  ChevronUp, 
  Search, 
  User, 
  Activity, 
  MessageSquare, 
  Lightbulb,
  BarChart3,
  FileText
} from 'lucide-react';
import { Separator } from './ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { AnalyticsView } from './AnalyticsView';
import { NeedCard } from './NeedCard';

interface ResultsViewProps {
  data: ProgressData;
  onStartNew: () => void;
}

export function ResultsView({ data, onStartNew }: ResultsViewProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [priorityFilter, setPriorityFilter] = useState<string>('all');
  const [openSections, setOpenSections] = useState<Record<string, boolean>>({
    agents: true,
    experiences: false,
    interviews: false,
    needs: true
  });

  const { agents, experiences, interviews, needs } = data.intermediate_results;

  // Calculate summary statistics
  const needsByCategory = useMemo(() => {
    const counts: Record<string, number> = {};
    needs.forEach(need => {
      counts[need.category] = (counts[need.category] || 0) + 1;
    });
    return counts;
  }, [needs]);

  const needsByPriority = useMemo(() => {
    const counts: Record<string, number> = {};
    needs.forEach(need => {
      counts[need.priority] = (counts[need.priority] || 0) + 1;
    });
    return counts;
  }, [needs]);

  // Filter needs
  const filteredNeeds = useMemo(() => {
    return needs.filter(need => {
      const matchesSearch = searchQuery === '' || 
        need.need_statement.toLowerCase().includes(searchQuery.toLowerCase()) ||
        need.evidence.toLowerCase().includes(searchQuery.toLowerCase()) ||
        need.design_implication.toLowerCase().includes(searchQuery.toLowerCase());
      
      const matchesCategory = categoryFilter === 'all' || need.category === categoryFilter;
      const matchesPriority = priorityFilter === 'all' || need.priority === priorityFilter;

      return matchesSearch && matchesCategory && matchesPriority;
    });
  }, [needs, searchQuery, categoryFilter, priorityFilter]);

  const toggleSection = (section: string) => {
    setOpenSections(prev => ({ ...prev, [section]: !prev[section] }));
  };

  const handleDownload = () => {
    const exportData = {
      timestamp: new Date().toISOString(),
      summary: {
        total_agents: agents.length,
        total_needs: needs.length,
        needs_by_category: needsByCategory,
        needs_by_priority: needsByPriority
      },
      agents,
      experiences,
      interviews,
      needs
    };

    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `elicitron-results-${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-card border-b border-border">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div>
              <h1 className="mb-1">Analysis Results</h1>
              <p className="text-sm text-muted-foreground">
                Generated {agents.length} personas and extracted {needs.length} latent needs
              </p>
            </div>
            <div className="flex gap-2">
              <Button onClick={handleDownload} variant="outline">
                <Download className="w-4 h-4 mr-2" />
                Export JSON
              </Button>
              <Button onClick={onStartNew}>
                Start New Analysis
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
        {/* Executive Summary */}
        <section>
          <h2 className="mb-4">Executive Summary</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm flex items-center gap-2">
                  <BarChart3 className="w-4 h-4" />
                  Total Needs
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-3xl">{needs.length}</p>
                <p className="text-xs text-muted-foreground mt-1">Latent needs identified</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm flex items-center gap-2">
                  <Lightbulb className="w-4 h-4" />
                  By Priority
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">High</span>
                    <Badge variant="secondary" className="bg-red-100 text-red-800">
                      {needsByPriority.High || 0}
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">Medium</span>
                    <Badge variant="secondary" className="bg-orange-100 text-orange-800">
                      {needsByPriority.Medium || 0}
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">Low</span>
                    <Badge variant="secondary" className="bg-gray-100 text-gray-800">
                      {needsByPriority.Low || 0}
                    </Badge>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm flex items-center gap-2">
                  <FileText className="w-4 h-4" />
                  Top Categories
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {Object.entries(needsByCategory)
                    .sort(([, a], [, b]) => (b as number) - (a as number))
                    .slice(0, 3)
                    .map(([category, count]) => (
                      <div key={category} className="flex items-center justify-between text-sm">
                        <span className="text-muted-foreground">{category}</span>
                        <Badge variant="outline">{count}</Badge>
                      </div>
                    ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </section>

        <Separator />

        {/* Detailed Results */}
        <section>
          <Tabs defaultValue="needs" className="w-full">
            <TabsList className="grid w-full grid-cols-5">
              <TabsTrigger value="needs">
                <Lightbulb className="w-4 h-4 mr-2" />
                Needs
              </TabsTrigger>
              <TabsTrigger value="analytics">
                <BarChart3 className="w-4 h-4 mr-2" />
                Analytics
              </TabsTrigger>
              <TabsTrigger value="agents">
                <User className="w-4 h-4 mr-2" />
                Agents
              </TabsTrigger>
              <TabsTrigger value="experiences">
                <Activity className="w-4 h-4 mr-2" />
                Experiences
              </TabsTrigger>
              <TabsTrigger value="interviews">
                <MessageSquare className="w-4 h-4 mr-2" />
                Interviews
              </TabsTrigger>
            </TabsList>

            {/* Analytics Tab */}
            <TabsContent value="analytics" className="mt-6">
              {data.analytics ? (
                <AnalyticsView 
                  analytics={data.analytics} 
                  agents={agents.map(a => a.name || '')}
                />
              ) : (
                <Card className="border-dashed">
                  <CardContent className="py-12 text-center text-muted-foreground">
                    Analytics data not available for this run
                  </CardContent>
                </Card>
              )}
            </TabsContent>

            {/* Needs Tab */}
            <TabsContent value="needs" className="space-y-4 mt-6">
              {/* Filters */}
              <Card>
                <CardContent className="pt-6">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="relative">
                      <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                      <Input
                        placeholder="Search needs..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="pl-9"
                      />
                    </div>
                    <Select value={categoryFilter} onValueChange={setCategoryFilter}>
                      <SelectTrigger>
                        <SelectValue placeholder="Filter by category" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">All Categories</SelectItem>
                        {Object.keys(needsByCategory).map(cat => (
                          <SelectItem key={cat} value={cat}>{cat}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <Select value={priorityFilter} onValueChange={setPriorityFilter}>
                      <SelectTrigger>
                        <SelectValue placeholder="Filter by priority" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">All Priorities</SelectItem>
                        <SelectItem value="High">High</SelectItem>
                        <SelectItem value="Medium">Medium</SelectItem>
                        <SelectItem value="Low">Low</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </CardContent>
              </Card>

              {/* Needs List */}
              <div className="space-y-4">
                {filteredNeeds.map((need, idx) => (
                  <NeedCard key={idx} need={need} index={idx} />
                ))}
                {filteredNeeds.length === 0 && (
                  <Card className="border-dashed">
                    <CardContent className="py-12 text-center text-muted-foreground">
                      No needs match your filters
                    </CardContent>
                  </Card>
                )}
              </div>
            </TabsContent>

            {/* Agents Tab */}
            <TabsContent value="agents" className="space-y-4 mt-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {agents.map(agent => (
                  <AgentDetailCard key={agent.id} agent={agent} />
                ))}
              </div>
            </TabsContent>

            {/* Experiences Tab */}
            <TabsContent value="experiences" className="space-y-4 mt-6">
              <div className="space-y-4">
                {experiences.map(exp => (
                  <ExperienceDetailCard key={exp.agent_id} experience={exp} />
                ))}
              </div>
            </TabsContent>

            {/* Interviews Tab */}
            <TabsContent value="interviews" className="space-y-4 mt-6">
              <div className="space-y-4">
                {interviews.map(interview => (
                  <InterviewDetailCard key={interview.agent_id} interview={interview} />
                ))}
              </div>
            </TabsContent>
          </Tabs>
        </section>
      </div>
    </div>
  );
}

// Detail card components (NeedDetailCard removed - using NeedCard instead)

function AgentDetailCard({ agent }: { agent: Agent }) {
  // Gender color mapping
  const genderConfig: Record<string, string> = {
    Male: 'bg-blue-100 text-blue-700 border-blue-200',
    Female: 'bg-pink-100 text-pink-700 border-pink-200',
    'Non-binary': 'bg-purple-100 text-purple-700 border-purple-200'
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-start gap-3">
          <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
            <User className="w-6 h-6 text-primary" />
          </div>
          <div className="flex-1">
            <div className="text-xs text-muted-foreground mb-1">Agent {agent.id}</div>
            <CardTitle>{agent.name}</CardTitle>
            {/* Age and Gender Chips */}
            {(agent.age || agent.gender) && (
              <div className="flex flex-wrap gap-1.5 mt-2">
                {agent.age && (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 text-xs font-medium rounded-full bg-gray-100 text-gray-700 border border-gray-200">
                    {agent.age} yrs
                  </span>
                )}
                {agent.gender && (
                  <span className={`inline-flex items-center gap-1 px-2 py-0.5 text-xs font-medium rounded-full border ${genderConfig[agent.gender] || 'bg-gray-100 text-gray-700 border-gray-200'}`}>
                    {agent.gender}
                  </span>
                )}
              </div>
            )}
            <CardDescription className="mt-2">{agent.description}</CardDescription>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="bg-muted/50 p-3 rounded-md">
          <p className="text-xs text-muted-foreground mb-1">Reasoning:</p>
          <p className="text-sm italic">{agent.reasoning}</p>
        </div>
      </CardContent>
    </Card>
  );
}

function ExperienceDetailCard({ experience }: { experience: Experience }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Activity className="w-5 h-5" />
          Agent {experience.agent_id} Experience
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {experience.steps.map(step => (
          <div key={step.step} className="pb-4 last:pb-0 border-b last:border-0">
            <Badge variant="outline" className="mb-3">Step {step.step}</Badge>
            <div className="space-y-2 text-sm">
              <div>
                <span className="text-muted-foreground">Action: </span>
                <span>{step.action}</span>
              </div>
              <div>
                <span className="text-muted-foreground">Observation: </span>
                <span>{step.observation}</span>
              </div>
              <div>
                <span className="text-muted-foreground">Challenge: </span>
                <span className="italic">{step.challenge}</span>
              </div>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

function InterviewDetailCard({ interview }: { interview: Interview }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <MessageSquare className="w-5 h-5" />
          Agent {interview.agent_id} Interview
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {interview.interview.map((qa, idx) => (
          <div key={idx} className="pb-4 last:pb-0 border-b last:border-0">
            <div className="space-y-2">
              <p className="text-sm">
                <span className="text-muted-foreground">Q: </span>
                {qa.question}
              </p>
              <p className="text-sm pl-4 border-l-2 border-primary/30">
                <span className="text-muted-foreground">A: </span>
                {qa.answer}
              </p>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
