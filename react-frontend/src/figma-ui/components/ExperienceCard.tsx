import { Experience, Agent } from '../lib/api';
import { Activity, ChevronDown } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from './ui/collapsible';
import { motion } from 'framer-motion';
import { useState } from 'react';

interface ExperienceCardProps {
  experience: Experience;
  index: number;
  agents: Agent[];
}

interface ExperienceStepProps {
  step: { step: number; action: string; observation: string; challenge: string };
}

function hashToIndex(str: string): number {
  const s = str || 'Agent';
  let h = 0;
  for (let i = 0; i < s.length; i++) h = ((h << 5) - h + s.charCodeAt(i)) | 0;
  return (Math.abs(h) % 99) + 1;
}

function getAvatarUrl(agent: { name: string; gender?: string }): string {
  const index = hashToIndex(agent.name);
  const gender = (agent.gender || '').toLowerCase();
  const folder = gender === 'female' ? 'women' : 'men';
  return `https://randomuser.me/api/portraits/${folder}/${index}.jpg`;
}

function ExperienceStep({ step }: ExperienceStepProps) {
  const [actionOpen, setActionOpen] = useState(true);
  const [observationOpen, setObservationOpen] = useState(true);
  const [challengeOpen, setChallengeOpen] = useState(true);

  return (
    <div className="space-y-2 border-b pb-3 last:border-0">
      <div className="flex items-center gap-2">
        <Badge variant="outline" className="text-xs">Step {step.step}</Badge>
      </div>
      <div className="space-y-1.5 text-xs">
        <Collapsible open={actionOpen} onOpenChange={setActionOpen}>
          <CollapsibleTrigger className="flex items-center gap-1.5 text-muted-foreground hover:text-foreground transition-colors w-full text-left">
            <ChevronDown className={`w-3 h-3 transition-transform duration-200 ${actionOpen ? 'rotate-180' : ''}`} />
            <span className="font-medium">Action</span>
          </CollapsibleTrigger>
          <CollapsibleContent className="mt-1 text-foreground/90 pl-4">
            {step.action}
          </CollapsibleContent>
        </Collapsible>
        <Collapsible open={observationOpen} onOpenChange={setObservationOpen}>
          <CollapsibleTrigger className="flex items-center gap-1.5 text-muted-foreground hover:text-foreground transition-colors w-full text-left">
            <ChevronDown className={`w-3 h-3 transition-transform duration-200 ${observationOpen ? 'rotate-180' : ''}`} />
            <span className="font-medium">Observation</span>
          </CollapsibleTrigger>
          <CollapsibleContent className="mt-1 text-foreground/90 pl-4">
            {step.observation}
          </CollapsibleContent>
        </Collapsible>
        <Collapsible open={challengeOpen} onOpenChange={setChallengeOpen}>
          <CollapsibleTrigger className="flex items-center gap-1.5 text-muted-foreground hover:text-foreground transition-colors w-full text-left">
            <ChevronDown className={`w-3 h-3 transition-transform duration-200 ${challengeOpen ? 'rotate-180' : ''}`} />
            <span className="font-medium">Challenge</span>
          </CollapsibleTrigger>
          <CollapsibleContent className="mt-1 text-foreground/80 italic pl-4">
            {step.challenge}
          </CollapsibleContent>
        </Collapsible>
      </div>
    </div>
  );
}

export function ExperienceCard({ experience, index, agents }: ExperienceCardProps) {
  const agent = agents.find(a => a.id === experience.agent_id);
  const agentName = agent?.name || `Agent ${experience.agent_id}`;
  const avatarUrl = agent ? getAvatarUrl(agent) : '';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.1 }}
    >
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center gap-3">
            {avatarUrl && (
              <img
                src={avatarUrl}
                alt={agentName}
                className="w-10 h-10 rounded-full object-cover"
                onError={(e) => {
                  (e.target as HTMLImageElement).style.display = 'none';
                }}
              />
            )}
            <div className="flex-1">
              <CardTitle className="text-sm">{agentName} Experience</CardTitle>
              {agent?.occupation && (
                <p className="text-xs text-muted-foreground mt-0.5">{agent.occupation}</p>
              )}
            </div>
            <Activity className="w-4 h-4 text-primary" />
          </div>
        </CardHeader>
        <CardContent className="space-y-3">
          {experience.steps.map((step) => (
            <ExperienceStep key={step.step} step={step} />
          ))}
        </CardContent>
      </Card>
    </motion.div>
  );
}
