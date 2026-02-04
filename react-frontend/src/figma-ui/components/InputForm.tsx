import { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Slider } from './ui/slider';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Sparkles, History, Lightbulb, RefreshCw, Zap } from 'lucide-react';

const PROMPT_HISTORY_KEY = 'elicitron_prompt_history';
const MAX_HISTORY_ITEMS = 10;

// Fixed Quick Start suggestions - these never change
const QUICK_START_SUGGESTIONS = [
  { product: 'Fitness Tracking App', context: 'A mobile app for tracking workouts, nutrition, and health metrics. Target users are health-conscious individuals aged 25-45 who want to maintain an active lifestyle.' },
  { product: 'Team Collaboration Tool', context: 'A web-based platform for remote teams to communicate, share files, and manage projects. Focus on small to medium businesses with distributed teams.' },
  { product: 'E-learning Platform', context: 'An online learning platform for professional skill development. Target users are working professionals looking to upskill in technology and business domains.' },
];

interface PromptHistoryItem {
  product: string;
  context: string;
  timestamp: number;
}

interface InputFormProps {
  onSubmit: (data: { product: string; design_context: string; n_agents: number; pipeline_mode: string }) => void;
  onReproducibilityTest?: () => void;
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

export function InputForm({ onSubmit, onReproducibilityTest }: InputFormProps) {
  const [product, setProduct] = useState('');
  const [designContext, setDesignContext] = useState('');
  const [nAgents, setNAgents] = useState([3]);
  const [pipelineMode, setPipelineMode] = useState<'sequential' | 'parallel'>('sequential');
  const [promptHistory, setPromptHistory] = useState<PromptHistoryItem[]>([]);
  const [showHistoryDropdown, setShowHistoryDropdown] = useState(false);
  const [filteredHistory, setFilteredHistory] = useState<PromptHistoryItem[]>([]);

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
        n_agents: nAgents[0],
        pipeline_mode: pipelineMode
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
                  {QUICK_START_SUGGESTIONS.map((suggestion, idx) => (
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
                          <div className="font-medium text-sm truncate">{item.product}</div>
                          <div className="text-xs text-muted-foreground truncate">{item.context.substring(0, 60)}...</div>
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
                  placeholder="Describe your product, target users, and any specific areas you want to explore..."
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

              {/* Pipeline Mode Toggle */}
              <div className="space-y-3 p-4 rounded-lg bg-gray-100 border border-gray-200">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Zap className={`h-4 w-4 ${pipelineMode === 'parallel' ? 'text-amber-500' : 'text-gray-400'}`} />
                    <Label htmlFor="pipeline-mode" className="font-medium cursor-pointer">
                      Fast Mode (Parallel Processing)
                    </Label>
                  </div>
                  <button
                    type="button"
                    role="switch"
                    aria-checked={pipelineMode === 'parallel'}
                    onClick={() => setPipelineMode(pipelineMode === 'parallel' ? 'sequential' : 'parallel')}
                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 ${
                      pipelineMode === 'parallel' ? 'bg-primary' : 'bg-gray-300'
                    }`}
                  >
                    <span
                      className={`inline-block h-4 w-4 transform rounded-full bg-white shadow-lg transition-transform ${
                        pipelineMode === 'parallel' ? 'translate-x-6' : 'translate-x-1'
                      }`}
                    />
                  </button>
                </div>
                <p className="text-xs text-gray-500">
                  {pipelineMode === 'parallel' 
                    ? '⚡ Parallel: Faster execution (~2x speed), processes agents concurrently'
                    : '🔄 Sequential: Traditional stage-by-stage execution, more stable'
                  }
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

        {/* Footer with discrete reproducibility test link */}
        <div className="flex items-center justify-between mt-6 px-2">
          <p className="text-xs text-muted-foreground">
            Analysis typically takes 2-5 minutes depending on the number of personas
          </p>
          {onReproducibilityTest && (
            <Button
              type="button"
              variant="ghost"
              size="sm"
              onClick={() => {
                console.log('Reproducibility Test clicked');
                onReproducibilityTest();
              }}
              className="text-xs text-muted-foreground hover:text-primary"
            >
              <RefreshCw className="h-3 w-3 mr-1" />
              Reproducibility Test
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
