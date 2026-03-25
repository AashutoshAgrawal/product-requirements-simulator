import { useState, useEffect, useMemo } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Slider } from './ui/slider';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Sparkles, History, Lightbulb, RefreshCw, FileText } from 'lucide-react';

const PROMPT_HISTORY_KEY = 'elicitron_prompt_history';
const MAX_HISTORY_ITEMS = 10;

// Pool of 15 Quick Start ideas; we randomly show 3 each time
const QUICK_START_POOL = [
  { product: 'Fitness Tracking App', context: 'A mobile app for tracking workouts, nutrition, and health metrics. Target users are health-conscious individuals aged 25-45 who want to maintain an active lifestyle.' },
  { product: 'Team Collaboration Tool', context: 'A web-based platform for remote teams to communicate, share files, and manage projects. Focus on small to medium businesses with distributed teams.' },
  { product: 'E-learning Platform', context: 'An online learning platform for professional skill development. Target users are working professionals looking to upskill in technology and business domains.' },
  { product: 'Meal Planning App', context: 'An app that suggests weekly meal plans and grocery lists based on dietary preferences, allergies, and household size. Targets busy parents and health-conscious singles.' },
  { product: 'Local Event Discovery', context: 'A mobile app for discovering concerts, meetups, and community events nearby. Target users are young professionals and students in urban areas.' },
  { product: 'Budget & Savings Tracker', context: 'Personal finance app for tracking spending, setting goals, and visualizing savings. Aimed at millennials and first-time budgeters.' },
  { product: 'Pet Care & Vet Reminders', context: 'App for pet owners to log vet visits, vaccinations, and medications with reminders. Targets dog and cat owners of all ages.' },
  { product: 'Habit Tracker', context: 'Minimal daily habit tracker with streaks and simple analytics. For people building routines around exercise, reading, or mindfulness.' },
  { product: 'Recipe Box & Grocery List', context: 'Save recipes from the web and generate shopping lists. For home cooks who want to reduce food waste and plan meals.' },
  { product: 'Volunteer Matching Platform', context: 'Connects volunteers with local nonprofits and one-off opportunities. Targets retirees, students, and cause-driven professionals.' },
  { product: 'Language Learning for Travel', context: 'Bite-sized lessons and phrasebooks for travelers. Focus on practical phrases for short trips rather than full fluency.' },
  { product: 'Neighborhood Buy/Sell Marketplace', context: 'Hyperlocal classifieds for selling furniture, gear, and kids’ items. For people who prefer pickup over shipping.' },
  { product: 'Meditation & Sleep Stories', context: 'Guided meditation and audio sleep stories for stress and insomnia. Targets stressed professionals and light sleepers.' },
  { product: 'Running Route Planner', context: 'Plan and discover running routes by distance and terrain. For casual joggers and marathon trainers in cities.' },
  { product: 'Freelancer Proposal Toolkit', context: 'Templates, tracking, and tips for freelancers writing proposals and managing client outreach. For solo consultants and gig workers.' },
];

function pickRandomSuggestions<T>(pool: T[], count: number): T[] {
  const shuffled = [...pool].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, count);
}

interface PromptHistoryItem {
  product: string;
  context: string;
  timestamp: number;
}

interface InputFormProps {
  onSubmit: (data: { product: string; design_context: string; n_agents: number }) => void;
  onReproducibilityTest?: () => void;
  onViewPastRuns?: () => void;
}

function getPromptHistory(): PromptHistoryItem[] {
  try {
    const stored = localStorage.getItem(PROMPT_HISTORY_KEY);
    return stored ? JSON.parse(stored) : [];
  } catch {
    return [];
  }
}

function savePromptToHistory(product: string, context: string): void {
  try {
    const history = getPromptHistory();
    const filtered = history.filter(
      item => !(item.product === product && item.context === context)
    );
    filtered.unshift({ product, context, timestamp: Date.now() });
    const trimmed = filtered.slice(0, MAX_HISTORY_ITEMS);
    localStorage.setItem(PROMPT_HISTORY_KEY, JSON.stringify(trimmed));
  } catch {
    // Ignore localStorage errors
  }
}

const QUICK_START_COUNT = 3;

