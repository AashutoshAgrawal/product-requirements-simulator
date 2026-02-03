import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Progress } from './ui/progress';
import { RefreshCw, CheckCircle, XCircle, Loader2 } from 'lucide-react';
import { getReproducibilityStatus, ReproducibilityStatusResponse } from '../lib/api';

interface ReproducibilityProgressProps {
  jobId: string;
  onComplete: (results: any) => void;
}

export function ReproducibilityProgress({ jobId, onComplete }: ReproducibilityProgressProps) {
  const [status, setStatus] = useState<ReproducibilityStatusResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let intervalId: NodeJS.Timeout;

    const checkStatus = async () => {
      try {
        const response = await getReproducibilityStatus(jobId);
        setStatus(response);

        if (response.status === 'completed' && response.results) {
          clearInterval(intervalId);
          onComplete(response.results);
        } else if (response.status === 'failed') {
          clearInterval(intervalId);
          setError(response.error || 'Test failed');
        }
      } catch (err) {
        console.error('Error checking status:', err);
        setError('Failed to check test status');
      }
    };

    // Check immediately
    checkStatus();
    
    // Then poll every 3 seconds
    intervalId = setInterval(checkStatus, 3000);

    return () => clearInterval(intervalId);
  }, [jobId, onComplete]);

  const progress = status?.progress;
  const progressPercent = progress 
    ? (progress.iteration / progress.total) * 100 
    : 0;

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-background via-background to-muted/20">
      <div className="w-full max-w-xl">
        <Card className="border-2 shadow-lg">
          <CardHeader className="text-center">
            <div className="mx-auto mb-4">
              {status?.status === 'completed' ? (
                <CheckCircle className="h-16 w-16 text-green-500" />
              ) : status?.status === 'failed' ? (
                <XCircle className="h-16 w-16 text-red-500" />
              ) : (
                <div className="relative">
                  <RefreshCw className="h-16 w-16 text-primary animate-spin" />
                </div>
              )}
            </div>
            <CardTitle className="text-2xl">
              {status?.status === 'completed' 
                ? 'Test Complete!' 
                : status?.status === 'failed'
                ? 'Test Failed'
                : 'Running Reproducibility Test'}
            </CardTitle>
            <CardDescription>
              {error || progress?.message || 'Initializing test...'}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Progress Bar */}
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Progress</span>
                <span className="font-medium">
                  {progress?.iteration || 0} / {progress?.total || '?'} iterations
                </span>
              </div>
              <Progress value={progressPercent} className="h-3" />
            </div>

            {/* Iteration Status */}
            {progress && progress.total > 0 && (
              <div className="grid grid-cols-5 gap-2">
                {Array.from({ length: progress.total }, (_, i) => (
                  <div
                    key={i}
                    className={`h-2 rounded-full ${
                      i < progress.iteration
                        ? 'bg-green-500'
                        : i === progress.iteration
                        ? 'bg-primary animate-pulse'
                        : 'bg-muted'
                    }`}
                  />
                ))}
              </div>
            )}

            {/* Status Details */}
            <div className="bg-muted/50 rounded-lg p-4 space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Status</span>
                <span className="font-medium capitalize">{status?.status || 'queued'}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Job ID</span>
                <span className="font-mono text-xs">{jobId.slice(0, 8)}...</span>
              </div>
            </div>

            {/* Info Text */}
            {status?.status === 'processing' && (
              <p className="text-sm text-center text-muted-foreground">
                Each iteration runs the full pipeline. This may take several minutes.
              </p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
