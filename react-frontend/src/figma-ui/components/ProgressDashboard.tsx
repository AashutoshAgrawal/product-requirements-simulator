import { useEffect, useState } from 'react';
import { getStatus, ProgressData } from '../lib/api';
import { StageTracker } from './StageTracker';
import { AgentCard } from './AgentCard';
import { ExperienceCard } from './ExperienceCard';
import { InterviewCard } from './InterviewCard';
import { NeedCard } from './NeedCard';
import { Progress } from './ui/progress';
import { Card, CardContent } from './ui/card';
import { Loader2 } from 'lucide-react';

interface ProgressDashboardProps {
  jobId: string;
  onComplete: (data: ProgressData) => void;
}

const POLL_INTERVAL = 2000; // 2 seconds
const STAGES = ['Agent Generation', 'Experience Simulation', 'Interview', 'Need Extraction'];

export function ProgressDashboard({ jobId, onComplete }: ProgressDashboardProps) {
  const [progressData, setProgressData] = useState<ProgressData | null>(null);
  const [prevCounts, setPrevCounts] = useState({
    agents: 0,
    experiences: 0,
    interviews: 0,
    needs: 0
  });

  useEffect(() => {
    let intervalId: NodeJS.Timeout;

    const poll = async () => {
      try {
        const data = await getStatus(jobId);
        
        // Only update if there are actual changes
        const currentCounts = {
          agents: data.intermediate_results.agents.length,
          experiences: data.intermediate_results.experiences.length,
          interviews: data.intermediate_results.interviews.length,
          needs: data.intermediate_results.needs.length
        };

        // Update state to trigger re-render with new items
        setProgressData(data);
        setPrevCounts(currentCounts);

        if (data.status === 'completed' || data.progress.completed) {
          clearInterval(intervalId);
          setTimeout(() => onComplete(data), 1000);
        }
      } catch (error) {
        console.error('Error polling status:', error);
      }
    };

    // Initial poll
    poll();

    // Set up polling
    intervalId = setInterval(poll, POLL_INTERVAL);

    return () => clearInterval(intervalId);
  }, [jobId, onComplete]);

  if (!progressData) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 animate-spin text-primary mx-auto mb-4" />
          <p className="text-muted-foreground">Initializing analysis...</p>
        </div>
      </div>
    );
  }

  const { progress, intermediate_results } = progressData;
  const progressPercentage = ((progress.stage_number - 1) / 4) * 100 + 
    (progress.stage_number === 4 && progress.completed ? 25 : 0);

  return (
    <div className="min-h-screen bg-background pb-12">
      {/* Header */}
      <div className="bg-card border-b border-border sticky top-0 z-20 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="text-center mb-6">
            <h2 className="mb-2">Analysis in Progress</h2>
            <p className="text-sm text-muted-foreground">{progress.message}</p>
          </div>
          
          {/* Stage Tracker */}
          <div className="mb-6">
            <StageTracker currentStage={progress.stage_number} stages={STAGES} />
          </div>

          {/* Progress Bar */}
          <div className="max-w-2xl mx-auto">
            <Progress value={progressPercentage} className="h-2" />
            <p className="text-xs text-center text-muted-foreground mt-2">
              {Math.round(progressPercentage)}% complete
            </p>
          </div>
        </div>
      </div>

      {/* Content Sections */}
      <div className="max-w-7xl mx-auto px-4 mt-8 space-y-10">
        {/* Agents Section */}
        {intermediate_results.agents.length > 0 && (
          <section>
            <div className="flex items-center justify-between mb-4">
              <h3>User Personas</h3>
              <span className="text-sm text-muted-foreground">
                {intermediate_results.agents.length} generated
              </span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {intermediate_results.agents.map((agent, idx) => (
                <AgentCard key={agent.id} agent={agent} index={idx} />
              ))}
            </div>
          </section>
        )}

        {/* Experiences Section */}
        {intermediate_results.experiences.length > 0 && (
          <section>
            <div className="flex items-center justify-between mb-4">
              <h3>Product Experiences</h3>
              <span className="text-sm text-muted-foreground">
                {intermediate_results.experiences.length} simulated
              </span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {intermediate_results.experiences.map((exp, idx) => (
                <ExperienceCard key={`exp-${exp.agent_id}`} experience={exp} index={idx} />
              ))}
            </div>
          </section>
        )}

        {/* Interviews Section */}
        {intermediate_results.interviews.length > 0 && (
          <section>
            <div className="flex items-center justify-between mb-4">
              <h3>User Interviews</h3>
              <span className="text-sm text-muted-foreground">
                {intermediate_results.interviews.length} conducted
                {progress.stage_number === 3 && !progress.completed && (
                  <span className="ml-2 text-primary">• In progress</span>
                )}
              </span>
            </div>
            {progress.stage_number === 3 && !progress.completed && intermediate_results.interviews.length > 0 && (
              <Card className="mb-4 border-primary/50 bg-primary/5">
                <CardContent className="py-3">
                  <p className="text-sm">
                    <span className="text-muted-foreground">Currently asking Agent {intermediate_results.interviews[intermediate_results.interviews.length - 1].agent_id}:</span>
                    <span className="ml-2 font-medium">
                      {intermediate_results.interviews[intermediate_results.interviews.length - 1].interview[
                        intermediate_results.interviews[intermediate_results.interviews.length - 1].interview.length - 1
                      ]?.question || 'Conducting interview...'}
                    </span>
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">
                    Question {intermediate_results.interviews[intermediate_results.interviews.length - 1].interview.length} in progress
                  </p>
                </CardContent>
              </Card>
            )}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {intermediate_results.interviews.map((interview, idx) => (
                <InterviewCard key={`int-${interview.agent_id}`} interview={interview} index={idx} />
              ))}
            </div>
          </section>
        )}

        {/* Needs Section */}
        {intermediate_results.needs.length > 0 && (
          <section>
            <div className="flex items-center justify-between mb-4">
              <h3>Latent Needs</h3>
              <span className="text-sm text-muted-foreground">
                {intermediate_results.needs.length} extracted
              </span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {intermediate_results.needs.map((need, idx) => (
                <NeedCard key={`need-${idx}`} need={need} index={idx} />
              ))}
            </div>
          </section>
        )}

        {/* Empty State */}
        {intermediate_results.agents.length === 0 && (
          <Card className="border-dashed">
            <CardContent className="py-12 text-center">
              <Loader2 className="w-12 h-12 animate-spin text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">
                Generating user personas...
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
