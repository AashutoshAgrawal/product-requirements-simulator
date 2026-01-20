import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Slider } from './ui/slider';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Sparkles } from 'lucide-react';

interface InputFormProps {
  onSubmit: (data: { product: string; design_context: string; n_agents: number }) => void;
}

export function InputForm({ onSubmit }: InputFormProps) {
  const [product, setProduct] = useState('');
  const [designContext, setDesignContext] = useState('');
  const [nAgents, setNAgents] = useState([3]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (product.trim() && designContext.trim()) {
      onSubmit({
        product: product.trim(),
        design_context: designContext.trim(),
        n_agents: nAgents[0]
      });
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-background via-background to-muted/20">
      <div className="w-full max-w-2xl">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 mb-4">
            <Sparkles className="w-8 h-8 text-primary" />
          </div>
          <h1 className="mb-2">Elicitron</h1>
          <p className="text-muted-foreground">
            AI-powered requirements elicitation through simulated user interviews
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Start Analysis</CardTitle>
            <CardDescription>
              Generate user personas, simulate experiences, and extract latent needs
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="product">Product Name</Label>
                <Input
                  id="product"
                  placeholder="e.g., Project Management Tool"
                  value={product}
                  onChange={(e) => setProduct(e.target.value)}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="context">Design Context</Label>
                <Textarea
                  id="context"
                  placeholder="Describe your product, target users, and any specific areas you want to explore..."
                  value={designContext}
                  onChange={(e) => setDesignContext(e.target.value)}
                  rows={6}
                  required
                />
                <p className="text-xs text-muted-foreground">
                  Provide details about your product's purpose, target audience, and key features
                </p>
              </div>

              <div className="space-y-4">
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <Label htmlFor="agents">Number of User Personas</Label>
                    <span className="text-sm text-muted-foreground">{nAgents[0]} agents</span>
                  </div>
                  <Slider
                    id="agents"
                    min={1}
                    max={5}
                    step={1}
                    value={nAgents}
                    onValueChange={setNAgents}
                  />
                  <p className="text-xs text-muted-foreground">
                    More agents provide diverse perspectives but take longer (≈1 min per agent)
                  </p>
                </div>
              </div>

              <Button type="submit" className="w-full" size="lg">
                <Sparkles className="w-4 h-4 mr-2" />
                Start Analysis
              </Button>
            </form>
          </CardContent>
        </Card>

        <p className="text-center text-xs text-muted-foreground mt-6">
          Analysis typically takes 2-5 minutes depending on the number of personas
        </p>
      </div>
    </div>
  );
}
