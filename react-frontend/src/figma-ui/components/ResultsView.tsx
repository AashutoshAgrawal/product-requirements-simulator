import { useState, useMemo, type ReactNode } from 'react';
import { ProgressData, Agent, Experience, Interview, Need } from '../lib/api';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import {
  Download,
  Search,
  User,
  Activity,
  MessageSquare,
  Lightbulb,
  BarChart3,
  FileText,
  Settings,
  MousePointer2,
  Zap,
  Shield,
  Heart,
  Users,
  Accessibility as AccessibilityIcon
} from 'lucide-react';
import { Separator } from './ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { AnalyticsView } from './AnalyticsView';
import { TreeView, TreeNodeData } from './TreeView';
import { PersonaProfile } from './PersonaProfile';

interface ResultsViewProps {
  data: ProgressData;
  onStartNew: () => void;
}

export function ResultsView({ data, onStartNew }: ResultsViewProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [priorityFilter, setPriorityFilter] = useState<string>('all');
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

              {/* Needs: Collapsible tree by category */}
              <div className="bg-card border border-border rounded-lg p-4 min-h-[400px]">
                {filteredNeeds.length > 0 ? (
                  <TreeView
                    data={(() => {
                      const grouped: Record<string, Need[]> = {};
                      filteredNeeds.forEach((need) => {
                        if (!grouped[need.category]) grouped[need.category] = [];
                        grouped[need.category].push(need);
                      });
                      const categoryIcons: Record<string, ReactNode> = {
                        Functional: <Settings className="w-4 h-4" />,
                        Usability: <MousePointer2 className="w-4 h-4" />,
                        Performance: <Zap className="w-4 h-4" />,
                        Safety: <Shield className="w-4 h-4" />,
                        Emotional: <Heart className="w-4 h-4" />,
                        Social: <Users className="w-4 h-4" />,
                        Accessibility: <AccessibilityIcon className="w-4 h-4" />,
                      };
                      return Object.entries(grouped)
                        .sort(([a], [b]) => a.localeCompare(b))
                        .map(([category, items]): TreeNodeData => ({
                          id: `cat-${category}`,
                          label: category,
                          icon: categoryIcons[category] ?? <Lightbulb className="w-4 h-4" />,
                          badge: <Badge variant="outline">{items.length}</Badge>,
                          children: items.map((need, idx): TreeNodeData => ({
                            id: `need-${category}-${idx}`,
                            label: need.need_statement,
                            badge: (
                              <Badge
                                className={
                                  need.priority === 'High'
                                    ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
                                    : need.priority === 'Medium'
                                      ? 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400'
                                      : 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300'
                                }
                                variant="secondary"
                              >
                                {need.priority}
                              </Badge>
                            ),
                            content: (
                              <div className="space-y-4">
                                <div>
                                  <p className="font-semibold text-xs uppercase tracking-wider text-muted-foreground mb-1">Evidence</p>
                                  <p className="italic">&ldquo;{need.evidence}&rdquo;</p>
                                </div>
                                <div>
                                  <p className="font-semibold text-xs uppercase tracking-wider text-muted-foreground mb-1">Design Implication</p>
                                  <p>{need.design_implication}</p>
                                </div>
                              </div>
                            ),
                          })),
                        }));
                    })()}
                  />
                ) : (
                  <div className="py-12 text-center text-muted-foreground">No needs match your filters</div>
                )}
              </div>
            </TabsContent>

            {/* Agents Tab: Persona-style tree */}
            <TabsContent value="agents" className="space-y-4 mt-6">
              <div className="bg-card border border-border rounded-lg p-4">
                <TreeView
                  data={agents.map((agent): TreeNodeData => ({
                    id: `agent-${agent.id}`,
                    label: (
                      <div className="flex items-center gap-3 py-1">
                        <div className="w-10 h-10 rounded-full border-2 border-primary/20 bg-primary/5 shrink-0 flex items-center justify-center text-sm font-bold text-primary">
                          {agent.name.split(/\s+/).map((s) => s[0]).join('').toUpperCase().slice(0, 2)}
                        </div>
                        <div className="flex flex-col min-w-0">
                          <span className="font-bold text-base truncate">{agent.name}</span>
                          <span className="text-xs text-muted-foreground truncate">{agent.description.split('.')[0]}.</span>
                        </div>
                      </div>
                    ),
                    content: (
                      <div className="py-6 px-2 md:px-4">
                        <PersonaProfile agent={agent} />
                      </div>
                    ),
                  }))}
                />
              </div>
            </TabsContent>

            {/* Experiences Tab: Collapsible tree by agent, then steps */}
            <TabsContent value="experiences" className="space-y-4 mt-6">
              <div className="bg-card border border-border rounded-lg p-4">
                <TreeView
                  data={experiences.map((exp): TreeNodeData => ({
                    id: `exp-${exp.agent_id}`,
                    label: agents.find((a) => a.id === exp.agent_id)?.name ?? `Agent ${exp.agent_id + 1}`,
                    icon: <Activity className="w-4 h-4" />,
                    children: exp.steps.map((step): TreeNodeData => ({
                      id: `exp-${exp.agent_id}-step-${step.step}`,
                      label: `Step ${step.step}: ${step.action.length > 80 ? step.action.slice(0, 80) + '…' : step.action}`,
                      content: (
                        <div className="space-y-3">
                          <div>
                            <p className="font-semibold text-xs uppercase tracking-wider text-muted-foreground mb-1">Observation</p>
                            <p>{step.observation}</p>
                          </div>
                          <div>
                            <p className="font-semibold text-xs uppercase tracking-wider text-muted-foreground mb-1">Challenge Identified</p>
                            <p className="text-destructive/90 dark:text-destructive font-medium">{step.challenge}</p>
                          </div>
                        </div>
                      ),
                    })),
                  }))}
                />
              </div>
            </TabsContent>

            {/* Interviews Tab: Collapsible tree by agent, then Q&A */}
            <TabsContent value="interviews" className="space-y-4 mt-6">
              <div className="bg-card border border-border rounded-lg p-4">
                <TreeView
                  data={interviews.map((interview): TreeNodeData => ({
                    id: `int-${interview.agent_id}`,
                    label: agents.find((a) => a.id === interview.agent_id)?.name ?? `Agent ${interview.agent_id + 1}`,
                    icon: <MessageSquare className="w-4 h-4" />,
                    children: interview.interview.map((qa, idx): TreeNodeData => ({
                      id: `int-${interview.agent_id}-qa-${idx}`,
                      label: qa.question,
                      content: (
                        <div className="pl-2 border-l-2 border-primary/30 py-1">
                          <p className="font-semibold text-xs uppercase tracking-wider text-muted-foreground mb-1">Answer</p>
                          <p>{qa.answer}</p>
                        </div>
                      ),
                    })),
                  }))}
                />
              </div>
            </TabsContent>
          </Tabs>
        </section>
      </div>
    </div>
  );
}