export function InputForm({ onSubmit, onReproducibilityTest, onViewPastRuns }: InputFormProps) {
  const [product, setProduct] = useState('');
  const [designContext, setDesignContext] = useState('');
  const [nAgents, setNAgents] = useState([3]);
  const [promptHistory, setPromptHistory] = useState<PromptHistoryItem[]>([]);
  const [showHistoryDropdown, setShowHistoryDropdown] = useState(false);
  const [filteredHistory, setFilteredHistory] = useState<PromptHistoryItem[]>([]);

  const quickStartSuggestions = useMemo(
    () => pickRandomSuggestions(QUICK_START_POOL, QUICK_START_COUNT),
    []
  );

  useEffect(() => {
    setPromptHistory(getPromptHistory());
  }, []);

  useEffect(() => {
    if (product.trim() && promptHistory.length > 0) {
      const filtered = promptHistory.filter(item =>
        item.product.toLowerCase().includes(product.toLowerCase())
      );
      setFilteredHistory(filtered.slice(0, 5));
    } else {
      setFilteredHistory(promptHistory.slice(0, 5));
    }
  }, [product, promptHistory]);

  const handleProductFocus = () => {
    if (promptHistory.length > 0) {
      setShowHistoryDropdown(true);
    }
  };

  const handleProductBlur = () => {
    setTimeout(() => setShowHistoryDropdown(false), 200);
  };

  const handleHistorySelect = (item: PromptHistoryItem) => {
    setProduct(item.product);
    setDesignContext(item.context);
    setShowHistoryDropdown(false);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (product.trim() && designContext.trim()) {
      savePromptToHistory(product.trim(), designContext.trim());
      onSubmit({
        product: product.trim(),
        design_context: designContext.trim(),
        n_agents: nAgents[0]
      });
    }
  };

  const handleQuickStartClick = (suggestedProduct: string, suggestedContext: string) => {
    setProduct(suggestedProduct);
    setDesignContext(suggestedContext);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-background via-background to-muted/20">
      <div className="w-full max-w-2xl">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 mb-2">
            <Sparkles className="w-8 h-8 text-primary" />
          </div>
          <h1 className="text-4xl font-bold mb-2">Elicitron</h1>
          <p className="text-muted-foreground">
            AI-powered requirements elicitation through simulated user interviews
          </p>
        </div>

        <Card className="border-2 shadow-lg">
          <CardHeader className="pb-2">
            <CardTitle>Start Analysis</CardTitle>
            <CardDescription>
              Generate user personas, simulate experiences, and extract latent needs
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Quick Start - Fixed suggestions at the TOP */}
              <div>
                <Label className="text-sm text-muted-foreground mb-2 block">Quick Start</Label>
                <div className="flex flex-wrap gap-2">
                  {quickStartSuggestions.map((suggestion, idx) => (
                    <Button
                      key={idx}
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={() => handleQuickStartClick(suggestion.product, suggestion.context)}
                      className="text-xs"
                    >
                      <Lightbulb className="h-3 w-3 mr-1" />
                      {suggestion.product}
                    </Button>
                  ))}
                </div>
              </div>

              {/* Product Name with History Dropdown */}
              <div className="space-y-2 relative">
                <Label htmlFor="product">Product Name</Label>
                <Input
                  id="product"
                  placeholder="e.g., Project Management Tool"
                  value={product}
                  onChange={(e) => setProduct(e.target.value)}
                  onFocus={handleProductFocus}
                  onBlur={handleProductBlur}
                  autoComplete="off"
                  required
                />
                {showHistoryDropdown && filteredHistory.length > 0 && (
                  <div className="absolute z-50 w-full mt-1 bg-white border-2 border-gray-200 rounded-lg shadow-lg max-h-48 overflow-y-auto">
                    <div className="px-3 py-2 text-xs text-muted-foreground border-b border-gray-100 flex items-center gap-1.5">
                      <History className="w-3 h-3" />
                      Recent searches
                    </div>
                    {filteredHistory.map((item, index) => (
                      <button
                        key={index}
                        type="button"
                        onClick={() => handleHistorySelect(item)}
                        className="w-full px-3 py-2.5 text-left hover:bg-gray-50 transition-colors flex items-start gap-2 border-b border-gray-50 last:border-b-0"
                      >
                        <History className="w-4 h-4 text-muted-foreground mt-0.5 flex-shrink-0" />
                        <div className="min-w-0">
                          <div className="font-medium text-sm whitespace-normal break-words">{item.product}</div>
                          <div className="text-xs text-muted-foreground whitespace-normal break-words">{item.context}</div>
                        </div>
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {/* Design Context */}
              <div className="space-y-2">
                <Label htmlFor="context">Design Context</Label>
                <Textarea
                  id="context"
                  placeholder="Describe your product, target users, and any specific areas you want to explore"
                  value={designContext}
                  onChange={(e) => setDesignContext(e.target.value)}
                  rows={4}
                  required
                />
              </div>

              {/* Number of Agents Slider */}
              <div className="space-y-3">
                <div className="flex justify-between">
                  <Label>Number of User Personas</Label>
                  <span className="text-sm text-muted-foreground">{nAgents[0]} agents</span>
                </div>
                <Slider
                  value={nAgents}
                  onValueChange={setNAgents}
                  min={1}
                  max={5}
                  step={1}
                />
                <p className="text-xs text-muted-foreground">
                  More agents provide diverse perspectives but take longer (≈1 min per agent)
                </p>
              </div>

              {/* Submit Button */}
              <Button 
                type="submit" 
                className="w-full" 
                size="lg"
                disabled={!product.trim() || !designContext.trim()}
              >
                <Sparkles className="h-5 w-5 mr-2" />
                Start Analysis
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Footer: help text + Past runs / Reproducibility */}
        <div className="flex items-center justify-between mt-6 px-2 flex-wrap gap-2">
          <p className="text-xs text-muted-foreground">
            Analysis typically takes 2-5 minutes depending on the number of personas
          </p>
          <div className="flex items-center gap-2">
            {onViewPastRuns && (
              <Button
                type="button"
                variant="ghost"
                size="sm"
                onClick={onViewPastRuns}
                className="text-xs text-muted-foreground hover:text-primary"
              >
                <FileText className="h-3 w-3 mr-1" />
                Past runs
              </Button>
            )}
            {onReproducibilityTest && (
              <Button
                type="button"
                variant="ghost"
                size="sm"
                onClick={onReproducibilityTest}
                className="text-xs text-muted-foreground hover:text-primary"
              >
                <RefreshCw className="h-3 w-3 mr-1" />
                Reproducibility Test
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
