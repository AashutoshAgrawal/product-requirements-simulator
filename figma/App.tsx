import { useState } from 'react';
import { InputForm } from './components/InputForm';
import { ProgressDashboard } from './components/ProgressDashboard';
import { ResultsView } from './components/ResultsView';
import { submitAnalysis, ProgressData } from './lib/mockApi';
import { Toaster } from './components/ui/sonner';
import { toast } from 'sonner@2.0.3';

type AppState = 'input' | 'progress' | 'results';

export default function App() {
  const [state, setState] = useState<AppState>('input');
  const [jobId, setJobId] = useState<string | null>(null);
  const [resultsData, setResultsData] = useState<ProgressData | null>(null);

  const handleStartAnalysis = async (formData: {
    product: string;
    design_context: string;
    n_agents: number;
  }) => {
    try {
      const response = await submitAnalysis(formData);
      setJobId(response.job_id);
      setState('progress');
      toast.success('Analysis started successfully!');
    } catch (error) {
      toast.error('Failed to start analysis. Please try again.');
      console.error('Error starting analysis:', error);
    }
  };

  const handleAnalysisComplete = (data: ProgressData) => {
    setResultsData(data);
    setState('results');
    toast.success('Analysis completed!');
  };

  const handleStartNew = () => {
    setState('input');
    setJobId(null);
    setResultsData(null);
  };

  return (
    <>
      {state === 'input' && (
        <InputForm onSubmit={handleStartAnalysis} />
      )}
      
      {state === 'progress' && jobId && (
        <ProgressDashboard 
          jobId={jobId} 
          onComplete={handleAnalysisComplete}
        />
      )}
      
      {state === 'results' && resultsData && (
        <ResultsView 
          data={resultsData}
          onStartNew={handleStartNew}
        />
      )}

      <Toaster />
    </>
  );
}
