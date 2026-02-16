import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { listSavedRuns, getSavedRun, savedRunToProgressData, SavedRunMeta } from '../lib/api';
import { ProgressData } from '../lib/api';
import { FileText, ArrowLeft, Loader2, Calendar, Users, Lightbulb } from 'lucide-react';

interface PastRunsViewProps {
  onBack: () => void;
  onOpenRun: (data: ProgressData) => void;
}

export function PastRunsView({ onBack, onOpenRun }: PastRunsViewProps) {
  const [runs, setRuns] = useState<SavedRunMeta[]>([]);
  const [loading, setLoading] = useState(true);
  const [openingId, setOpeningId] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    listSavedRuns()
      .then((list) => {
        if (!cancelled) setRuns(list);
      })
      .catch(() => {
        if (!cancelled) setRuns([]);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => { cancelled = true; };
  }, []);

  const handleOpen = async (filename: string) => {
    setOpeningId(filename);
    try {
      const run = await getSavedRun(filename);
      const data = savedRunToProgressData(run);
      onOpenRun(data);
    } catch (e) {
      console.error('Failed to load run:', e);
    } finally {
      setOpeningId(null);
    }
  };

  const formatDate = (iso: string) => {
    if (!iso) return '—';
    try {
      const d = new Date(iso);
      return d.toLocaleDateString(undefined, { dateStyle: 'medium' }) + ' ' + d.toLocaleTimeString(undefined, { timeStyle: 'short' });
    } catch {
      return iso;
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-2xl font-bold flex items-center gap-2">
            <FileText className="w-7 h-7 text-primary" />
            Past runs
          </h1>
          <Button onClick={onBack} variant="outline">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back
          </Button>
        </div>

        <p className="text-muted-foreground mb-6">
          View inputs and results from previous pipeline runs. Runs are read from the server’s saved results.
        </p>

        {loading ? (
          <div className="flex justify-center py-16">
            <Loader2 className="w-10 h-10 animate-spin text-primary" />
          </div>
        ) : runs.length === 0 ? (
          <Card className="border-dashed">
            <CardContent className="py-12 text-center text-muted-foreground">
              No saved runs found. Complete an analysis to see runs here.
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            {runs.map((run) => (
              <Card
                key={run.filename}
                className="cursor-pointer hover:border-primary/50 transition-colors"
                onClick={() => handleOpen(run.filename)}
              >
                <CardHeader className="pb-2">
                  <CardTitle className="text-base flex items-center justify-between gap-2">
                    <span className="truncate">{run.product || 'Untitled run'}</span>
                    {openingId === run.filename ? (
                      <Loader2 className="w-4 h-4 animate-spin shrink-0" />
                    ) : null}
                  </CardTitle>
                  <div className="flex flex-wrap gap-3 text-xs text-muted-foreground mt-1">
                    <span className="flex items-center gap-1">
                      <Calendar className="w-3.5 h-3.5" />
                      {formatDate(run.start_time)}
                    </span>
                    <span className="flex items-center gap-1">
                      <Users className="w-3.5 h-3.5" />
                      {run.n_agents} agents
                    </span>
                    <span className="flex items-center gap-1">
                      <Lightbulb className="w-3.5 h-3.5" />
                      {run.total_needs} needs
                    </span>
                    <span>{run.mode}</span>
                  </div>
                </CardHeader>
                <CardContent className="pt-0">
                  <p className="text-sm text-muted-foreground line-clamp-2">
                    {run.design_context}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
