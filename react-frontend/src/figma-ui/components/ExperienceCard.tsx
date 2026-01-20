import { Experience } from '../lib/api';
import { Activity } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { motion } from 'framer-motion';

interface ExperienceCardProps {
  experience: Experience;
  index: number;
}

export function ExperienceCard({ experience, index }: ExperienceCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.1 }}
    >
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-primary" />
            <CardTitle className="text-sm">Agent {experience.agent_id + 1} Experience</CardTitle>
          </div>
        </CardHeader>
        <CardContent className="space-y-3">
          {experience.steps.slice(0, 1).map((step) => (
            <div key={step.step} className="space-y-2">
              <div className="flex items-center gap-2">
                <Badge variant="outline" className="text-xs">Step {step.step}</Badge>
              </div>
              <div className="space-y-1.5 text-xs">
                <div>
                  <span className="text-muted-foreground">Action:</span>{' '}
                  <span className="text-foreground/90">{step.action}</span>
                </div>
                <div>
                  <span className="text-muted-foreground">Challenge:</span>{' '}
                  <span className="text-foreground/80 italic">{step.challenge}</span>
                </div>
              </div>
            </div>
          ))}
          {experience.steps.length > 1 && (
            <p className="text-xs text-muted-foreground pt-1">
              + {experience.steps.length - 1} more steps
            </p>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}
